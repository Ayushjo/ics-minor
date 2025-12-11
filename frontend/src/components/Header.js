import React from 'react';
import { Activity, Play, Square, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';
import './Header.css';

function Header({ connected, simulationRunning, onStart, onStop, onReset }) {
  return (
    <motion.header
      className="header glass"
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <Activity size={24} strokeWidth={2.5} />
            <h1>ICS Fault Detection</h1>
          </div>
          <div className="status-indicator">
            <div className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></div>
            <span className="status-text">
              {connected ? 'System Connected' : 'Disconnected'}
            </span>
          </div>
        </div>

        <div className="header-right">
          <div className="command-bar">
            <motion.button
              className="btn btn-primary"
              onClick={onStart}
              disabled={!connected || simulationRunning}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Play size={16} />
              Start
            </motion.button>
            <motion.button
              className="btn btn-danger"
              onClick={onStop}
              disabled={!connected || !simulationRunning}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Square size={16} />
              Stop
            </motion.button>
            <motion.button
              className="btn btn-secondary"
              onClick={onReset}
              disabled={!connected}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <RotateCcw size={16} />
              Reset
            </motion.button>
          </div>
        </div>
      </div>
    </motion.header>
  );
}

export default Header;
