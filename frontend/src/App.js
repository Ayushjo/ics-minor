import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, Shield, AlertTriangle, Activity } from 'lucide-react';
import './App.css';
import Header from './components/Header';
import StatCard from './components/StatCard';
import RealTimeChart from './components/RealTimeChart';
import RiskGauge from './components/RiskGauge';
import Decisions from './components/Decisions';
import AlertSystem from './components/AlertSystem';
import SensorHeatmap from './components/SensorHeatmap';
import AttackPatterns from './components/AttackPatterns';
import HistoricalAnalytics from './components/HistoricalAnalytics';

const SOCKET_URL = 'http://localhost:5000';

function App() {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [simulationRunning, setSimulationRunning] = useState(false);
  const [latestResults, setLatestResults] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [error, setError] = useState(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const newSocket = io(SOCKET_URL, {
      transports: ['websocket', 'polling']
    });

    newSocket.on('connect', () => {
      console.log('Connected to backend');
      setConnected(true);
      setError(null);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from backend');
      setConnected(false);
    });

    newSocket.on('connection_response', (data) => {
      console.log('Connection response:', data);
    });

    newSocket.on('real_time_update', (data) => {
      console.log('Real-time update received:', data);
      setLatestResults(data);

      // Add to history (keep last 20 data points)
      setHistoryData(prev => {
        const newHistory = [...prev, {
          timestamp: new Date().toLocaleTimeString(),
          anomalyRate: data.detection?.anomaly_rate || 0,
          cyberRisk: data.cyber_risk?.score || 0,
          operationalRisk: data.operational_risk?.score || 0,
          anomaliesCount: data.detection?.num_anomalies || 0
        }];
        return newHistory.slice(-20); // Keep last 20 points
      });
    });

    newSocket.on('simulation_started', (data) => {
      console.log('Simulation started:', data);
      setSimulationRunning(true);
    });

    newSocket.on('simulation_stopped', (data) => {
      console.log('Simulation stopped:', data);
      setSimulationRunning(false);
    });

    newSocket.on('error', (data) => {
      console.error('Socket error:', data);
      setError(data.message);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  const handleStartSimulation = () => {
    if (socket && connected) {
      socket.emit('start_simulation', {
        batch_size: 50,
        delay: 3
      });
    }
  };

  const handleStopSimulation = () => {
    if (socket && connected) {
      socket.emit('stop_simulation');
    }
  };

  const handleResetSimulation = () => {
    if (socket && connected) {
      socket.emit('reset_simulation');
      setHistoryData([]);
      setLatestResults(null);
    }
  };

  const detection = latestResults?.detection;
  const batchInfo = latestResults?.batch_info;

  return (
    <div className="app-container">
      <Header
        connected={connected}
        simulationRunning={simulationRunning}
        onStart={handleStartSimulation}
        onStop={handleStopSimulation}
        onReset={handleResetSimulation}
      />

      <main className="dashboard">
        <AnimatePresence>
          {error && (
            <motion.div
              className="error-banner"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <AlertTriangle size={16} />
              <span>{error}</span>
            </motion.div>
          )}
        </AnimatePresence>

        {!latestResults && connected && (
          <motion.div
            className="placeholder-modern"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="placeholder-icon">
              <Activity size={64} strokeWidth={1.5} />
            </div>
            <h2>System Ready</h2>
            <p>Click "Start" to begin real-time monitoring</p>
          </motion.div>
        )}

        {latestResults && latestResults.status === 'success' && (
          <>
            {/* Top Row - Stat Cards */}
            <div className="stats-grid">
              <StatCard
                title="Total Samples"
                value={batchInfo?.total_processed || 0}
                icon={Database}
                color="blue"
              />
              <StatCard
                title="Anomalies"
                value={detection?.num_anomalies || 0}
                icon={AlertTriangle}
                color="rose"
                trend={detection?.anomaly_rate > 10 ? 'up' : 'down'}
                trendValue={`${(detection?.anomaly_rate || 0).toFixed(1)}%`}
              />
              <StatCard
                title="Cyber Risk"
                value={latestResults?.cyber_risk?.score?.toFixed(0) || 0}
                unit="%"
                icon={Shield}
                color="amber"
              />
              <StatCard
                title="Op. Risk"
                value={latestResults?.operational_risk?.score?.toFixed(0) || 0}
                unit="%"
                icon={Activity}
                color="emerald"
              />
            </div>

            {/* Middle Row - Main Chart and Risk Gauges */}
            <div className="main-row">
              <div className="chart-section">
                <RealTimeChart data={historyData} />
              </div>
              <div className="risk-section">
                <RiskGauge
                  cyberRisk={latestResults?.cyber_risk}
                  operationalRisk={latestResults?.operational_risk}
                />
              </div>
            </div>

            {/* Alert System Row */}
            <div className="alerts-row">
              <AlertSystem socket={socket} latestResults={latestResults} />
            </div>

            {/* Feature Panels Row */}
            <div className="features-grid">
              <AttackPatterns latestResults={latestResults} />
              <SensorHeatmap latestResults={latestResults} />
            </div>

            {/* Decisions Row */}
            <Decisions decisions={latestResults?.decisions} />

            {/* Historical Analytics */}
            <HistoricalAnalytics socket={socket} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
