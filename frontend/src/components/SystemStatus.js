import React from 'react';
import './SystemStatus.css';

function SystemStatus({ connected, systemState, simulationRunning }) {
  return (
    <div className="card system-status">
      <h2>System Status</h2>
      <div className="status-grid">
        <div className="status-item">
          <span className="status-label">Connection:</span>
          <span className={`status-value ${connected ? 'status-ok' : 'status-error'}`}>
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        <div className="status-item">
          <span className="status-label">System State:</span>
          <span className="status-value">{systemState}</span>
        </div>
        <div className="status-item">
          <span className="status-label">Simulation:</span>
          <span className={`status-value ${simulationRunning ? 'status-ok' : ''}`}>
            {simulationRunning ? 'Running' : 'Stopped'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default SystemStatus;
