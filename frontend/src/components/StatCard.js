import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import './StatCard.css';

function StatCard({ title, value, unit, trend, trendValue, icon: Icon, color = 'blue' }) {
  const getTrendIcon = () => {
    if (trend === 'up') return <TrendingUp size={14} />;
    if (trend === 'down') return <TrendingDown size={14} />;
    return <Minus size={14} />;
  };

  const getTrendClass = () => {
    if (trend === 'up') return 'trend-up';
    if (trend === 'down') return 'trend-down';
    return 'trend-neutral';
  };

  return (
    <motion.div
      className="stat-card card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -4 }}
    >
      <div className="stat-header">
        <span className="stat-label">{title}</span>
        {Icon && (
          <div className={`stat-icon stat-icon-${color}`}>
            <Icon size={16} />
          </div>
        )}
      </div>

      <div className="stat-value-container">
        <motion.div
          className="stat-value"
          key={value}
          initial={{ scale: 1.2, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
        >
          {value}
          {unit && <span className="stat-unit">{unit}</span>}
        </motion.div>
      </div>

      {trendValue && (
        <div className={`stat-trend ${getTrendClass()}`}>
          {getTrendIcon()}
          <span>{trendValue}</span>
        </div>
      )}
    </motion.div>
  );
}

export default StatCard;
