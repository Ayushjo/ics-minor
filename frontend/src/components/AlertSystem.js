import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, XCircle, AlertTriangle, AlertCircle, CheckCircle2, X } from 'lucide-react';
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

    // Cyber risk alerts with detailed threat information
    const cyberScore = results.cyber_risk.score;
    const cyberLevel = results.cyber_risk.level;
    const attackProb = results.cyber_risk.avg_attack_probability || 0;
    const maxAttackProb = results.cyber_risk.max_attack_probability || 0;

    if (cyberScore >= 70) {
      alerts.push({
        id: `cyber-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'critical',
        type: 'Cyber Security',
        message: `Potential ${results.cyber_risk.attack_signature || 'cyber attack'} - ${cyberLevel} threat level`,
        value: `${cyberScore.toFixed(1)}%`,
        details: {
          'Attack Probability': `${(maxAttackProb * 100).toFixed(1)}%`,
          'Threat Type': results.cyber_risk.threat_assessment || 'Unknown'
        }
      });
    } else if (cyberScore >= 40) {
      alerts.push({
        id: `cyber-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'high',
        type: 'Cyber Security',
        message: `Elevated cyber threat detected - ${results.cyber_risk.attack_signature || 'monitoring required'}`,
        value: `${cyberScore.toFixed(1)}%`,
        details: {
          'Risk Level': cyberLevel,
          'Attack Probability': `${(attackProb * 100).toFixed(1)}%`
        }
      });
    } else if (cyberScore >= 20) {
      alerts.push({
        id: `cyber-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'medium',
        type: 'Cyber Security',
        message: `Moderate cyber activity - ${cyberLevel} level`,
        value: `${cyberScore.toFixed(1)}%`,
        details: {
          'Status': 'Under Monitoring'
        }
      });
    }

    // Operational risk alerts with affected systems
    const opsScore = results.operational_risk.score;
    const opsLevel = results.operational_risk.level;
    const affectedSystems = results.operational_risk.affected_systems || [];
    const faultSeverity = results.operational_risk.fault_severity || 'Unknown';
    const downtime = results.operational_risk.estimated_downtime || 0;

    if (opsScore >= 70) {
      alerts.push({
        id: `ops-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'critical',
        type: 'System Operations',
        message: `Critical operational issue - ${faultSeverity} severity affecting ${affectedSystems.length} systems`,
        value: `${opsScore.toFixed(1)}%`,
        details: {
          'Affected Systems': affectedSystems.slice(0, 3).join(', ') || 'Multiple',
          'Est. Downtime': `${downtime} min`,
          'Safety Impact': results.operational_risk.safety_impact || 'Evaluating'
        }
      });
    } else if (opsScore >= 40) {
      alerts.push({
        id: `ops-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'high',
        type: 'System Operations',
        message: `Operational degradation detected - ${affectedSystems.length || 'multiple'} systems affected`,
        value: `${opsScore.toFixed(1)}%`,
        details: {
          'Systems': affectedSystems.slice(0, 2).join(', ') || 'Check dashboard',
          'Severity': faultSeverity
        }
      });
    } else if (opsScore >= 20) {
      alerts.push({
        id: `ops-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'medium',
        type: 'System Operations',
        message: `Minor operational issues - ${opsLevel} level`,
        value: `${opsScore.toFixed(1)}%`,
        details: {
          'Impact': 'Low',
          'Status': 'Monitoring'
        }
      });
    }

    // Anomaly alerts with detailed sensor information
    const anomalyRate = results.detection.anomaly_rate;
    const numAnomalies = results.detection.num_anomalies;
    const batchSize = results.batch_info?.total_samples || 0;

    if (anomalyRate >= 0.30) {
      alerts.push({
        id: `anomaly-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'critical',
        type: 'Sensor Anomalies',
        message: `${numAnomalies} sensors showing critical anomalies out of ${batchSize} total readings`,
        value: `${(anomalyRate * 100).toFixed(1)}%`,
        details: {
          'Anomalous Sensors': `${numAnomalies}`,
          'Total Readings': `${batchSize}`,
          'Action': 'Immediate Investigation Required'
        }
      });
    } else if (anomalyRate >= 0.15) {
      alerts.push({
        id: `anomaly-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'high',
        type: 'Sensor Anomalies',
        message: `${numAnomalies} sensors deviating from normal behavior in current batch`,
        value: `${(anomalyRate * 100).toFixed(1)}%`,
        details: {
          'Flagged Sensors': `${numAnomalies}/${batchSize}`,
          'Recommendation': 'Check sensor heatmap for details'
        }
      });
    } else if (anomalyRate >= 0.05) {
      alerts.push({
        id: `anomaly-${Date.now()}-${Math.random()}`,
        timestamp,
        severity: 'medium',
        type: 'Sensor Anomalies',
        message: `${numAnomalies} sensor readings showing unusual patterns`,
        value: `${(anomalyRate * 100).toFixed(1)}%`,
        details: {
          'Sensors': `${numAnomalies} flagged`,
          'Status': 'Within acceptable range'
        }
      });
    }

    return alerts;
  };

  const getSeverityConfig = (severity) => {
    switch (severity) {
      case 'critical':
        return {
          icon: <XCircle size={20} />,
          color: 'rose',
          label: 'Critical'
        };
      case 'high':
        return {
          icon: <AlertTriangle size={20} />,
          color: 'amber',
          label: 'High'
        };
      case 'medium':
        return {
          icon: <AlertCircle size={20} />,
          color: 'blue',
          label: 'Medium'
        };
      default:
        return {
          icon: <AlertCircle size={20} />,
          color: 'blue',
          label: 'Info'
        };
    }
  };

  const acknowledgeAlert = (alertId) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const clearAll = () => {
    setAlerts([]);
  };

  // Ensure we always have a stable reference to displayed alerts
  const displayedAlerts = React.useMemo(() => {
    if (alerts.length === 0) return [];
    return showAll ? alerts : alerts.slice(0, 5);
  }, [alerts, showAll]);

  const criticalCount = alerts.filter(a => a.severity === 'critical').length;
  const highCount = alerts.filter(a => a.severity === 'high').length;

  return (
    <motion.div
      className="alert-system-modern"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="alert-system-header">
        <div className="header-content">
          <div className="header-icon-wrapper">
            <Bell size={24} />
          </div>
          <div className="header-text">
            <h3>Real-Time Alert Monitor</h3>
            <p className="header-subtitle">System Health & Security Notifications</p>
          </div>
        </div>
        <div className="header-badges">
          {criticalCount > 0 && (
            <div className="status-badge badge-critical">
              <span className="badge-count">{criticalCount}</span>
              <span>Critical</span>
            </div>
          )}
          {highCount > 0 && (
            <div className="status-badge badge-high">
              <span className="badge-count">{highCount}</span>
              <span>High</span>
            </div>
          )}
          {alerts.length === 0 && (
            <div className="status-badge badge-normal">
              <CheckCircle2 size={16} />
              <span>All Clear</span>
            </div>
          )}
        </div>
      </div>

      {/* Alert List */}
      <div className="alert-list-modern">
        {alerts.length === 0 ? (
          <div className="alert-empty-state">
            <CheckCircle2 size={48} />
            <h4>No Active Alerts</h4>
            <p>System operating within normal parameters</p>
          </div>
        ) : (
          <>
            <div className="alerts-container">
              <AnimatePresence mode="popLayout">
                {displayedAlerts.map((alert, index) => {
                  const config = getSeverityConfig(alert.severity);
                  return (
                    <motion.div
                      key={alert.id}
                      className={`alert-card-compact alert-card-${config.color}`}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ duration: 0.2 }}
                      layout
                    >
                      <div className="alert-compact-content">
                        <div className="alert-compact-icon">{config.icon}</div>

                        <div className="alert-compact-main">
                          <div className="alert-compact-top">
                            <span className="alert-compact-type">{alert.type}</span>
                            <span className="alert-compact-severity">{config.label}</span>
                          </div>
                          <div className="alert-compact-message">{alert.message}</div>
                          {alert.details && Object.keys(alert.details).length > 0 && (
                            <div className="alert-compact-details">
                              {Object.entries(alert.details).map(([key, value]) => (
                                value && (
                                  <span key={key} className="detail-inline">
                                    {key}: <strong>{value}</strong>
                                  </span>
                                )
                              ))}
                            </div>
                          )}
                        </div>

                        <div className="alert-compact-value">{alert.value}</div>

                        <button
                          className="alert-compact-close"
                          onClick={() => acknowledgeAlert(alert.id)}
                          title="Acknowledge"
                        >
                          <X size={16} />
                        </button>
                      </div>

                      <div className="alert-compact-time">
                        {new Date(alert.timestamp).toLocaleTimeString()}
                      </div>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>

            {/* Footer Actions */}
            <div className="alert-footer-actions">
              {alerts.length > 5 && (
                <button
                  className="btn-action btn-show-all"
                  onClick={() => setShowAll(!showAll)}
                >
                  {showAll ? 'Show Less' : `Show All (${alerts.length})`}
                </button>
              )}
              {alerts.length > 0 && (
                <button
                  className="btn-action btn-clear-all"
                  onClick={clearAll}
                >
                  <X size={16} />
                  Clear All
                </button>
              )}
            </div>
          </>
        )}
      </div>
    </motion.div>
  );
}

export default AlertSystem;
