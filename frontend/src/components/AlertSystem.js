import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, AlertCircle, Info, XCircle, Check } from 'lucide-react';
import './AlertSystem.css';

function AlertSystem({ socket, latestResults }) {
  const [alerts, setAlerts] = useState([]);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    // Generate alerts from latest results
    if (latestResults && latestResults.cyber_risk && latestResults.operational_risk) {
      const newAlerts = generateAlerts(latestResults);
      if (newAlerts.length > 0) {
        setAlerts(prev => [...newAlerts, ...prev].slice(0, 50)); // Keep last 50
      }
    }
  }, [latestResults]);

  const generateAlerts = (results) => {
    const alerts = [];
    const timestamp = new Date().toISOString();

    // Cyber risk alerts
    const cyberScore = results.cyber_risk.score;
    const cyberLevel = results.cyber_risk.level;

    if (cyberScore >= 70) {
      alerts.push({
        id: `cyber-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'critical',
        type: 'cyber_risk',
        message: `Critical cyber risk detected: ${cyberScore.toFixed(1)}%`,
        details: {
          level: cyberLevel,
          threat: results.cyber_risk.attack_signature
        }
      });
    } else if (cyberScore >= 50) {
      alerts.push({
        id: `cyber-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'high',
        type: 'cyber_risk',
        message: `High cyber risk: ${cyberScore.toFixed(1)}%`,
        details: {
          level: cyberLevel,
          threat: results.cyber_risk.attack_signature
        }
      });
    } else if (cyberScore >= 30) {
      alerts.push({
        id: `cyber-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'medium',
        type: 'cyber_risk',
        message: `Moderate cyber risk: ${cyberScore.toFixed(1)}%`,
        details: {
          level: cyberLevel
        }
      });
    }

    // Operational risk alerts
    const opsScore = results.operational_risk.score;
    const opsLevel = results.operational_risk.level;

    if (opsScore >= 70) {
      alerts.push({
        id: `ops-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'critical',
        type: 'operational_risk',
        message: `Critical operational risk: ${opsScore.toFixed(1)}%`,
        details: {
          level: opsLevel,
          affected: results.operational_risk.affected_systems?.join(', ')
        }
      });
    } else if (opsScore >= 50) {
      alerts.push({
        id: `ops-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'high',
        type: 'operational_risk',
        message: `High operational risk: ${opsScore.toFixed(1)}%`,
        details: {
          level: opsLevel
        }
      });
    }

    // Anomaly rate alerts
    const anomalyRate = results.detection.anomaly_rate * 100;

    if (anomalyRate >= 40) {
      alerts.push({
        id: `anomaly-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'critical',
        type: 'anomaly_detection',
        message: `Critical anomaly rate: ${anomalyRate.toFixed(1)}%`,
        details: {
          count: results.detection.num_anomalies
        }
      });
    } else if (anomalyRate >= 25) {
      alerts.push({
        id: `anomaly-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'high',
        type: 'anomaly_detection',
        message: `High anomaly rate: ${anomalyRate.toFixed(1)}%`,
        details: {
          count: results.detection.num_anomalies
        }
      });
    }

    return alerts;
  };

  const getAlertIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <XCircle size={18} />;
      case 'high':
        return <AlertTriangle size={18} />;
      case 'medium':
        return <AlertCircle size={18} />;
      default:
        return <Info size={18} />;
    }
  };

  const acknowledgeAlert = (alertId) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const clearAll = () => {
    setAlerts([]);
  };

  const displayedAlerts = showAll ? alerts : alerts.slice(0, 5);
  const criticalCount = alerts.filter(a => a.severity === 'critical').length;
  const highCount = alerts.filter(a => a.severity === 'high').length;

  return (
    <motion.div
      className="card alert-system"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="alert-header">
        <div className="alert-title-section">
          <h3>Real-Time Alerts</h3>
          <div className="alert-summary">
            {criticalCount > 0 && (
              <span className="alert-badge critical">{criticalCount} Critical</span>
            )}
            {highCount > 0 && (
              <span className="alert-badge high">{highCount} High</span>
            )}
            {alerts.length === 0 && (
              <span className="alert-badge normal">All Clear</span>
            )}
          </div>
        </div>
        {alerts.length > 0 && (
          <button className="btn-clear" onClick={clearAll}>
            Clear All
          </button>
        )}
      </div>

      <div className="alert-list">
        {alerts.length === 0 ? (
          <div className="alert-empty">
            <Check size={32} />
            <p>No active alerts</p>
            <span>System operating normally</span>
          </div>
        ) : (
          <AnimatePresence>
            {displayedAlerts.map((alert, index) => (
              <motion.div
                key={alert.id}
                className={`alert-item alert-${alert.severity}`}
                initial={{ opacity: 0, x: -20, height: 0 }}
                animate={{ opacity: 1, x: 0, height: 'auto' }}
                exit={{ opacity: 0, x: 20, height: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <div className="alert-icon">
                  {getAlertIcon(alert.severity)}
                </div>
                <div className="alert-content">
                  <div className="alert-message">{alert.message}</div>
                  <div className="alert-meta">
                    <span className="alert-type">{alert.type.replace(/_/g, ' ')}</span>
                    <span className="alert-time">
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  {alert.details && Object.keys(alert.details).length > 0 && (
                    <div className="alert-details">
                      {Object.entries(alert.details).map(([key, value]) => (
                        value && (
                          <span key={key}>
                            {key}: <strong>{value}</strong>
                          </span>
                        )
                      ))}
                    </div>
                  )}
                </div>
                <button
                  className="alert-dismiss"
                  onClick={() => acknowledgeAlert(alert.id)}
                  title="Acknowledge"
                >
                  ×
                </button>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>

      {alerts.length > 5 && (
        <button
          className="btn-show-more"
          onClick={() => setShowAll(!showAll)}
        >
          {showAll ? 'Show Less' : `Show All (${alerts.length})`}
        </button>
      )}
    </motion.div>
  );
}

export default AlertSystem;
