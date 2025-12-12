import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, PowerTransformer, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import joblib
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import Risk Mapping Agent
try:
    from risk_mapping import RiskMappingAgent
except ImportError:
    RiskMappingAgent = None


def load_and_merge_data(file1_path: str, file2_path: str) -> pd.DataFrame:
    """Load and merge two CSV datasets for training."""
    print("Loading data files...")

    df1 = pd.read_csv(file1_path, header=0, low_memory=False)
    df1.columns = df1.iloc[0]
    df1 = df1[1:]

    df = pd.read_csv(file2_path, header=0, low_memory=False)
    df.columns = df.iloc[0]
    df = df[1:]

    df.columns = df.columns.str.strip()
    df1.columns = df1.columns.str.strip()

    df1['Normal/Attack'] = (df1['Normal/Attack'].astype(str).str.strip()
                           .str.replace(r'\s+', '', regex=True).str.lower())
    df1['Normal/Attack'] = df1['Normal/Attack'].replace({
        'attack': 'Attack', 'normal': 'Normal', 'a ttack': 'Attack'
    })

    df['Normal/Attack'] = 'Normal'

    df_merged = pd.concat([df1, df], ignore_index=True)
    df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)
    df_merged = df_merged.drop_duplicates()

    print(f"Data loaded successfully!")
    print(f"Total samples: {len(df_merged)}")
    print(f"Label distribution:\n{df_merged['Normal/Attack'].value_counts()}")

    return df_merged


class PerceptionAgent:
    """Handles data preprocessing, normalization, and feature transformation."""

    def __init__(self):
        self.scaler = None
        self.power_transformer = None
        self.feature_cols = None
        self.skewed_features = None

    def fit(self, df: pd.DataFrame) -> None:
        """Fit preprocessing transformers on training data."""
        print("[Perception Agent] Fitting preprocessing pipeline...")

        self.feature_cols = [col for col in df.columns
                            if col not in ['Timestamp', 'Normal/Attack']]

        df[self.feature_cols] = df[self.feature_cols].astype(float)

        self.skewed_features = [col for col in self.feature_cols
                               if abs(df[col].skew()) > 1]

        print(f"[Perception Agent] Found {len(self.skewed_features)} skewed features")

        if self.skewed_features:
            self.power_transformer = PowerTransformer(method='yeo-johnson')
            self.power_transformer.fit(df[self.skewed_features])

        self.scaler = StandardScaler()
        X = df[self.feature_cols].copy()
        if self.skewed_features:
            X[self.skewed_features] = self.power_transformer.transform(X[self.skewed_features])
        self.scaler.fit(X)

        print("[Perception Agent] Preprocessing pipeline fitted")

    def preprocess(self, raw_data: pd.DataFrame) -> Tuple[np.ndarray, pd.Series]:
        """Clean and normalize incoming sensor data."""
        if self.scaler is None:
            raise ValueError("Agent not fitted. Call fit() first.")

        df = raw_data.copy()
        df[self.feature_cols] = df[self.feature_cols].ffill()

        if self.skewed_features:
            df[self.skewed_features] = self.power_transformer.transform(
                df[self.skewed_features]
            )

        X_scaled = self.scaler.transform(df[self.feature_cols])
        return X_scaled, df['Timestamp']

    def save(self, filepath: str) -> None:
        """Save agent state."""
        joblib.dump({
            'scaler': self.scaler,
            'power_transformer': self.power_transformer,
            'feature_cols': self.feature_cols,
            'skewed_features': self.skewed_features
        }, filepath)
        print(f"[Perception Agent] Saved to {filepath}")

    def load(self, filepath: str) -> None:
        """Load agent state."""
        state = joblib.load(filepath)
        self.scaler = state['scaler']
        self.power_transformer = state['power_transformer']
        self.feature_cols = state['feature_cols']
        self.skewed_features = state['skewed_features']
        print(f"[Perception Agent] Loaded from {filepath}")


class FaultDetectionAgent:
    """Detects anomalies using Random Forest classifier."""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.threshold = 0.5

        if model_path:
            self.load_model(model_path)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the fault detection model."""
        print("[Fault Detection Agent] Training Random Forest model...")

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_train, y_train)
        print("[Fault Detection Agent] Model training complete")

    def detect(self, X: np.ndarray) -> Dict:
        """Detect faults in preprocessed sensor data."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() or load_model() first.")

        y_pred = self.model.predict(X)
        y_prob = self.model.predict_proba(X)[:, 1]

        anomaly_flags = y_pred == 1
        confidence = np.max(self.model.predict_proba(X), axis=1)

        return {
            'anomaly_detected': anomaly_flags,
            'attack_probability': y_prob,
            'predictions': y_pred,
            'confidence': confidence,
            'num_anomalies': int(anomaly_flags.sum()),
            'anomaly_rate': float(anomaly_flags.mean())
        }

    def save_model(self, filepath: str) -> None:
        """Save trained model."""
        joblib.dump(self.model, filepath)
        print(f"[Fault Detection Agent] Model saved to {filepath}")

    def load_model(self, filepath: str) -> None:
        """Load pre-trained model."""
        self.model = joblib.load(filepath)
        print(f"[Fault Detection Agent] Model loaded from {filepath}")


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CyberRiskAssessmentAgent:
    """Evaluates likelihood of cyber-induced anomalies."""

    def __init__(self):
        self.prob_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.85
        }

    def assess_risk(self, detection_results: Dict, timestamps: np.ndarray = None) -> Dict:
        """Assess cyber risk based on fault detection results."""
        attack_probs = detection_results['attack_probability']
        anomaly_flags = detection_results['anomaly_detected']

        avg_attack_prob = float(np.mean(attack_probs))
        max_attack_prob = float(np.max(attack_probs))
        num_anomalies = int(np.sum(anomaly_flags))
        anomaly_rate = float(np.mean(anomaly_flags))

        temporal_risk_score = 0.0
        if timestamps is not None and len(timestamps) > 1:
            temporal_risk_score = self._analyze_temporal_pattern(anomaly_flags)

        cyber_risk_score = self._calculate_cyber_risk_score(
            avg_attack_prob, anomaly_rate, temporal_risk_score
        )

        risk_level = self._classify_risk_level(cyber_risk_score)
        attack_signature = self._identify_attack_pattern(anomaly_flags, attack_probs)

        return {
            'cyber_risk_score': cyber_risk_score,
            'risk_level': risk_level.value,
            'avg_attack_probability': avg_attack_prob,
            'max_attack_probability': max_attack_prob,
            'anomaly_count': num_anomalies,
            'anomaly_rate': anomaly_rate,
            'temporal_risk': temporal_risk_score,
            'attack_signature': attack_signature,
            'threat_assessment': self._generate_threat_assessment(risk_level, attack_signature)
        }

    def _calculate_cyber_risk_score(self, avg_prob: float, anomaly_rate: float,
                                    temporal_risk: float) -> float:
        score = (0.4 * avg_prob + 0.3 * anomaly_rate + 0.3 * temporal_risk)
        return min(1.0, score)

    def _analyze_temporal_pattern(self, anomaly_flags: np.ndarray) -> float:
        if len(anomaly_flags) < 10:
            return 0.0

        consecutive_count = 0
        max_consecutive = 0

        for flag in anomaly_flags:
            if flag:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                consecutive_count = 0

        temporal_risk = min(1.0, max_consecutive / 10.0)
        return temporal_risk

    def _classify_risk_level(self, score: float) -> RiskLevel:
        if score < self.prob_thresholds['low']:
            return RiskLevel.LOW
        elif score < self.prob_thresholds['medium']:
            return RiskLevel.MEDIUM
        elif score < self.prob_thresholds['high']:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL

    def _identify_attack_pattern(self, anomaly_flags: np.ndarray,
                                 attack_probs: np.ndarray) -> str:
        anomaly_rate = np.mean(anomaly_flags)
        avg_prob = np.mean(attack_probs[anomaly_flags]) if anomaly_flags.any() else 0

        if anomaly_rate > 0.8:
            return "Persistent Attack"
        elif anomaly_rate > 0.5:
            return "Intermittent Attack"
        elif avg_prob > 0.9:
            return "Targeted Attack"
        elif anomaly_rate > 0.1:
            return "Sporadic Anomalies"
        else:
            return "Normal Operation"

    def _generate_threat_assessment(self, risk_level: RiskLevel,
                                    attack_signature: str) -> str:
        assessments = {
            RiskLevel.LOW: f"Minimal cyber threat detected. {attack_signature}.",
            RiskLevel.MEDIUM: f"Moderate cyber risk. {attack_signature}. Monitor closely.",
            RiskLevel.HIGH: f"High cyber threat level! {attack_signature}. Immediate attention required.",
            RiskLevel.CRITICAL: f"CRITICAL CYBER ATTACK! {attack_signature}. Activate incident response!"
        }
        return assessments.get(risk_level, "Unknown threat level")


class OperationalRiskAssessmentAgent:
    """Assesses impact on system safety, performance, and operational continuity."""

    def __init__(self):
        self.risk_matrix = {
            ('low', 'low'): 0.1,
            ('low', 'medium'): 0.2,
            ('low', 'high'): 0.4,
            ('medium', 'low'): 0.3,
            ('medium', 'medium'): 0.5,
            ('medium', 'high'): 0.7,
            ('high', 'low'): 0.5,
            ('high', 'medium'): 0.7,
            ('high', 'high'): 0.9
        }

    def assess_risk(self, detection_results: Dict, cyber_risk: Dict) -> Dict:
        """Assess operational risk and fault severity."""
        anomaly_rate = detection_results['anomaly_rate']
        num_anomalies = detection_results['num_anomalies']

        impact_level = self._assess_impact(anomaly_rate, num_anomalies)
        likelihood = cyber_risk['risk_level']

        op_risk_score = self._calculate_operational_risk(likelihood, impact_level)
        fault_severity = self._assess_fault_severity(op_risk_score, anomaly_rate)
        affected_systems = self._identify_affected_systems(num_anomalies, anomaly_rate)
        estimated_downtime = self._estimate_downtime(fault_severity, impact_level)

        return {
            'operational_risk_score': op_risk_score,
            'risk_level': self._classify_risk_level(op_risk_score).value,
            'fault_severity': fault_severity,
            'impact_level': impact_level,
            'likelihood': likelihood,
            'affected_systems': affected_systems,
            'estimated_downtime_minutes': estimated_downtime,
            'safety_impact': self._assess_safety_impact(op_risk_score),
            'performance_degradation': self._assess_performance_impact(anomaly_rate),
            'mitigation_priority': self._determine_priority(op_risk_score, fault_severity)
        }

    def _assess_impact(self, anomaly_rate: float, num_anomalies: int) -> str:
        if anomaly_rate > 0.7 or num_anomalies > 1000:
            return 'high'
        elif anomaly_rate > 0.3 or num_anomalies > 100:
            return 'medium'
        else:
            return 'low'

    def _calculate_operational_risk(self, likelihood: str, impact: str) -> float:
        likelihood_map = {
            'low': 'low',
            'medium': 'medium',
            'high': 'high',
            'critical': 'high'
        }
        normalized_likelihood = likelihood_map.get(likelihood, 'medium')
        return self.risk_matrix.get((normalized_likelihood, impact), 0.5)

    def _assess_fault_severity(self, risk_score: float, anomaly_rate: float) -> str:
        combined_score = (risk_score + anomaly_rate) / 2

        if combined_score > 0.8:
            return 'Critical'
        elif combined_score > 0.6:
            return 'High'
        elif combined_score > 0.3:
            return 'Medium'
        else:
            return 'Low'

    def _identify_affected_systems(self, num_anomalies: int, anomaly_rate: float) -> List[str]:
        affected = []

        if anomaly_rate > 0.5:
            affected.extend(['Primary Treatment', 'Distribution System'])
        if num_anomalies > 500:
            affected.append('Control System')
        if anomaly_rate > 0.8:
            affected.append('Safety Systems')

        return affected if affected else ['Monitoring Systems']

    def _estimate_downtime(self, severity: str, impact: str) -> int:
        downtime_map = {
            ('Critical', 'high'): 240,
            ('Critical', 'medium'): 120,
            ('High', 'high'): 120,
            ('High', 'medium'): 60,
            ('Medium', 'high'): 60,
            ('Medium', 'medium'): 30,
        }
        return downtime_map.get((severity, impact), 15)

    def _assess_safety_impact(self, risk_score: float) -> str:
        if risk_score > 0.8:
            return 'Severe - Immediate safety concerns'
        elif risk_score > 0.6:
            return 'Moderate - Safety monitoring required'
        elif risk_score > 0.3:
            return 'Minor - Standard safety protocols'
        else:
            return 'Minimal - No safety concerns'

    def _assess_performance_impact(self, anomaly_rate: float) -> str:
        degradation = anomaly_rate * 100
        return f"{degradation:.1f}% performance degradation"

    def _determine_priority(self, risk_score: float, severity: str) -> int:
        if severity == 'Critical' or risk_score > 0.8:
            return 1
        elif severity == 'High' or risk_score > 0.6:
            return 2
        elif severity == 'Medium' or risk_score > 0.4:
            return 3
        else:
            return 4

    def _classify_risk_level(self, score: float) -> RiskLevel:
        if score < 0.3:
            return RiskLevel.LOW
        elif score < 0.6:
            return RiskLevel.MEDIUM
        elif score < 0.85:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL


class DecisionMakingAgent:
    """Recommends and prioritizes mitigation actions based on risk assessments."""

    def __init__(self):
        self.action_library = {
            'critical_cyber': [
                'Isolate affected network segments',
                'Activate incident response team',
                'Switch to backup control system',
                'Initiate emergency shutdown protocol',
                'Preserve logs for forensic analysis'
            ],
            'high_cyber': [
                'Increase monitoring frequency',
                'Restrict remote access',
                'Verify actuator commands',
                'Alert security operations center'
            ],
            'critical_operational': [
                'Emergency shutdown of affected stages',
                'Activate backup water supply',
                'Notify emergency response team',
                'Implement manual override controls',
                'Evacuate non-essential personnel'
            ],
            'high_operational': [
                'Reduce process throughput',
                'Activate redundant systems',
                'Increase operator supervision',
                'Prepare for manual intervention'
            ],
            'medium_risk': [
                'Continue enhanced monitoring',
                'Log anomalies for analysis',
                'Notify maintenance team',
                'Schedule system inspection'
            ],
            'low_risk': [
                'Standard monitoring protocols',
                'Document anomaly in system logs'
            ]
        }

        self.stage_actions = {
            'P1': ['Close inlet valve MV101', 'Stop pumps P101/P102'],
            'P2': ['Isolate chemical dosing', 'Stop dosing pumps'],
            'P3': ['Bypass ultrafiltration', 'Activate backwash'],
            'P4': ['Switch to backup UV system', 'Adjust dechlorination'],
            'P5': ['Reduce RO pressure', 'Activate membrane protection'],
            'P6': ['Close distribution valves', 'Activate storage tanks']
        }

    def decide(self, cyber_assessment: Dict, operational_assessment: Dict) -> Dict:
        """Generate mitigation strategy based on risk assessments."""
        cyber_risk = cyber_assessment['risk_level']
        operational_risk = operational_assessment['risk_level']
        fault_severity = operational_assessment['fault_severity']
        affected_systems = operational_assessment['affected_systems']

        primary_threat = self._identify_primary_threat(cyber_risk, operational_risk)
        recommended_actions = self._select_actions(cyber_risk, operational_risk, fault_severity)
        stage_specific_actions = self._get_stage_actions(affected_systems)
        action_priority = self._prioritize_actions(
            recommended_actions,
            operational_assessment['mitigation_priority']
        )
        response_timeline = self._calculate_response_timeline(
            cyber_risk, operational_risk, fault_severity
        )
        rationale = self._generate_rationale(
            primary_threat, cyber_assessment, operational_assessment
        )

        return {
            'primary_threat': primary_threat,
            'recommended_actions': recommended_actions,
            'stage_specific_actions': stage_specific_actions,
            'action_priority': action_priority,
            'response_timeline': response_timeline,
            'requires_human_approval': self._requires_human_approval(cyber_risk, operational_risk),
            'estimated_resolution_time': operational_assessment['estimated_downtime_minutes'],
            'decision_rationale': rationale,
            'emergency_contacts': self._get_emergency_contacts(primary_threat)
        }

    def _identify_primary_threat(self, cyber_risk: str, operational_risk: str) -> str:
        risk_scores = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

        cyber_score = risk_scores.get(cyber_risk, 0)
        op_score = risk_scores.get(operational_risk, 0)

        if cyber_score > op_score:
            return 'Cyber Attack'
        elif op_score > cyber_score:
            return 'Operational Failure'
        else:
            return 'Combined Cyber-Physical Threat'

    def _select_actions(self, cyber_risk: str, operational_risk: str,
                       fault_severity: str) -> List[str]:
        actions = []

        if cyber_risk == 'critical':
            actions.extend(self.action_library['critical_cyber'])
        elif cyber_risk == 'high':
            actions.extend(self.action_library['high_cyber'])

        if operational_risk == 'critical' or fault_severity == 'Critical':
            actions.extend(self.action_library['critical_operational'])
        elif operational_risk == 'high' or fault_severity == 'High':
            actions.extend(self.action_library['high_operational'])
        elif operational_risk == 'medium':
            actions.extend(self.action_library['medium_risk'])
        else:
            actions.extend(self.action_library['low_risk'])

        return list(dict.fromkeys(actions))

    def _get_stage_actions(self, affected_systems: List[str]) -> List[str]:
        stage_actions = []

        if 'Primary Treatment' in affected_systems:
            stage_actions.extend(self.stage_actions['P2'])
        if 'Distribution System' in affected_systems:
            stage_actions.extend(self.stage_actions['P6'])
        if 'Control System' in affected_systems:
            stage_actions.append('Switch to manual control mode')
        if 'Safety Systems' in affected_systems:
            stage_actions.append('Activate emergency safety protocols')

        return stage_actions

    def _prioritize_actions(self, actions: List[str], priority: int) -> Dict:
        if priority == 1:
            return {
                'immediate': actions[:3] if len(actions) >= 3 else actions,
                'short_term': actions[3:6] if len(actions) > 3 else [],
                'ongoing': actions[6:] if len(actions) > 6 else []
            }
        elif priority == 2:
            return {
                'immediate': actions[:2] if len(actions) >= 2 else actions,
                'short_term': actions[2:5] if len(actions) > 2 else [],
                'ongoing': actions[5:] if len(actions) > 5 else []
            }
        else:
            return {
                'immediate': actions[:1] if actions else [],
                'short_term': actions[1:4] if len(actions) > 1 else [],
                'ongoing': actions[4:] if len(actions) > 4 else []
            }

    def _calculate_response_timeline(self, cyber_risk: str, operational_risk: str,
                                    fault_severity: str) -> str:
        if cyber_risk == 'critical' or operational_risk == 'critical':
            return 'IMMEDIATE (0-5 minutes)'
        elif cyber_risk == 'high' or operational_risk == 'high' or fault_severity == 'High':
            return 'URGENT (5-15 minutes)'
        elif cyber_risk == 'medium' or operational_risk == 'medium':
            return 'PRIORITY (15-60 minutes)'
        else:
            return 'STANDARD (1-24 hours)'

    def _requires_human_approval(self, cyber_risk: str, operational_risk: str) -> bool:
        return cyber_risk == 'critical' or operational_risk == 'critical'

    def _generate_rationale(self, primary_threat: str, cyber_assessment: Dict,
                           operational_assessment: Dict) -> str:
        rationale = f"Decision based on {primary_threat.lower()}. "

        if cyber_assessment['risk_level'] in ['high', 'critical']:
            rationale += f"Cyber threat detected: {cyber_assessment['attack_signature']}. "

        if operational_assessment['risk_level'] in ['high', 'critical']:
            rationale += f"Operational impact: {operational_assessment['fault_severity']} severity, "
            rationale += f"{operational_assessment['performance_degradation']}. "

        rationale += f"Estimated recovery: {operational_assessment['estimated_downtime_minutes']} minutes."

        return rationale

    def _get_emergency_contacts(self, primary_threat: str) -> List[str]:
        contacts = {
            'Cyber Attack': ['Security Operations Center', 'IT Incident Response Team', 'Plant Manager'],
            'Operational Failure': ['Plant Engineer', 'Maintenance Team', 'Safety Officer'],
            'Combined Cyber-Physical Threat': ['Emergency Response Team', 'Plant Manager', 'Security Team', 'Safety Officer']
        }
        return contacts.get(primary_threat, ['Plant Manager'])


class CoordinationAgent:
    """Manages communication and workflow between all agents."""

    def __init__(self):
        self.perception_agent = None
        self.fault_detection_agent = None
        self.cyber_risk_agent = None
        self.operational_risk_agent = None
        self.decision_agent = None
        self.risk_mapping_agent = None
        self.execution_log = []
        self.system_state = 'INITIALIZED'

    def register_agents(self, perception, fault_detection, cyber_risk,
                       operational_risk, decision_making, risk_mapping=None):
        """Register all agents with coordinator."""
        self.perception_agent = perception
        self.fault_detection_agent = fault_detection
        self.cyber_risk_agent = cyber_risk
        self.operational_risk_agent = operational_risk
        self.decision_agent = decision_making
        self.risk_mapping_agent = risk_mapping

        self.system_state = 'READY'
        self._log_event('All agents registered', 'INFO')

    def process_data(self, raw_data: pd.DataFrame) -> Dict:
        """Execute full agent pipeline on incoming data."""
        self._log_event('Starting data processing pipeline', 'INFO')
        self.system_state = 'PROCESSING'

        try:
            X_processed, timestamps = self.perception_agent.preprocess(raw_data)
            detection_results = self.fault_detection_agent.detect(X_processed)

            cyber_assessment = self.cyber_risk_agent.assess_risk(
                detection_results, timestamps
            )
            operational_assessment = self.operational_risk_agent.assess_risk(
                detection_results, cyber_assessment
            )

            decisions = self.decision_agent.decide(
                cyber_assessment, operational_assessment
            )

            # Map anomalies to system-level risks
            risk_mapping_results = None
            if self.risk_mapping_agent:
                try:
                    risk_mapping_results = self.risk_mapping_agent.map_anomalies_to_risks({
                        'predictions': detection_results['predictions'],
                        'attack_probabilities': detection_results['attack_probabilities'],
                        'sensor_data': raw_data
                    })
                    self._log_event('Risk mapping completed', 'INFO')
                except Exception as e:
                    self._log_event(f'Risk mapping error: {str(e)}', 'WARNING')
                    risk_mapping_results = None

            self.system_state = 'COMPLETED'
            self._log_event('Pipeline completed successfully', 'SUCCESS')

            result = {
                'status': 'SUCCESS',
                'system_state': self.system_state,
                'detection_results': detection_results,
                'cyber_assessment': cyber_assessment,
                'operational_assessment': operational_assessment,
                'decisions': decisions,
                'execution_log': self.execution_log.copy()
            }

            # Add risk mapping results if available
            if risk_mapping_results:
                result['risk_mapping'] = risk_mapping_results

            return result

        except Exception as e:
            self.system_state = 'ERROR'
            self._log_event(f'Pipeline error: {str(e)}', 'ERROR')
            return {
                'status': 'ERROR',
                'system_state': self.system_state,
                'error': str(e),
                'execution_log': self.execution_log.copy()
            }

    def _log_event(self, message: str, level: str):
        """Log system events."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.execution_log.append(log_entry)

    def get_system_status(self) -> str:
        """Get current system state."""
        return self.system_state

    def generate_report(self, results: Dict) -> str:
        """Generate human-readable system report."""
        if results['status'] != 'SUCCESS':
            return f"SYSTEM ERROR: {results.get('error', 'Unknown error')}"

        report = []
        report.append("="*70)
        report.append("INTEGRATED AGENTIC AI SYSTEM - ANALYSIS REPORT")
        report.append("="*70)

        det = results['detection_results']
        report.append("\nDETECTION SUMMARY:")
        report.append(f"   Samples Analyzed: {len(det['predictions'])}")
        report.append(f"   Anomalies Detected: {det['num_anomalies']}")
        report.append(f"   Anomaly Rate: {det['anomaly_rate']*100:.2f}%")

        cyber = results['cyber_assessment']
        ops = results['operational_assessment']
        report.append(f"\nCYBER RISK: {cyber['risk_level'].upper()}")
        report.append(f"   Score: {cyber['cyber_risk_score']:.3f}")
        report.append(f"   Pattern: {cyber['attack_signature']}")

        report.append(f"\nOPERATIONAL RISK: {ops['risk_level'].upper()}")
        report.append(f"   Score: {ops['operational_risk_score']:.3f}")
        report.append(f"   Severity: {ops['fault_severity']}")
        report.append(f"   Downtime: {ops['estimated_downtime_minutes']} min")

        # Add risk mapping information if available
        if 'risk_mapping' in results and results['risk_mapping']:
            risk_map = results['risk_mapping']
            majority = risk_map.get('majority_risk', {})

            if majority.get('category') != 'None':
                report.append(f"\nRISK MAPPING ANALYSIS:")
                report.append(f"   Dominant Risk: {majority['category']}")
                report.append(f"   Occurrence: {majority['count']} instances ({majority['percentage']:.1f}%)")
                report.append(f"   Severity: {majority['severity']}")
                report.append(f"   Affected Stages: {', '.join(majority['affected_stages'])}")

                if majority.get('affected_sensors'):
                    sensors_str = ', '.join(majority['affected_sensors'][:3])
                    report.append(f"   Key Sensors: {sensors_str}")

        dec = results['decisions']
        report.append(f"\nRECOMMENDED ACTIONS:")
        report.append(f"   Primary Threat: {dec['primary_threat']}")
        report.append(f"   Response Timeline: {dec['response_timeline']}")
        report.append(f"   Human Approval Required: {dec['requires_human_approval']}")

        report.append("\n   Immediate Actions:")
        for action in dec['action_priority']['immediate']:
            report.append(f"   • {action}")

        if dec['stage_specific_actions']:
            report.append("\n   Stage-Specific Actions:")
            for action in dec['stage_specific_actions'][:3]:
                report.append(f"   • {action}")

        report.append(f"\nEMERGENCY CONTACTS:")
        for contact in dec['emergency_contacts']:
            report.append(f"   • {contact}")

        report.append("\n" + "="*70)

        return "\n".join(report)
