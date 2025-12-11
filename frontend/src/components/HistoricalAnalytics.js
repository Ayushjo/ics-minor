import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, BarChart2, Clock } from 'lucide-react';
import './HistoricalAnalytics.css';

function HistoricalAnalytics({ socket }) {
  const [statistics, setStatistics] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchAnalytics = async () => {
    try {
      // Fetch statistics
      const statsResponse = await fetch('http://localhost:5000/api/analytics/statistics');
      const statsData = await statsResponse.json();
      if (statsData.status === 'success' && statsData.statistics) {
        setStatistics(statsData.statistics);
      }

      // Fetch timeline
      const timelineResponse = await fetch('http://localhost:5000/api/analytics/timeline?minutes=60');
      const timelineData = await timelineResponse.json();
      if (timelineData.status === 'success') {
        setTimeline(timelineData.timeline);
      }

      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card analytics-container">
        <h3>Historical Analytics</h3>
        <div className="analytics-loading">Loading analytics data...</div>
      </div>
    );
  }

  if (!statistics) {
    return (
      <div className="card analytics-container">
        <h3>Historical Analytics</h3>
        <div className="analytics-empty">No historical data available. Start simulation to collect data.</div>
      </div>
    );
  }

  return (
    <motion.div
      className="card analytics-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="analytics-header">
        <h3>Historical Analytics</h3>
        <div className="session-info">
          <Clock size={16} />
          <span>Session: {statistics.session_duration_minutes.toFixed(1)} min</span>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="analytics-summary">
        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'var(--accent-blue-dim)', color: 'var(--accent-blue)' }}>
            <BarChart2 size={20} />
          </div>
          <div className="summary-content">
            <span className="summary-label">Total Batches</span>
            <span className="summary-value">{statistics.total_batches_processed}</span>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'var(--accent-rose-dim)', color: 'var(--accent-rose)' }}>
            <TrendingUp size={20} />
          </div>
          <div className="summary-content">
            <span className="summary-label">Avg Anomaly Rate</span>
            <span className="summary-value">{statistics.avg_anomaly_rate.toFixed(1)}%</span>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'var(--accent-amber-dim)', color: 'var(--accent-amber)' }}>
            <TrendingUp size={20} />
          </div>
          <div className="summary-content">
            <span className="summary-label">Avg Cyber Risk</span>
            <span className="summary-value">{statistics.avg_cyber_risk.toFixed(1)}%</span>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'var(--accent-emerald-dim)', color: 'var(--accent-emerald)' }}>
            <TrendingUp size={20} />
          </div>
          <div className="summary-content">
            <span className="summary-label">Avg Op. Risk</span>
            <span className="summary-value">{statistics.avg_operational_risk.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Risk Trend Chart */}
      {timeline.length > 0 && (
        <div className="analytics-chart-section">
          <h4>Risk Trends (Last Hour)</h4>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={timeline}>
              <defs>
                <linearGradient id="gradCyber" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="gradOps" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" vertical={false} />
              <XAxis
                dataKey="timestamp"
                stroke="rgba(255, 255, 255, 0.3)"
                style={{ fontSize: '0.7rem' }}
                tickFormatter={(value) => new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              />
              <YAxis stroke="rgba(255, 255, 255, 0.3)" style={{ fontSize: '0.7rem' }} />
              <Tooltip
                contentStyle={{
                  background: 'rgba(10, 10, 10, 0.95)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  padding: '12px'
                }}
                labelFormatter={(value) => new Date(value).toLocaleTimeString()}
              />
              <Area
                type="monotone"
                dataKey="cyber_risk_score"
                stroke="#f59e0b"
                strokeWidth={2}
                fill="url(#gradCyber)"
                name="Cyber Risk"
              />
              <Area
                type="monotone"
                dataKey="operational_risk_score"
                stroke="#10b981"
                strokeWidth={2}
                fill="url(#gradOps)"
                name="Operational Risk"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Threat Distribution */}
      {statistics.threat_distribution && Object.keys(statistics.threat_distribution).length > 0 && (
        <div className="analytics-chart-section">
          <h4>Threat Distribution</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={Object.entries(statistics.threat_distribution).map(([key, value]) => ({ name: key, count: value }))}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
              <XAxis
                dataKey="name"
                stroke="rgba(255, 255, 255, 0.3)"
                style={{ fontSize: '0.65rem' }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis stroke="rgba(255, 255, 255, 0.3)" style={{ fontSize: '0.7rem' }} />
              <Tooltip
                contentStyle={{
                  background: 'rgba(10, 10, 10, 0.95)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px'
                }}
              />
              <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Key Metrics */}
      <div className="analytics-metrics">
        <div className="metric-row">
          <span className="metric-label">Total Anomalies Detected:</span>
          <span className="metric-value">{statistics.total_anomalies_detected}</span>
        </div>
        <div className="metric-row">
          <span className="metric-label">Maximum Cyber Risk:</span>
          <span className="metric-value metric-value-high">{statistics.max_cyber_risk.toFixed(1)}%</span>
        </div>
        <div className="metric-row">
          <span className="metric-label">Maximum Operational Risk:</span>
          <span className="metric-value metric-value-high">{statistics.max_operational_risk.toFixed(1)}%</span>
        </div>
      </div>
    </motion.div>
  );
}

export default HistoricalAnalytics;
