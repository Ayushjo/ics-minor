import React from 'react';
import './ControlPanel.css';

function ControlPanel({ connected, simulationRunning, onStart, onStop, onReset }) {
  return (
    <div className="card control-panel">
      <h2>Control Panel</h2>
      <div className="control-buttons">
        <button
          className="btn btn-success"
          onClick={onStart}
          disabled={!connected || simulationRunning}
        >
          Start Simulation
        </button>
        <button
          className="btn btn-danger"
          onClick={onStop}
          disabled={!connected || !simulationRunning}
        >
          Stop Simulation
        </button>
        <button
          className="btn btn-secondary"
          onClick={onReset}
          disabled={!connected}
        >
          Reset
        </button>
      </div>
      <div className="control-info">
        <p>
          <strong>Batch Size:</strong> 50 samples | <strong>Interval:</strong> 3 seconds
        </p>
      </div>
    </div>
  );
}

export default ControlPanel;
