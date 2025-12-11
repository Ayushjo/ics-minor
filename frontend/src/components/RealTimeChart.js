import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import './RealTimeChart.css';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="tooltip-time">{payload[0]?.payload?.timestamp}</p>
        {payload.map((entry, index) => (
          <div key={index} className="tooltip-entry">
            <span className="tooltip-dot" style={{ background: entry.color }}></span>
            <span className="tooltip-label">{entry.name}:</span>
            <span className="tooltip-value">{entry.value.toFixed(2)}%</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

function RealTimeChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="card chart-container">
        <div className="chart-header">
          <h3>Real-Time Monitoring</h3>
          <span className="chart-subtitle">Live System Metrics</span>
        </div>
        <div className="chart-empty">
          <p>No data available. Start simulation to see live metrics.</p>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className="card chart-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <div className="chart-header">
        <h3>Real-Time Monitoring</h3>
        <span className="chart-subtitle">Live System Metrics</span>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <AreaChart
          data={data}
          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorAnomalyRate" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorCyberRisk" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorOperationalRisk" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" vertical={false} />

          <XAxis
            dataKey="timestamp"
            stroke="rgba(255, 255, 255, 0.3)"
            style={{ fontSize: '0.75rem', fill: 'rgba(255, 255, 255, 0.5)' }}
            tickLine={false}
            axisLine={{ stroke: 'rgba(255, 255, 255, 0.1)' }}
          />

          <YAxis
            stroke="rgba(255, 255, 255, 0.3)"
            style={{ fontSize: '0.75rem', fill: 'rgba(255, 255, 255, 0.5)' }}
            tickLine={false}
            axisLine={{ stroke: 'rgba(255, 255, 255, 0.1)' }}
          />

          <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255, 255, 255, 0.1)', strokeWidth: 1 }} />

          <Area
            type="monotone"
            dataKey="anomalyRate"
            stroke="#f43f5e"
            strokeWidth={2}
            fill="url(#colorAnomalyRate)"
            name="Anomaly Rate"
            animationDuration={1000}
          />

          <Area
            type="monotone"
            dataKey="cyberRisk"
            stroke="#f59e0b"
            strokeWidth={2}
            fill="url(#colorCyberRisk)"
            name="Cyber Risk"
            animationDuration={1000}
          />

          <Area
            type="monotone"
            dataKey="operationalRisk"
            stroke="#3b82f6"
            strokeWidth={2}
            fill="url(#colorOperationalRisk)"
            name="Operational Risk"
            animationDuration={1000}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className="chart-legend-modern">
        <div className="legend-item-modern">
          <div className="legend-line" style={{ background: '#f43f5e' }}></div>
          <span>Anomaly Rate</span>
        </div>
        <div className="legend-item-modern">
          <div className="legend-line" style={{ background: '#f59e0b' }}></div>
          <span>Cyber Risk</span>
        </div>
        <div className="legend-item-modern">
          <div className="legend-line" style={{ background: '#3b82f6' }}></div>
          <span>Operational Risk</span>
        </div>
      </div>
    </motion.div>
  );
}

export default RealTimeChart;
