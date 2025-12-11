import React from 'react';
import './DetectionResults.css';

function DetectionResults({ detection, batchInfo }) {
  if (!detection || !batchInfo) return null;

  const anomalyPercentage = (batchInfo.anomaly_rate * 100).toFixed(1);

  return (
    <div className="card detection-results">
      <h2>Detection Results</h2>

      <div className="metric-grid">
        <div className="metric-item">
          <div className="metric-label">Total Samples</div>
          <div className="metric-value">{batchInfo.total_samples}</div>
        </div>
        <div className="metric-item">
          <div className="metric-label">Anomalies Detected</div>
          <div className="metric-value metric-danger">{batchInfo.anomalies_detected}</div>
        </div>
        <div className="metric-item">
          <div className="metric-label">Anomaly Rate</div>
          <div className="metric-value">{anomalyPercentage}%</div>
        </div>
      </div>

      <div className="detection-bar">
        <div
          className="detection-bar-fill"
          style={{ width: `${anomalyPercentage}%` }}
        ></div>
      </div>

      <div className="detection-stats">
        <p>
          <strong>Average Confidence:</strong> {(detection.confidence?.slice(0, 10).reduce((a, b) => a + b, 0) / Math.min(10, detection.confidence?.length || 1) * 100).toFixed(1)}%
        </p>
      </div>
    </div>
  );
}

export default DetectionResults;
