"""
Enhanced Features Module
Provides historical analytics, sensor analysis, attack pattern recognition, and alert system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import deque, defaultdict
import json

class HistoricalAnalytics:
    """Stores and analyzes historical data"""

    def __init__(self, max_history=1000):
        self.max_history = max_history
        self.history = deque(maxlen=max_history)
        self.session_start = datetime.now()

    def add_record(self, results, batch_data):
        """Add a new processing result to history"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'anomaly_rate': results['detection']['anomaly_rate'],
            'num_anomalies': results['detection']['num_anomalies'],
            'cyber_risk_score': results['cyber_risk']['score'],
            'cyber_risk_level': results['cyber_risk']['level'],
            'operational_risk_score': results['operational_risk']['score'],
            'operational_risk_level': results['operational_risk']['level'],
            'primary_threat': results['decisions']['primary_threat'],
            'batch_size': len(batch_data),
            'attack_type': batch_data['Attack_Type'].value_counts().to_dict() if 'Attack_Type' in batch_data.columns else {},
            'attack_severity': batch_data['Attack_Severity'].value_counts().to_dict() if 'Attack_Severity' in batch_data.columns else {},
            'affected_stages': batch_data['Affected_Stage'].value_counts().to_dict() if 'Affected_Stage' in batch_data.columns else {},
        }
        self.history.append(record)

    def get_history(self, limit=None):
        """Get historical records"""
        if limit:
            return list(self.history)[-limit:]
        return list(self.history)

    def get_statistics(self):
        """Get overall statistics"""
        if not self.history:
            return None

        df = pd.DataFrame(list(self.history))

        return {
            'session_duration_minutes': (datetime.now() - self.session_start).total_seconds() / 60,
            'total_batches_processed': len(self.history),
            'total_anomalies_detected': df['num_anomalies'].sum(),
            'avg_anomaly_rate': df['anomaly_rate'].mean(),
            'avg_cyber_risk': df['cyber_risk_score'].mean(),
            'avg_operational_risk': df['operational_risk_score'].mean(),
            'max_cyber_risk': df['cyber_risk_score'].max(),
            'max_operational_risk': df['operational_risk_score'].max(),
            'risk_trend': {
                'cyber': df['cyber_risk_score'].tolist()[-20:],
                'operational': df['operational_risk_score'].tolist()[-20:],
                'timestamps': df['timestamp'].tolist()[-20:]
            },
            'threat_distribution': df['primary_threat'].value_counts().to_dict(),
        }

    def get_timeline_data(self, minutes=30):
        """Get timeline data for charts (last N minutes)"""
        if not self.history:
            return []

        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        timeline = []

        for record in self.history:
            record_time = datetime.fromisoformat(record['timestamp'])
            if record_time >= cutoff_time:
                timeline.append(record)

        return timeline


class SensorAnalyzer:
    """Analyzes individual sensor behavior"""

    def __init__(self):
        self.sensor_stats = {}
        self.stage_map = {
            1: ['FIT101', 'LIT101', 'MV101', 'P101', 'P102'],
            2: ['AIT201', 'AIT202', 'AIT203', 'FIT201', 'MV201', 'P201', 'P202', 'P203', 'P204', 'P205', 'P206'],
            3: ['DPIT301', 'FIT301', 'LIT301', 'MV301', 'MV302', 'MV303', 'MV304', 'P301', 'P302'],
            4: ['AIT401', 'AIT402', 'FIT401', 'LIT401', 'P401', 'P402', 'P403', 'P404', 'UV401'],
            5: ['AIT501', 'AIT502', 'AIT503', 'AIT504', 'FIT501', 'FIT502', 'FIT503', 'FIT504', 'P501', 'P502', 'PIT501', 'PIT502', 'PIT503'],
            6: ['FIT601', 'P601', 'P602', 'P603']
        }

    def analyze_batch(self, batch_data, predictions):
        """Analyze sensor-level anomalies in a batch"""
        sensor_analysis = {
            'heatmap_data': [],
            'anomalous_sensors': [],
            'stage_summary': {},
            'critical_sensors': []
        }

        # Get sensor columns (exclude metadata)
        metadata_cols = ['Normal/Attack', 'Attack_Type', 'Attack_Severity', 'Affected_Stage',
                        'Num_Affected_Sensors', 'Timestamp', 'Unnamed: 0', 'index']
        sensor_cols = [col for col in batch_data.columns if col not in metadata_cols and not col.startswith('Unnamed')]

        # Calculate anomaly rate per sensor
        for sensor in sensor_cols:
            sensor_data = batch_data[sensor].values
            sensor_mean = sensor_data.mean()
            sensor_std = sensor_data.std()

            # Detect anomalies using Z-score
            z_scores = np.abs((sensor_data - sensor_mean) / (sensor_std + 1e-10))
            anomaly_count = np.sum(z_scores > 2.5)  # 2.5 sigma threshold
            anomaly_rate = (anomaly_count / len(sensor_data)) * 100

            # Get stage for this sensor (extract from sensor name)
            stage = 0
            try:
                # Extract stage number from sensor name (e.g., FIT-101 -> stage 1)
                stage_str = sensor.split('-')[1][:1] if '-' in sensor else '0'
                stage = int(stage_str) if stage_str.isdigit() else 0
            except:
                stage = 0

            sensor_info = {
                'sensor': sensor,
                'stage': stage,
                'anomaly_rate': float(anomaly_rate),
                'mean_value': float(sensor_mean),
                'std_value': float(sensor_std),
                'max_z_score': float(z_scores.max()),
                'status': 'critical' if anomaly_rate > 30 else 'warning' if anomaly_rate > 15 else 'normal'
            }

            sensor_analysis['heatmap_data'].append(sensor_info)

            if anomaly_rate > 15:
                sensor_analysis['anomalous_sensors'].append(sensor_info)

            if anomaly_rate > 30:
                sensor_analysis['critical_sensors'].append(sensor)

        # Summarize by stage
        for stage in range(1, 7):
            stage_sensors = [s for s in sensor_analysis['heatmap_data'] if s['stage'] == stage]
            if stage_sensors:
                avg_anomaly_rate = np.mean([s['anomaly_rate'] for s in stage_sensors])
                critical_count = len([s for s in stage_sensors if s['status'] == 'critical'])

                sensor_analysis['stage_summary'][f'Stage {stage}'] = {
                    'avg_anomaly_rate': float(avg_anomaly_rate),
                    'critical_sensors': critical_count,
                    'total_sensors': len(stage_sensors),
                    'status': 'critical' if critical_count > 2 else 'warning' if critical_count > 0 else 'normal'
                }

        # Sort heatmap data by anomaly rate
        sensor_analysis['heatmap_data'].sort(key=lambda x: x['anomaly_rate'], reverse=True)

        return sensor_analysis


class AttackPatternRecognizer:
    """Recognizes and classifies attack patterns"""

    def __init__(self):
        self.pattern_history = deque(maxlen=100)
        self.pattern_stats = defaultdict(int)

    def recognize_patterns(self, batch_data, sensor_analysis):
        """Recognize attack patterns in the current batch"""
        patterns = {
            'detected_patterns': [],
            'pattern_summary': {},
            'attack_timeline': [],
            'pattern_confidence': {}
        }

        if 'Attack_Type' in batch_data.columns:
            # Direct pattern detection from data
            attack_types = batch_data[batch_data['Normal/Attack'] == 1]['Attack_Type'].value_counts()

            for attack_type, count in attack_types.items():
                if attack_type != 'Normal':
                    # Get severity distribution for this attack type
                    attack_subset = batch_data[batch_data['Attack_Type'] == attack_type]
                    severities = attack_subset['Attack_Severity'].value_counts().to_dict()
                    affected_stages = attack_subset['Affected_Stage'].value_counts().to_dict()

                    pattern_info = {
                        'pattern_type': attack_type,
                        'occurrences': int(count),
                        'percentage': float((count / len(batch_data)) * 100),
                        'severity_distribution': severities,
                        'affected_stages': affected_stages,
                        'confidence': 0.95,  # High confidence since we have ground truth
                        'description': self._get_pattern_description(attack_type)
                    }

                    patterns['detected_patterns'].append(pattern_info)
                    self.pattern_stats[attack_type] += count

        # Heuristic-based pattern detection from sensor anomalies
        critical_sensors = sensor_analysis['critical_sensors']

        if len(critical_sensors) > 0:
            # Multiple sensors affected - possible coordinated attack
            if len(critical_sensors) >= 3:
                patterns['detected_patterns'].append({
                    'pattern_type': 'coordinated_attack',
                    'occurrences': len(critical_sensors),
                    'confidence': 0.85,
                    'affected_sensors': critical_sensors,
                    'description': 'Multiple sensors showing anomalous behavior simultaneously'
                })

        # Build pattern summary
        if patterns['detected_patterns']:
            for pattern in patterns['detected_patterns']:
                p_type = pattern['pattern_type']
                if p_type not in patterns['pattern_summary']:
                    patterns['pattern_summary'][p_type] = {
                        'total_occurrences': 0,
                        'avg_severity': 0,
                        'last_seen': datetime.now().isoformat()
                    }
                patterns['pattern_summary'][p_type]['total_occurrences'] += pattern['occurrences']

        # Build attack timeline
        if 'Timestamp' in batch_data.columns and 'Normal/Attack' in batch_data.columns:
            attacks = batch_data[batch_data['Normal/Attack'] == 1]
            for idx, row in attacks.iterrows():
                patterns['attack_timeline'].append({
                    'timestamp': row['Timestamp'] if isinstance(row['Timestamp'], str) else row['Timestamp'].isoformat(),
                    'attack_type': row.get('Attack_Type', 'Unknown'),
                    'severity': row.get('Attack_Severity', 'Unknown'),
                    'stage': int(row.get('Affected_Stage', 0))
                })

        # Store in history
        self.pattern_history.append({
            'timestamp': datetime.now().isoformat(),
            'patterns': patterns['detected_patterns']
        })

        return patterns

    def _get_pattern_description(self, attack_type):
        """Get human-readable description of attack pattern"""
        descriptions = {
            'sensor_spike': 'Abnormal spike in sensor readings - possible sensor tampering or extreme process deviation',
            'sensor_drop': 'Sudden drop in sensor values - potential sensor failure or malicious manipulation',
            'sensor_flatline': 'Sensor readings frozen at constant value - likely sensor compromise or communication attack',
            'sensor_oscillation': 'Rapid fluctuations in sensor data - indicative of replay attack or control system interference',
            'pump_manipulation': 'Unauthorized changes to pump states - direct actuator manipulation attack',
            'valve_manipulation': 'Abnormal valve position changes - actuator-based attack affecting flow control',
            'multi_stage_cascade': 'Coordinated attack across multiple process stages - advanced persistent threat',
            'data_injection': 'Subtle false data injection - stealthy attack aiming to evade detection'
        }
        return descriptions.get(attack_type, 'Unknown attack pattern')

    def get_pattern_statistics(self):
        """Get overall pattern statistics"""
        return {
            'total_patterns_detected': sum(self.pattern_stats.values()),
            'pattern_breakdown': dict(self.pattern_stats),
            'most_common_pattern': max(self.pattern_stats.items(), key=lambda x: x[1])[0] if self.pattern_stats else None,
            'pattern_diversity': len(self.pattern_stats)
        }


class AlertSystem:
    """Real-time alert generation system"""

    def __init__(self):
        self.active_alerts = []
        self.alert_history = deque(maxlen=200)
        self.thresholds = {
            'cyber_risk': {'critical': 70, 'high': 50, 'medium': 30},
            'operational_risk': {'critical': 70, 'high': 50, 'medium': 30},
            'anomaly_rate': {'critical': 40, 'high': 25, 'medium': 15},
            'sensor_anomalies': {'critical': 5, 'high': 3, 'medium': 1}
        }

    def check_and_generate_alerts(self, results, sensor_analysis, patterns):
        """Check conditions and generate alerts"""
        new_alerts = []

        # Check cyber risk
        cyber_score = results['cyber_risk']['score']
        if cyber_score >= self.thresholds['cyber_risk']['critical']:
            new_alerts.append(self._create_alert(
                'critical',
                'cyber_risk',
                f'Critical cyber risk detected: {cyber_score:.1f}%',
                {'score': cyber_score, 'level': results['cyber_risk']['level']}
            ))
        elif cyber_score >= self.thresholds['cyber_risk']['high']:
            new_alerts.append(self._create_alert(
                'high',
                'cyber_risk',
                f'High cyber risk: {cyber_score:.1f}%',
                {'score': cyber_score, 'level': results['cyber_risk']['level']}
            ))

        # Check operational risk
        ops_score = results['operational_risk']['score']
        if ops_score >= self.thresholds['operational_risk']['critical']:
            new_alerts.append(self._create_alert(
                'critical',
                'operational_risk',
                f'Critical operational risk: {ops_score:.1f}%',
                {'score': ops_score, 'level': results['operational_risk']['level']}
            ))
        elif ops_score >= self.thresholds['operational_risk']['high']:
            new_alerts.append(self._create_alert(
                'high',
                'operational_risk',
                f'High operational risk: {ops_score:.1f}%',
                {'score': ops_score, 'level': results['operational_risk']['level']}
            ))

        # Check anomaly rate
        anomaly_rate = results['detection']['anomaly_rate']
        if anomaly_rate >= self.thresholds['anomaly_rate']['critical']:
            new_alerts.append(self._create_alert(
                'critical',
                'anomaly_detection',
                f'Critical anomaly rate: {anomaly_rate:.1f}%',
                {'rate': anomaly_rate, 'count': results['detection']['num_anomalies']}
            ))

        # Check critical sensors
        critical_sensor_count = len(sensor_analysis['critical_sensors'])
        if critical_sensor_count >= self.thresholds['sensor_anomalies']['critical']:
            new_alerts.append(self._create_alert(
                'critical',
                'sensor_failure',
                f'{critical_sensor_count} sensors in critical state',
                {'sensors': sensor_analysis['critical_sensors']}
            ))

        # Check for specific attack patterns
        if patterns['detected_patterns']:
            for pattern in patterns['detected_patterns']:
                if pattern['pattern_type'] == 'multi_stage_cascade':
                    new_alerts.append(self._create_alert(
                        'critical',
                        'attack_pattern',
                        'Multi-stage cascade attack detected',
                        pattern
                    ))

        # Add to history and active alerts
        for alert in new_alerts:
            self.alert_history.append(alert)
            self.active_alerts.append(alert)

        # Clean up old alerts (older than 5 minutes)
        current_time = datetime.now()
        self.active_alerts = [
            alert for alert in self.active_alerts
            if (current_time - datetime.fromisoformat(alert['timestamp'])).total_seconds() < 300
        ]

        return new_alerts

    def _create_alert(self, severity, alert_type, message, details):
        """Create an alert object"""
        return {
            'id': f"alert_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'type': alert_type,
            'message': message,
            'details': details,
            'acknowledged': False
        }

    def get_active_alerts(self):
        """Get currently active alerts"""
        return sorted(self.active_alerts, key=lambda x: x['timestamp'], reverse=True)

    def get_alert_summary(self):
        """Get alert statistics"""
        if not self.alert_history:
            return {'total': 0, 'by_severity': {}, 'by_type': {}}

        df = pd.DataFrame(list(self.alert_history))
        return {
            'total_alerts': len(self.alert_history),
            'active_alerts': len(self.active_alerts),
            'by_severity': df['severity'].value_counts().to_dict(),
            'by_type': df['type'].value_counts().to_dict(),
            'recent_critical': len(df[df['severity'] == 'critical'].tail(10))
        }

    def acknowledge_alert(self, alert_id):
        """Mark an alert as acknowledged"""
        for alert in self.active_alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                return True
        return False
