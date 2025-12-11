import React from 'react';
import { motion } from 'framer-motion';
import { Clock, AlertCircle, CheckCircle2, Users } from 'lucide-react';
import './Decisions.css';

function Decisions({ decisions }) {
  if (!decisions) return null;

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'immediate':
        return <AlertCircle size={16} />;
      case 'short_term':
        return <Clock size={16} />;
      case 'ongoing':
        return <CheckCircle2 size={16} />;
      default:
        return <CheckCircle2 size={16} />;
    }
  };

  const allActions = [
    ...(decisions.action_priority?.immediate?.map(a => ({ text: a, priority: 'immediate' })) || []),
    ...(decisions.action_priority?.short_term?.map(a => ({ text: a, priority: 'short_term' })) || []),
    ...(decisions.action_priority?.ongoing?.map(a => ({ text: a, priority: 'ongoing' })) || [])
  ];

  return (
    <motion.div
      className="card decisions-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
    >
      <div className="decisions-header-modern">
        <h3>Automated Decisions</h3>
        <span className="decisions-subtitle">Recommended Actions</span>
      </div>

      <div className="decision-meta">
        <div className="meta-item">
          <span className="meta-label">Primary Threat</span>
          <span className="meta-value threat-value">{decisions.primary_threat}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Timeline</span>
          <span className="meta-value timeline-value">{decisions.response_timeline}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Approval</span>
          <span className={`meta-value ${decisions.requires_human_approval ? 'approval-required-value' : 'approval-not-required-value'}`}>
            {decisions.requires_human_approval ? 'Required' : 'Automated'}
          </span>
        </div>
      </div>

      <div className="timeline-container">
        {allActions.map((action, index) => (
          <motion.div
            key={index}
            className={`timeline-item timeline-${action.priority}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 * index, duration: 0.3 }}
          >
            <div className="timeline-marker">
              {getPriorityIcon(action.priority)}
            </div>
            <div className="timeline-content">
              <div className="timeline-badge">
                {action.priority.replace('_', ' ')}
              </div>
              <p className="timeline-text">{action.text}</p>
            </div>
          </motion.div>
        ))}
      </div>

      {decisions.emergency_contacts?.length > 0 && (
        <div className="emergency-section">
          <div className="emergency-header">
            <Users size={16} />
            <span>Emergency Contacts</span>
          </div>
          <div className="contact-chips">
            {decisions.emergency_contacts.map((contact, index) => (
              <motion.span
                key={index}
                className="contact-chip"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.05 * index }}
              >
                {contact}
              </motion.span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

export default Decisions;
