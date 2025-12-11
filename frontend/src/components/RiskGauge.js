import React from 'react';
import { motion } from 'framer-motion';
import { Shield, AlertTriangle } from 'lucide-react';
import './RiskGauge.css';

function CircularProgress({ value, size = 120, strokeWidth = 8, color }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (value / 100) * circumference;

  return (
    <svg width={size} height={size} className="circular-progress">
      {/* Background circle */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke="rgba(255, 255, 255, 0.05)"
        strokeWidth={strokeWidth}
      />
      {/* Progress circle */}
      <motion.circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        initial={{ strokeDashoffset: circumference }}
        animate={{ strokeDashoffset: offset }}
        transition={{ duration: 1, ease: 'easeOut' }}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dy="0.3em"
        className="progress-text"
        fill={color}
      >
        {value.toFixed(0)}
      </text>
    </svg>
  );
}

function RiskGauge({ cyberRisk, operationalRisk }) {
  if (!cyberRisk || !operationalRisk) return null;

  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'critical':
        return '#f43f5e';
      case 'high':
        return '#f59e0b';
      case 'medium':
        return '#f59e0b';
      case 'low':
        return '#10b981';
      default:
        return '#6b7280';
    }
  };

  return (
    <motion.div
      className="card risk-gauge-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
    >
      <div className="risk-header">
        <h3>Risk Assessment</h3>
        <span className="risk-subtitle">System Risk Analysis</span>
      </div>

      <div className="risk-gauges">
        {/* Cyber Risk */}
        <div className="risk-item">
          <div className="risk-icon-header">
            <Shield size={20} />
            <h4>Cyber Risk</h4>
          </div>

          <div className="gauge-wrapper">
            <CircularProgress
              value={cyberRisk.score || 0}
              color={getRiskColor(cyberRisk.level)}
            />
          </div>

          <div className="risk-details">
            <div className="risk-level-badge" style={{ background: `${getRiskColor(cyberRisk.level)}20`, color: getRiskColor(cyberRisk.level) }}>
              {cyberRisk.level}
            </div>
            <div className="risk-info">
              <span className="info-label">Affected Systems</span>
              <span className="info-value">{cyberRisk.affected_systems?.length || 0}</span>
            </div>
          </div>
        </div>

        {/* Operational Risk */}
        <div className="risk-item">
          <div className="risk-icon-header">
            <AlertTriangle size={20} />
            <h4>Operational Risk</h4>
          </div>

          <div className="gauge-wrapper">
            <CircularProgress
              value={operationalRisk.score || 0}
              color={getRiskColor(operationalRisk.level)}
            />
          </div>

          <div className="risk-details">
            <div className="risk-level-badge" style={{ background: `${getRiskColor(operationalRisk.level)}20`, color: getRiskColor(operationalRisk.level) }}>
              {operationalRisk.level}
            </div>
            <div className="risk-info">
              <span className="info-label">Downtime Est.</span>
              <span className="info-value">{operationalRisk.downtime_estimate || 'N/A'}</span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default RiskGauge;
