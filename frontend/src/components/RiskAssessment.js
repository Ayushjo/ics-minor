import React from 'react';
import './RiskAssessment.css';

function RiskAssessment({ cyberRisk, operationalRisk }) {
  if (!cyberRisk || !operationalRisk) return null;

  const getRiskColor = (level) => {
    const colors = {
      low: '#4caf50',
      medium: '#ff9800',
      high: '#ff5722',
      critical: '#f44336'
    };
    return colors[level.toLowerCase()] || '#757575';
  };

  return (
    <div className="card risk-assessment">
      <h2>Risk Assessment</h2>

      <div className="risk-section">
        <h3>Cyber Risk</h3>
        <div className="risk-level" style={{ borderColor: getRiskColor(cyberRisk.level) }}>
          <div className="risk-header">
            <span className="risk-label" style={{ color: getRiskColor(cyberRisk.level) }}>
              {cyberRisk.level.toUpperCase()}
            </span>
            <span className="risk-score">{(cyberRisk.score * 100).toFixed(1)}%</span>
          </div>
          <div className="risk-bar">
            <div
              className="risk-bar-fill"
              style={{
                width: `${cyberRisk.score * 100}%`,
                background: getRiskColor(cyberRisk.level)
              }}
            ></div>
          </div>
          <div className="risk-details">
            <p><strong>Attack Signature:</strong> {cyberRisk.attack_signature}</p>
            <p><strong>Threat Assessment:</strong> {cyberRisk.threat_assessment}</p>
          </div>
        </div>
      </div>

      <div className="risk-section">
        <h3>Operational Risk</h3>
        <div className="risk-level" style={{ borderColor: getRiskColor(operationalRisk.level) }}>
          <div className="risk-header">
            <span className="risk-label" style={{ color: getRiskColor(operationalRisk.level) }}>
              {operationalRisk.level.toUpperCase()}
            </span>
            <span className="risk-score">{(operationalRisk.score * 100).toFixed(1)}%</span>
          </div>
          <div className="risk-bar">
            <div
              className="risk-bar-fill"
              style={{
                width: `${operationalRisk.score * 100}%`,
                background: getRiskColor(operationalRisk.level)
              }}
            ></div>
          </div>
          <div className="risk-details">
            <p><strong>Fault Severity:</strong> {operationalRisk.fault_severity}</p>
            <p><strong>Affected Systems:</strong> {operationalRisk.affected_systems.join(', ')}</p>
            <p><strong>Est. Downtime:</strong> {operationalRisk.estimated_downtime} minutes</p>
            <p><strong>Safety Impact:</strong> {operationalRisk.safety_impact}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RiskAssessment;
