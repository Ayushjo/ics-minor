import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Clock, CheckCircle2, Users, ShieldAlert, Target } from 'lucide-react';
import './Decisions.css';

function Decisions({ decisions }) {
  if (!decisions) return null;

  const getPriorityConfig = (priority) => {
    switch (priority) {
      case 'immediate':
        return {
          icon: <Zap size={20} />,
          label: 'Immediate Actions',
          color: 'rose',
          description: 'Critical - Execute Now'
        };
      case 'short_term':
        return {
          icon: <Clock size={20} />,
          label: 'Short-term Actions',
          color: 'amber',
          description: 'Execute within hours'
        };
      case 'ongoing':
        return {
          icon: <CheckCircle2 size={20} />,
          label: 'Ongoing Monitoring',
          color: 'blue',
          description: 'Continuous oversight'
        };
      default:
        return {
          icon: <CheckCircle2 size={20} />,
          label: 'Actions',
          color: 'blue',
          description: ''
        };
    }
  };

  const actionsByPriority = {
    immediate: decisions.action_priority?.immediate || [],
    short_term: decisions.action_priority?.short_term || [],
    ongoing: decisions.action_priority?.ongoing || []
  };

  return (
    <motion.div
      className="decisions-modern-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
    >
      {/* Header Section */}
      <div className="decisions-modern-header">
        <div className="header-left">
          <div className="header-icon">
            <Target size={24} />
          </div>
          <div>
            <h3>Automated Response System</h3>
            <p className="header-subtitle">AI-Generated Action Plan</p>
          </div>
        </div>
        <div className="header-badge">
          <ShieldAlert size={16} />
          <span>{decisions.requires_human_approval ? 'Approval Required' : 'Auto-Executing'}</span>
        </div>
      </div>

      {/* Threat Overview Card */}
      <div className="threat-overview-card">
        <div className="overview-item">
          <span className="overview-label">Primary Threat</span>
          <span className="overview-value threat-text">{decisions.primary_threat}</span>
        </div>
        <div className="overview-divider"></div>
        <div className="overview-item">
          <span className="overview-label">Response Timeline</span>
          <span className="overview-value timeline-text">{decisions.response_timeline}</span>
        </div>
      </div>

      {/* Action Priority Groups */}
      <div className="priority-groups">
        {Object.entries(actionsByPriority).map(([priority, actions]) => {
          if (actions.length === 0) return null;
          const config = getPriorityConfig(priority);

          return (
            <motion.div
              key={priority}
              className={`priority-group priority-${config.color}`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
            >
              <div className="priority-group-header">
                <div className="priority-icon">{config.icon}</div>
                <div className="priority-info">
                  <h4>{config.label}</h4>
                  <p>{config.description}</p>
                </div>
                <div className="priority-count">{actions.length}</div>
              </div>

              <div className="priority-actions">
                {actions.map((action, index) => (
                  <motion.div
                    key={index}
                    className="action-item"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.05 * index }}
                  >
                    <div className="action-number">{index + 1}</div>
                    <p className="action-text">{action}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Emergency Contacts */}
      {decisions.emergency_contacts?.length > 0 && (
        <motion.div
          className="emergency-contacts-card"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="emergency-contacts-header">
            <Users size={18} />
            <span>Emergency Response Team</span>
          </div>
          <div className="contacts-grid">
            {decisions.emergency_contacts.map((contact, index) => (
              <motion.div
                key={index}
                className="contact-card"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.05 * index }}
              >
                {contact}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

export default Decisions;
