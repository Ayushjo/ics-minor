import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Thermometer, TrendingUp, AlertTriangle } from 'lucide-react';
import './SensorHeatmap.css';

function SensorHeatmap({ latestResults }) {
  const [sensorData, setSensorData] = useState([]);
  const [selectedStage, setSelectedStage] = useState('all');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

  // Stage definitions matching the SWaT system
  const stageDefinitions = {
    1: { name: 'Raw Water Supply', sensors: ['FIT101', 'LIT101', 'MV101', 'P101', 'P102'] },
    2: { name: 'Chemical Dosing', sensors: ['AIT201', 'AIT202', 'AIT203', 'FIT201', 'MV201', 'P201', 'P202', 'P203', 'P204', 'P205', 'P206'] },
    3: { name: 'Ultrafiltration', sensors: ['DPIT301', 'FIT301', 'LIT301', 'MV301', 'MV302', 'MV303', 'MV304', 'P301', 'P302'] },
    4: { name: 'UV Dechlorination', sensors: ['AIT401', 'AIT402', 'FIT401', 'LIT401', 'P401', 'P402', 'P403', 'P404', 'UV401'] },
    5: { name: 'Reverse Osmosis', sensors: ['AIT501', 'AIT502', 'AIT503', 'AIT504', 'FIT501', 'FIT502', 'FIT503', 'FIT504', 'P501', 'P502', 'PIT501', 'PIT502', 'PIT503'] },
    6: { name: 'Backwash', sensors: ['FIT601', 'P601', 'P602', 'P603'] }
  };

  useEffect(() => {
    if (latestResults && latestResults.batch_info) {
      // Generate simulated sensor anomaly data
      // In production, this would come from the backend sensor_analysis
      const sensors = generateSensorData();
      setSensorData(sensors);
    }
  }, [latestResults]);

  const generateSensorData = () => {
    const allSensors = [];

    Object.entries(stageDefinitions).forEach(([stage, info]) => {
      info.sensors.forEach(sensor => {
        // Simulate anomaly rate based on current detection rate
        const baseRate = latestResults?.detection?.anomaly_rate || 0;
        const variation = (Math.random() - 0.5) * 0.4; // +/- 20%
        const anomalyRate = Math.max(0, Math.min(100, (baseRate + variation) * 100));

        allSensors.push({
          name: sensor,
          stage: parseInt(stage),
          stageName: info.name,
          anomalyRate,
          status: anomalyRate > 30 ? 'critical' : anomalyRate > 15 ? 'warning' : 'normal'
        });
      });
    });

    return allSensors;
  };

  const getAnomalyColor = (rate) => {
    if (rate > 30) return '#f43f5e'; // critical - rose
    if (rate > 15) return '#f59e0b'; // warning - amber
    if (rate > 5) return '#3b82f6';  // info - blue
    return '#10b981'; // normal - emerald
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'critical': return 'Critical';
      case 'warning': return 'Warning';
      default: return 'Normal';
    }
  };

  const filteredSensors = selectedStage === 'all'
    ? sensorData
    : sensorData.filter(s => s.stage === parseInt(selectedStage));

  const stageStats = {};
  Object.keys(stageDefinitions).forEach(stage => {
    const stageSensors = sensorData.filter(s => s.stage === parseInt(stage));
    const avgAnomaly = stageSensors.length > 0
      ? stageSensors.reduce((sum, s) => sum + s.anomalyRate, 0) / stageSensors.length
      : 0;
    const criticalCount = stageSensors.filter(s => s.status === 'critical').length;

    stageStats[stage] = {
      avgAnomaly,
      criticalCount,
      totalSensors: stageSensors.length,
      status: criticalCount > 2 ? 'critical' : criticalCount > 0 ? 'warning' : 'normal'
    };
  });

  return (
    <motion.div
      className="card sensor-heatmap"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="heatmap-header">
        <div className="heatmap-title-section">
          <h3>Sensor Status Heatmap</h3>
          <p className="heatmap-subtitle">51 sensors across 6 processing stages</p>
        </div>
        <div className="heatmap-controls">
          <select
            className="stage-filter"
            value={selectedStage}
            onChange={(e) => setSelectedStage(e.target.value)}
          >
            <option value="all">All Stages</option>
            {Object.entries(stageDefinitions).map(([stage, info]) => (
              <option key={stage} value={stage}>
                Stage {stage}: {info.name}
              </option>
            ))}
          </select>
          <div className="view-toggle">
            <button
              className={viewMode === 'grid' ? 'active' : ''}
              onClick={() => setViewMode('grid')}
            >
              Grid
            </button>
            <button
              className={viewMode === 'list' ? 'active' : ''}
              onClick={() => setViewMode('list')}
            >
              List
            </button>
          </div>
        </div>
      </div>

      {/* Stage Overview */}
      <div className="stage-overview">
        {Object.entries(stageDefinitions).map(([stage, info]) => {
          const stats = stageStats[stage];
          return (
            <div
              key={stage}
              className={`stage-card stage-${stats?.status || 'normal'}`}
              onClick={() => setSelectedStage(stage)}
            >
              <div className="stage-number">P{stage}</div>
              <div className="stage-info">
                <div className="stage-name">{info.name}</div>
                <div className="stage-metrics">
                  <span>{stats?.avgAnomaly?.toFixed(1)}% avg</span>
                  {stats?.criticalCount > 0 && (
                    <span className="critical-badge">{stats.criticalCount} critical</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Sensor Grid/List */}
      <div className={`sensor-container sensor-${viewMode}`}>
        {filteredSensors.length === 0 ? (
          <div className="no-sensors">
            <Thermometer size={32} />
            <p>No sensor data available</p>
          </div>
        ) : (
          filteredSensors.map((sensor, index) => (
            <motion.div
              key={sensor.name}
              className={`sensor-cell sensor-${sensor.status}`}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.2, delay: index * 0.01 }}
              style={{
                backgroundColor: `${getAnomalyColor(sensor.anomalyRate)}15`,
                borderColor: getAnomalyColor(sensor.anomalyRate)
              }}
            >
              <div className="sensor-header">
                <span className="sensor-name">{sensor.name}</span>
                {sensor.status === 'critical' && <AlertTriangle size={14} />}
              </div>
              <div className="sensor-rate">{sensor.anomalyRate.toFixed(1)}%</div>
              <div className="sensor-status">{getStatusText(sensor.status)}</div>
              {viewMode === 'list' && (
                <div className="sensor-stage">Stage {sensor.stage}</div>
              )}
            </motion.div>
          ))
        )}
      </div>

      {/* Legend */}
      <div className="heatmap-legend">
        <span className="legend-title">Status:</span>
        <div className="legend-items">
          <div className="legend-item">
            <div className="legend-color" style={{ background: '#10b981' }}></div>
            <span>Normal (&lt;5%)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ background: '#3b82f6' }}></div>
            <span>Monitor (5-15%)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ background: '#f59e0b' }}></div>
            <span>Warning (15-30%)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ background: '#f43f5e' }}></div>
            <span>Critical (&gt;30%)</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default SensorHeatmap;
