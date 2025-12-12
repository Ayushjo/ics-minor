"""
Risk Mapping Module for ICS Multi-Agent System
Maps sensors to system-level risks and tracks risk distributions
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from collections import defaultdict


class RiskMappingAgent:
    """
    Maps sensor anomalies to system-level risks and tracks risk distributions.
    Identifies which sensors contribute to which operational risks.
    """

    # Define the 8 system-level risks
    RISK_CATEGORIES = [
        "Water Overflow",
        "Pump Damage",
        "Water Quality Degradation",
        "Unsafe Chemical Dosing",
        "Process Interruption",
        "Unauthorized Access",
        "Data Tampering",
        "Denial of Service"
    ]

    # Sensor-to-Risk mapping based on SWaT architecture
    SENSOR_RISK_MAP = {
        # Stage 1 - Raw Water Supply
        'LIT-101': ['Water Overflow', 'Process Interruption', 'Data Tampering'],
        'FIT-101': ['Pump Damage', 'Unsafe Chemical Dosing', 'Process Interruption', 'Data Tampering'],
        'P-101': ['Pump Damage', 'Process Interruption'],
        'P-102': ['Pump Damage', 'Process Interruption'],
        'MV-101': ['Water Overflow', 'Process Interruption'],
        'AIT-101': ['Water Quality Degradation', 'Data Tampering'],
        'AIT-102': ['Water Quality Degradation', 'Data Tampering'],
        'DPIT-101': ['Pump Damage', 'Process Interruption'],

        # Stage 2 - Chemical Dosing
        'FIT-201': ['Unsafe Chemical Dosing', 'Water Quality Degradation', 'Process Interruption'],
        'AIT-201': ['Water Quality Degradation', 'Unsafe Chemical Dosing', 'Data Tampering'],
        'AIT-202': ['Water Quality Degradation', 'Unsafe Chemical Dosing', 'Data Tampering'],
        'AIT-203': ['Water Quality Degradation', 'Unsafe Chemical Dosing', 'Data Tampering'],
        'P-201': ['Pump Damage', 'Unsafe Chemical Dosing'],
        'P-202': ['Pump Damage', 'Unsafe Chemical Dosing'],
        'P-203': ['Pump Damage', 'Unsafe Chemical Dosing'],
        'P-204': ['Pump Damage', 'Unsafe Chemical Dosing'],
        'MV-201': ['Unsafe Chemical Dosing', 'Process Interruption'],

        # Stage 3 - Ultrafiltration
        'FIT-301': ['Pump Damage', 'Process Interruption', 'Data Tampering'],
        'LIT-301': ['Water Overflow', 'Process Interruption', 'Data Tampering'],
        'DPIT-301': ['Pump Damage', 'Process Interruption'],
        'P-301': ['Pump Damage', 'Process Interruption'],
        'P-302': ['Pump Damage', 'Process Interruption'],
        'MV-301': ['Water Overflow', 'Process Interruption'],
        'MV-302': ['Water Overflow', 'Process Interruption'],
        'AIT-301': ['Water Quality Degradation', 'Data Tampering'],
        'AIT-302': ['Water Quality Degradation', 'Data Tampering'],
        'AIT-303': ['Water Quality Degradation', 'Data Tampering'],

        # Stage 4 - UV Dechlorination
        'FIT-401': ['Pump Damage', 'Process Interruption', 'Data Tampering'],
        'LIT-401': ['Water Overflow', 'Process Interruption', 'Data Tampering'],
        'AIT-401': ['Water Quality Degradation', 'Unsafe Chemical Dosing', 'Data Tampering'],
        'AIT-402': ['Water Quality Degradation', 'Unsafe Chemical Dosing', 'Data Tampering'],
        'P-401': ['Pump Damage', 'Process Interruption'],
        'P-402': ['Pump Damage', 'Process Interruption'],
        'P-403': ['Pump Damage', 'Process Interruption'],
        'UV-401': ['Water Quality Degradation', 'Process Interruption'],

        # Stage 5 - Reverse Osmosis
        'FIT-501': ['Pump Damage', 'Water Quality Degradation', 'Process Interruption'],
        'FIT-502': ['Pump Damage', 'Water Quality Degradation', 'Process Interruption'],
        'FIT-503': ['Pump Damage', 'Water Quality Degradation', 'Process Interruption'],
        'PIT-501': ['Pump Damage', 'Process Interruption', 'Data Tampering'],
        'PIT-502': ['Pump Damage', 'Process Interruption', 'Data Tampering'],
        'P-501': ['Pump Damage', 'Process Interruption'],
        'P-502': ['Pump Damage', 'Process Interruption'],
        'AIT-501': ['Water Quality Degradation', 'Data Tampering'],

        # Stage 6 - Backwash/Cleaning
        'FIT-601': ['Pump Damage', 'Process Interruption', 'Data Tampering'],
        'LIT-601': ['Water Overflow', 'Process Interruption', 'Data Tampering'],
        'P-601': ['Pump Damage', 'Process Interruption'],
        'P-602': ['Pump Damage', 'Process Interruption'],
        'P-603': ['Pump Damage', 'Process Interruption'],
        'DPIT-601': ['Pump Damage', 'Process Interruption'],
        'AIT-601': ['Water Quality Degradation', 'Data Tampering'],
        'AIT-602': ['Water Quality Degradation', 'Data Tampering'],
    }

    # Stage mapping for sensors
    SENSOR_STAGE_MAP = {
        'LIT-101': 'P1', 'FIT-101': 'P1', 'P-101': 'P1', 'P-102': 'P1',
        'MV-101': 'P1', 'AIT-101': 'P1', 'AIT-102': 'P1', 'DPIT-101': 'P1',

        'FIT-201': 'P2', 'AIT-201': 'P2', 'AIT-202': 'P2', 'AIT-203': 'P2',
        'P-201': 'P2', 'P-202': 'P2', 'P-203': 'P2', 'P-204': 'P2', 'MV-201': 'P2',

        'FIT-301': 'P3', 'LIT-301': 'P3', 'DPIT-301': 'P3', 'P-301': 'P3',
        'P-302': 'P3', 'MV-301': 'P3', 'MV-302': 'P3', 'AIT-301': 'P3',
        'AIT-302': 'P3', 'AIT-303': 'P3',

        'FIT-401': 'P4', 'LIT-401': 'P4', 'AIT-401': 'P4', 'AIT-402': 'P4',
        'P-401': 'P4', 'P-402': 'P4', 'P-403': 'P4', 'UV-401': 'P4',

        'FIT-501': 'P5', 'FIT-502': 'P5', 'FIT-503': 'P5', 'PIT-501': 'P5',
        'PIT-502': 'P5', 'P-501': 'P5', 'P-502': 'P5', 'AIT-501': 'P5',

        'FIT-601': 'P6', 'LIT-601': 'P6', 'P-601': 'P6', 'P-602': 'P6',
        'P-603': 'P6', 'DPIT-601': 'P6', 'AIT-601': 'P6', 'AIT-602': 'P6',
    }

    def __init__(self):
        """Initialize the Risk Mapping Agent"""
        self.risk_history = defaultdict(lambda: defaultdict(int))
        self.sensor_anomaly_counts = defaultdict(int)
        self.total_anomalies = 0

    def map_anomalies_to_risks(self, anomaly_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map detected anomalies to system-level risks

        Args:
            anomaly_data: Dictionary containing anomaly detection results
                - predictions: array of binary predictions (0=normal, 1=anomaly)
                - attack_probabilities: probability scores for each sample
                - sensor_data: DataFrame with sensor readings

        Returns:
            Dictionary with risk mapping analysis
        """
        try:
            predictions = anomaly_data.get('predictions', [])
            sensor_data = anomaly_data.get('sensor_data', None)

            if sensor_data is None or len(predictions) == 0:
                return self._empty_risk_mapping()

            # Find which sensors have anomalies
            anomalous_indices = np.where(np.array(predictions) == 1)[0]

            if len(anomalous_indices) == 0:
                return self._empty_risk_mapping()

            # Analyze anomalous samples
            risk_contributions = defaultdict(list)
            sensor_contributions = defaultdict(lambda: defaultdict(int))

            for idx in anomalous_indices:
                sample = sensor_data.iloc[idx]

                # Check each sensor for anomalies
                for sensor_name in self.SENSOR_RISK_MAP.keys():
                    if sensor_name in sample.index:
                        sensor_value = sample[sensor_name]

                        # Simple anomaly detection: check if value is significantly different
                        # In real scenario, you'd use more sophisticated detection
                        if self._is_sensor_anomalous(sensor_name, sensor_value, sensor_data):
                            self.sensor_anomaly_counts[sensor_name] += 1
                            self.total_anomalies += 1

                            # Map to risks
                            risks = self.SENSOR_RISK_MAP.get(sensor_name, [])
                            for risk in risks:
                                risk_contributions[risk].append(sensor_name)
                                sensor_contributions[sensor_name][risk] += 1
                                self.risk_history[risk][sensor_name] += 1

            # Calculate risk distribution
            risk_distribution = self._calculate_risk_distribution(risk_contributions)

            # Identify majority risk
            majority_risk = self._identify_majority_risk(risk_distribution, risk_contributions)

            # Get sensor contribution details
            sensor_contribution_details = self._get_sensor_contributions(sensor_contributions)

            # Get risk details
            risk_details = self._get_risk_details(risk_contributions)

            return {
                'distribution': risk_distribution,
                'majority_risk': majority_risk,
                'sensor_contributions': sensor_contribution_details,
                'risk_details': risk_details,
                'total_anomalies_analyzed': len(anomalous_indices)
            }

        except Exception as e:
            print(f"Error in risk mapping: {str(e)}")
            return self._empty_risk_mapping()

    def _is_sensor_anomalous(self, sensor_name: str, value: float, sensor_data) -> bool:
        """
        Check if a sensor value is anomalous

        Args:
            sensor_name: Name of the sensor
            value: Current sensor value
            sensor_data: DataFrame with all sensor readings

        Returns:
            Boolean indicating if sensor is anomalous
        """
        try:
            if sensor_name not in sensor_data.columns:
                return False

            sensor_column = sensor_data[sensor_name]
            mean = sensor_column.mean()
            std = sensor_column.std()

            if std == 0:
                return False

            # Consider anomalous if more than 2 standard deviations from mean
            z_score = abs((value - mean) / std)
            return z_score > 2.0

        except Exception:
            return False

    def _calculate_risk_distribution(self, risk_contributions: Dict) -> Dict[str, float]:
        """Calculate percentage distribution of risks"""
        total_contributions = sum(len(sensors) for sensors in risk_contributions.values())

        if total_contributions == 0:
            return {risk: 0.0 for risk in self.RISK_CATEGORIES}

        distribution = {}
        for risk in self.RISK_CATEGORIES:
            count = len(risk_contributions.get(risk, []))
            distribution[risk] = round(count / total_contributions, 3)

        return distribution

    def _identify_majority_risk(self, distribution: Dict[str, float],
                               risk_contributions: Dict) -> Dict[str, Any]:
        """Identify the majority (dominant) risk category"""
        if not distribution or max(distribution.values()) == 0:
            return {
                'category': 'None',
                'percentage': 0,
                'count': 0,
                'affected_sensors': [],
                'affected_stages': [],
                'severity': 'Low',
                'description': 'No dominant risk detected'
            }

        # Find risk with highest percentage
        majority_risk_name = max(distribution, key=distribution.get)
        percentage = distribution[majority_risk_name]

        # Get affected sensors
        affected_sensors = list(set(risk_contributions.get(majority_risk_name, [])))
        count = len(risk_contributions.get(majority_risk_name, []))

        # Get affected stages
        affected_stages = list(set([
            self.SENSOR_STAGE_MAP.get(sensor, 'Unknown')
            for sensor in affected_sensors
        ]))

        # Determine severity
        if percentage >= 0.4:
            severity = 'Critical'
        elif percentage >= 0.25:
            severity = 'High'
        elif percentage >= 0.15:
            severity = 'Medium'
        else:
            severity = 'Low'

        # Generate description
        description = self._generate_risk_description(
            majority_risk_name, affected_sensors, affected_stages
        )

        return {
            'category': majority_risk_name,
            'percentage': round(percentage * 100, 1),
            'count': count,
            'affected_sensors': affected_sensors[:5],  # Top 5
            'affected_stages': sorted(affected_stages),
            'severity': severity,
            'description': description
        }

    def _generate_risk_description(self, risk_name: str, sensors: List[str],
                                   stages: List[str]) -> str:
        """Generate human-readable risk description"""
        descriptions = {
            'Water Overflow': f"Tank level sensors showing overflow conditions in stages {', '.join(stages)}",
            'Pump Damage': f"Pump or flow sensors indicating damage risk in stages {', '.join(stages)}",
            'Water Quality Degradation': f"Water quality sensors detecting contamination in stages {', '.join(stages)}",
            'Unsafe Chemical Dosing': f"Chemical dosing sensors showing unsafe levels in stages {', '.join(stages)}",
            'Process Interruption': f"Critical process sensors indicating potential shutdown in stages {', '.join(stages)}",
            'Unauthorized Access': f"Security breach detected affecting sensors in stages {', '.join(stages)}",
            'Data Tampering': f"Sensor data integrity compromised in stages {', '.join(stages)}",
            'Denial of Service': f"Communication loss with sensors in stages {', '.join(stages)}"
        }

        return descriptions.get(risk_name, f"Risk detected in stages {', '.join(stages)}")

    def _get_sensor_contributions(self, sensor_contributions: Dict) -> Dict[str, Any]:
        """Get detailed sensor contribution information"""
        result = {}

        for sensor_name, risks in sensor_contributions.items():
            total_count = sum(risks.values())
            primary_risk = max(risks, key=risks.get) if risks else 'Unknown'

            result[sensor_name] = {
                'risks': list(risks.keys()),
                'anomaly_count': total_count,
                'primary_risk': primary_risk,
                'stage': self.SENSOR_STAGE_MAP.get(sensor_name, 'Unknown')
            }

        return result

    def _get_risk_details(self, risk_contributions: Dict) -> Dict[str, Any]:
        """Get detailed information for each risk category"""
        result = {}

        for risk in self.RISK_CATEGORIES:
            sensors = risk_contributions.get(risk, [])

            # Count sensor occurrences
            sensor_counts = defaultdict(int)
            for sensor in sensors:
                sensor_counts[sensor] += 1

            # Build sensor list with counts
            sensor_list = []
            for sensor, count in sorted(sensor_counts.items(),
                                       key=lambda x: x[1], reverse=True):
                sensor_list.append({
                    'id': sensor,
                    'count': count,
                    'stage': self.SENSOR_STAGE_MAP.get(sensor, 'Unknown')
                })

            result[risk] = {
                'sensors': sensor_list[:10],  # Top 10 sensors
                'total': len(sensors),
                'unique_sensors': len(sensor_counts)
            }

        return result

    def _empty_risk_mapping(self) -> Dict[str, Any]:
        """Return empty risk mapping structure"""
        return {
            'distribution': {risk: 0.0 for risk in self.RISK_CATEGORIES},
            'majority_risk': {
                'category': 'None',
                'percentage': 0,
                'count': 0,
                'affected_sensors': [],
                'affected_stages': [],
                'severity': 'Low',
                'description': 'No anomalies detected'
            },
            'sensor_contributions': {},
            'risk_details': {risk: {'sensors': [], 'total': 0, 'unique_sensors': 0}
                           for risk in self.RISK_CATEGORIES},
            'total_anomalies_analyzed': 0
        }

    def get_historical_risk_summary(self) -> Dict[str, Any]:
        """Get summary of historical risk data"""
        summary = {
            'total_anomalies': self.total_anomalies,
            'risk_counts': {},
            'top_affected_sensors': []
        }

        # Calculate total for each risk
        for risk in self.RISK_CATEGORIES:
            total = sum(self.risk_history[risk].values())
            summary['risk_counts'][risk] = total

        # Get top affected sensors
        sorted_sensors = sorted(
            self.sensor_anomaly_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        summary['top_affected_sensors'] = [
            {'sensor': sensor, 'count': count, 'stage': self.SENSOR_STAGE_MAP.get(sensor, 'Unknown')}
            for sensor, count in sorted_sensors[:10]
        ]

        return summary

    def reset_history(self):
        """Reset all historical tracking data"""
        self.risk_history.clear()
        self.sensor_anomaly_counts.clear()
        self.total_anomalies = 0


# Helper function to get sensor-risk matrix
def get_sensor_risk_matrix() -> Dict[str, Any]:
    """
    Return the complete sensor-to-risk mapping matrix
    Useful for frontend visualization
    """
    agent = RiskMappingAgent()

    matrix = {}
    for sensor, risks in agent.SENSOR_RISK_MAP.items():
        matrix[sensor] = {
            'risks': risks,
            'stage': agent.SENSOR_STAGE_MAP.get(sensor, 'Unknown'),
            'risk_count': len(risks)
        }

    return {
        'matrix': matrix,
        'risk_categories': agent.RISK_CATEGORIES,
        'total_sensors': len(agent.SENSOR_RISK_MAP),
        'total_risks': len(agent.RISK_CATEGORIES)
    }
