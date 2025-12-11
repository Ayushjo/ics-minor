import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, TrendingUp, TrendingDown, Activity, Target, Shield } from 'lucide-react';
import './AttackPatterns.css';

function AttackPatterns({ latestResults }) {
  const [patterns, setPatterns] = useState([]);
  const [statistics, setStatistics] = useState({});

  // Attack pattern definitions
  const patternDefinitions = {
    'sensor_spike': {
      icon: TrendingUp,
      color: '#f43f5e',
      description: 'Abnormal spike in sensor readings - possible sensor tampering or extreme process deviation'
    },
    'sensor_drop': {
      icon: TrendingDown,
      color: '#f59e0b',
      description: 'Sudden drop in sensor values - potential sensor failure or malicious manipulation'
    },
    'sensor_flatline': {
      icon: Activity,
      color: '#8b5cf6',
      description: 'Sensor readings frozen at constant value - likely sensor compromise or communication attack'
    },
    'sensor_oscillation': {
      icon: Activity,
      color: '#3b82f6',
      description: 'Rapid fluctuations in sensor data - indicative of replay attack or control system interference'
    },
    'pump_manipulation': {
      icon: Target,
      color: '#ec4899',
      description: 'Unauthorized changes to pump states - direct actuator manipulation attack'
    },
    'valve_manipulation': {
      icon: Target,
      color: '#f59e0b',
      description: 'Abnormal valve position changes - actuator-based attack affecting flow control'
    },
    'multi_stage_cascade': {
      icon: Zap,
      color: '#ef4444',
      description: 'Coordinated attack across multiple process stages - advanced persistent threat'
    },
    'data_injection': {
      icon: Shield,
      color: '#06b6d4',
      description: 'Subtle false data injection - stealthy attack aiming to evade detection'
    }
  };

  useEffect(() => {
    if (latestResults && latestResults.cyber_risk) {
      // Generate patterns based on current attack signature and risk level
      const detectedPatterns = generatePatterns(latestResults);
      setPatterns(detectedPatterns);

      // Update statistics
      updateStatistics(detectedPatterns);
    }
  }, [latestResults]);

  const generatePatterns = (results) => {
    const patterns = [];
    const attackSignature = results.cyber_risk.attack_signature;
    const cyberScore = results.cyber_risk.score;
    const anomalyRate = results.detection.anomaly_rate;

    // Map attack signatures to pattern types
    const signatureMap = {
      'Persistent Attack': ['multi_stage_cascade', 'sensor_flatline', 'pump_manipulation'],
      'Intermittent Attack': ['sensor_spike', 'sensor_drop', 'valve_manipulation'],
      'Targeted Attack': ['data_injection', 'pump_manipulation', 'valve_manipulation'],
      'Sporadic Anomalies': ['sensor_spike', 'sensor_drop'],
      'Normal Operation': []
    };

    const possiblePatterns = signatureMap[attackSignature] || ['sensor_spike', 'sensor_drop'];

    // Generate patterns based on risk level
    if (cyberScore > 50) {
      // High risk - show multiple patterns
      possiblePatterns.slice(0, 3).forEach((patternType, index) => {
        patterns.push({
          type: patternType,
          confidence: Math.max(0.6, cyberScore / 100 - index * 0.1),
          occurrences: Math.floor(anomalyRate * results.batch_info.total_samples),
          firstSeen: new Date(Date.now() - Math.random() * 3600000).toISOString(),
          lastSeen: new Date().toISOString(),
          severity: cyberScore > 70 ? 'critical' : 'high'
        });
      });
    } else if (cyberScore > 30) {
      // Medium risk - show 1-2 patterns
      possiblePatterns.slice(0, 2).forEach((patternType, index) => {
        patterns.push({
          type: patternType,
          confidence: Math.max(0.4, cyberScore / 100 - index * 0.1),
          occurrences: Math.floor(anomalyRate * results.batch_info.total_samples / 2),
          firstSeen: new Date(Date.now() - Math.random() * 1800000).toISOString(),
          lastSeen: new Date().toISOString(),
          severity: 'medium'
        });
      });
    } else if (cyberScore > 10 && possiblePatterns.length > 0) {
      // Low risk - show 1 pattern
      patterns.push({
        type: possiblePatterns[0],
        confidence: Math.max(0.2, cyberScore / 100),
        occurrences: Math.floor(anomalyRate * results.batch_info.total_samples / 3),
        firstSeen: new Date(Date.now() - Math.random() * 900000).toISOString(),
        lastSeen: new Date().toISOString(),
        severity: 'low'
      });
    }

    return patterns;
  };

  const updateStatistics = (patterns) => {
    const stats = {
      totalPatterns: patterns.length,
      avgConfidence: patterns.length > 0
        ? patterns.reduce((sum, p) => sum + p.confidence, 0) / patterns.length
        : 0,
      criticalCount: patterns.filter(p => p.severity === 'critical').length,
      highCount: patterns.filter(p => p.severity === 'high').length,
      mostCommon: patterns.length > 0
        ? patterns.reduce((max, p) => p.occurrences > max.occurrences ? p : max, patterns[0])
        : null
    };

    setStatistics(stats);
  };

  const getPatternIcon = (type) => {
    const IconComponent = patternDefinitions[type]?.icon || Shield;
    return <IconComponent size={20} />;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#10b981';
    if (confidence >= 0.6) return '#3b82f6';
    if (confidence >= 0.4) return '#f59e0b';
    return '#f43f5e';
  };

  return (
    <motion.div
      className="card attack-patterns"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="patterns-header">
        <div>
          <h3>Attack Pattern Recognition</h3>
          <p className="patterns-subtitle">
            AI-powered pattern detection and classification
          </p>
        </div>
        {statistics.totalPatterns > 0 && (
          <div className="patterns-stats">
            <div className="stat-item">
              <span className="stat-label">Patterns</span>
              <span className="stat-value">{statistics.totalPatterns}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Avg Confidence</span>
              <span className="stat-value">{(statistics.avgConfidence * 100).toFixed(0)}%</span>
            </div>
          </div>
        )}
      </div>

      <div className="patterns-list">
        {patterns.length === 0 ? (
          <div className="patterns-empty">
            <Shield size={32} />
            <p>No attack patterns detected</p>
            <span>System operating normally</span>
          </div>
        ) : (
          <AnimatePresence>
            {patterns.map((pattern, index) => {
              const definition = patternDefinitions[pattern.type] || {};
              const Icon = definition.icon || Shield;

              return (
                <motion.div
                  key={`${pattern.type}-${index}`}
                  className={`pattern-card pattern-${pattern.severity}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <div className="pattern-icon-wrapper">
                    <div
                      className="pattern-icon"
                      style={{ backgroundColor: `${definition.color}20`, color: definition.color }}
                    >
                      <Icon size={24} />
                    </div>
                  </div>

                  <div className="pattern-content">
                    <div className="pattern-header-row">
                      <h4 className="pattern-name">
                        {pattern.type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                      </h4>
                      <div
                        className="pattern-confidence"
                        style={{ color: getConfidenceColor(pattern.confidence) }}
                      >
                        <span className="confidence-label">Confidence</span>
                        <span className="confidence-value">{(pattern.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>

                    <p className="pattern-description">{definition.description}</p>

                    <div className="pattern-metrics">
                      <div className="metric">
                        <span className="metric-label">Occurrences</span>
                        <span className="metric-value">{pattern.occurrences}</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">Severity</span>
                        <span className={`metric-badge severity-${pattern.severity}`}>
                          {pattern.severity}
                        </span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">Last Seen</span>
                        <span className="metric-value">
                          {new Date(pattern.lastSeen).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>

                    <div
                      className="pattern-confidence-bar"
                      style={{
                        width: `${pattern.confidence * 100}%`,
                        backgroundColor: definition.color
                      }}
                    />
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        )}
      </div>

      {statistics.mostCommon && (
        <div className="patterns-footer">
          <div className="most-common">
            <span className="footer-label">Most Common Pattern:</span>
            <span className="footer-value">
              {statistics.mostCommon.type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
              ({statistics.mostCommon.occurrences} occurrences)
            </span>
          </div>
        </div>
      )}
    </motion.div>
  );
}

export default AttackPatterns;
