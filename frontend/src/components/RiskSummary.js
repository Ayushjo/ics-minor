import React from 'react';
import { AlertTriangle, Activity } from 'lucide-react';
import './RiskSummary.css';

function RiskSummary({ riskMapping }) {
  console.log('RiskSummary - riskMapping:', riskMapping);

  // Use sample data if no real data available
  const sampleData = {
    distribution: {
      'Pump Damage': 45.2,
      'Water Overflow': 28.6,
      'Process Interruption': 15.9,
      'Data Tampering': 10.3
    },
    majority_risk: {
      category: 'Pump Damage',
      percentage: 45.2,
      count: 14,
      affected_sensors: ['FIT-101', 'FIT-201', 'FIT-301', 'LIT-301', 'P-101', 'P-201'],
      affected_stages: ['P1', 'P2', 'P3']
    },
    risk_details: {
      'Pump Damage': {
        total: 14,
        unique_sensors: 6,
        sensors: [
          { id: 'FIT-101', count: 5 },
          { id: 'FIT-201', count: 4 },
          { id: 'FIT-301', count: 3 },
          { id: 'LIT-301', count: 1 },
          { id: 'P-101', count: 1 }
        ]
      },
      'Water Overflow': {
        total: 9,
        unique_sensors: 4,
        sensors: [
          { id: 'LIT-101', count: 4 },
          { id: 'LIT-301', count: 3 },
          { id: 'LIT-401', count: 2 }
        ]
      },
      'Process Interruption': {
        total: 5,
        unique_sensors: 3,
        sensors: [
          { id: 'MV-101', count: 2 },
          { id: 'P-101', count: 2 },
          { id: 'P-201', count: 1 }
        ]
      },
      'Data Tampering': {
        total: 3,
        unique_sensors: 3,
        sensors: [
          { id: 'AIT-201', count: 1 },
          { id: 'FIT-101', count: 1 },
          { id: 'LIT-101', count: 1 }
        ]
      }
    }
  };

  // Use real data if available, otherwise use sample data
  const dataToUse = (riskMapping && riskMapping.distribution) ? riskMapping : sampleData;
  const { majority_risk, risk_details } = dataToUse;
  console.log('RiskSummary - Rendering with data:', { majority_risk, risk_details });

  // Check if we have a dominant risk
  const hasMajorityRisk = majority_risk && majority_risk.category !== 'None' && majority_risk.percentage > 15;

  // Get active risks (those with occurrences)
  const activeRisks = Object.entries(risk_details || {})
    .filter(([_, details]) => details.total > 0)
    .sort((a, b) => b[1].total - a[1].total);

  if (activeRisks.length === 0) {
    return null; // No risks detected yet
  }

  return (
    <div className="risk-summary-container">
      <div className="risk-summary-header">
        <Activity size={24} />
        <h2>Sensor-to-Risk Analysis</h2>
        <p>Shows which sensor failures are causing which system risks</p>
      </div>

      {hasMajorityRisk && (
        <div className="majority-risk-alert">
          <AlertTriangle size={32} />
          <div className="majority-content">
            <h3>Primary Risk Detected: {majority_risk.category}</h3>
            <p>
              <strong>{majority_risk.percentage}%</strong> of detected issues fall into this category
              ({majority_risk.count} occurrences affecting {majority_risk.affected_sensors?.length || 0} sensors)
            </p>
            {majority_risk.affected_stages && majority_risk.affected_stages.length > 0 && (
              <p className="stages">Affected stages: {majority_risk.affected_stages.join(', ')}</p>
            )}
          </div>
        </div>
      )}

      <div className="risk-breakdown">
        <h3>Risk Breakdown by Type</h3>
        <div className="risk-cards">
          {activeRisks.map(([riskName, details]) => (
            <div key={riskName} className="risk-card">
              <div className="risk-card-header">
                <h4>{riskName}</h4>
                <span className="risk-count">{details.total}</span>
              </div>
              <div className="risk-card-body">
                <p><strong>{details.unique_sensors}</strong> sensors affected</p>
                {details.sensors && details.sensors.length > 0 && (
                  <div className="top-sensors">
                    <span className="label">Top sensors:</span>
                    {details.sensors.slice(0, 3).map((s, idx) => (
                      <span key={idx} className="sensor-badge">
                        {s.id} ({s.count})
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default RiskSummary;
