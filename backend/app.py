from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
import threading
import time
import json
from datetime import datetime
import sys
import os

# Import your existing agent system
from agents import (
    PerceptionAgent,
    FaultDetectionAgent,
    CyberRiskAssessmentAgent,
    OperationalRiskAssessmentAgent,
    DecisionMakingAgent,
    CoordinationAgent,
    load_and_merge_data
)

# Import Risk Mapping Agent
try:
    from risk_mapping import RiskMappingAgent, get_sensor_risk_matrix
    RISK_MAPPING_ENABLED = True
except ImportError:
    RiskMappingAgent = None
    get_sensor_risk_matrix = None
    RISK_MAPPING_ENABLED = False
    print("Risk mapping features not available")

# Import enhanced features
try:
    from enhanced_features import (
        HistoricalAnalytics,
        SensorAnalyzer,
        AttackPatternRecognizer,
        AlertSystem
    )
    ENHANCED_FEATURES_ENABLED = True
except ImportError:
    ENHANCED_FEATURES_ENABLED = False
    print("Enhanced features not available")

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
coordinator = None
perception_agent = None
fault_detector = None
risk_mapping_agent = None
test_data = None
simulation_running = False
simulation_thread = None

# Enhanced features instances
if ENHANCED_FEATURES_ENABLED:
    historical_analytics = HistoricalAnalytics(max_history=2000)
    sensor_analyzer = SensorAnalyzer()
    pattern_recognizer = AttackPatternRecognizer()
    alert_system = AlertSystem()
else:
    historical_analytics = sensor_analyzer = pattern_recognizer = alert_system = None

class DataSimulator:
    """Simulates real-time data streaming from the SWaT system"""

    def __init__(self, test_df, batch_size=50, delay=2):
        self.test_df = test_df
        self.batch_size = batch_size
        self.delay = delay  # seconds between batches
        self.current_index = 0
        self.is_running = False

    def get_next_batch(self):
        """Get the next batch of data"""
        if self.current_index >= len(self.test_df):
            self.current_index = 0  # Loop back to start

        end_idx = min(self.current_index + self.batch_size, len(self.test_df))
        batch = self.test_df.iloc[self.current_index:end_idx]
        self.current_index = end_idx

        return batch

    def reset(self):
        """Reset the simulator to the beginning"""
        self.current_index = 0


# Initialize the simulator
data_simulator = None


def initialize_system():
    """Initialize all agents and load the model"""
    global coordinator, perception_agent, fault_detector, risk_mapping_agent, test_data, data_simulator

    print("Initializing Multi-Agent System...")

    try:
        # Load pre-trained agents (assuming they were saved during training)
        perception_agent = PerceptionAgent()
        perception_agent.load('models/perception_agent.pkl')

        fault_detector = FaultDetectionAgent()
        fault_detector.load_model('models/fault_detection_model.pkl')

        # Initialize risk assessment and decision agents
        cyber_risk_agent = CyberRiskAssessmentAgent()
        operational_risk_agent = OperationalRiskAssessmentAgent()
        decision_agent = DecisionMakingAgent()

        # Initialize risk mapping agent
        if RISK_MAPPING_ENABLED:
            risk_mapping_agent = RiskMappingAgent()
            print("Risk Mapping Agent initialized")
        else:
            risk_mapping_agent = None

        # Create coordinator and register all agents
        coordinator = CoordinationAgent()
        coordinator.register_agents(
            perception_agent,
            fault_detector,
            cyber_risk_agent,
            operational_risk_agent,
            decision_agent,
            risk_mapping=risk_mapping_agent
        )

        # Load test data for simulation
        # Use dataset with anomalies for testing risk mapping
        data_file = 'data/realtime_simulation_with_anomalies.csv'
        if not os.path.exists(data_file):
            print(f"Anomaly dataset not found, using default")
            data_file = 'data/realtime_simulation_v2.csv'
        if not os.path.exists(data_file):
            print(f"Using fallback data")
            data_file = 'data/test_data.csv'
        test_data = pd.read_csv(data_file)
        print(f"Loaded {len(test_data)} samples from {data_file}")

        # Initialize data simulator
        data_simulator = DataSimulator(test_data, batch_size=50, delay=3)

        print("[OK] System initialized successfully!")
        return True

    except Exception as e:
        import traceback
        error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
        print(f"Error initializing system: {error_msg}")
        traceback.print_exc()
        return False


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system_state': coordinator.get_system_status() if coordinator else 'NOT_INITIALIZED',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/system/initialize', methods=['POST'])
def initialize():
    """Initialize the multi-agent system"""
    success = initialize_system()

    if success:
        return jsonify({
            'status': 'success',
            'message': 'System initialized successfully',
            'system_state': coordinator.get_system_status()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to initialize system'
        }), 500


@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Get current system status"""
    if coordinator is None:
        return jsonify({
            'status': 'error',
            'message': 'System not initialized'
        }), 400

    return jsonify({
        'status': 'success',
        'system_state': coordinator.get_system_status(),
        'simulation_running': simulation_running,
        'data_index': data_simulator.current_index if data_simulator else 0,
        'total_samples': len(test_data) if test_data is not None else 0
    })


@app.route('/api/process/batch', methods=['POST'])
def process_batch():
    """Process a single batch of data manually"""
    if coordinator is None:
        return jsonify({
            'status': 'error',
            'message': 'System not initialized'
        }), 400

    try:
        data = request.json
        batch_size = data.get('batch_size', 50)
        scenario = data.get('scenario', 'mixed')  # 'attack', 'normal', 'mixed'

        # Get data based on scenario
        if scenario == 'attack':
            batch = test_data[test_data['Normal/Attack'] == 1].iloc[:batch_size]
        elif scenario == 'normal':
            batch = test_data[test_data['Normal/Attack'] == 0].iloc[:batch_size]
        else:
            batch = data_simulator.get_next_batch()

        # Process through the multi-agent system
        results = coordinator.process_data(batch)

        # Format response
        response = format_results(results, batch)

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_data():
    """Upload custom CSV data for processing"""
    if coordinator is None:
        return jsonify({
            'status': 'error',
            'message': 'System not initialized'
        }), 400

    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400

        file = request.files['file']

        # Read CSV
        df = pd.read_csv(file)

        # Process the data
        results = coordinator.process_data(df)

        response = format_results(results, df)

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/risk-mapping/matrix', methods=['GET'])
def get_risk_mapping_matrix():
    """Get the sensor-to-risk mapping matrix"""
    if not RISK_MAPPING_ENABLED or get_sensor_risk_matrix is None:
        return jsonify({
            'status': 'error',
            'message': 'Risk mapping feature not available'
        }), 503

    try:
        matrix = get_sensor_risk_matrix()
        return jsonify({
            'status': 'success',
            'data': matrix
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/risk-mapping/current', methods=['GET'])
def get_current_risk_mapping():
    """Get current risk mapping analysis"""
    if not RISK_MAPPING_ENABLED or risk_mapping_agent is None:
        return jsonify({
            'status': 'error',
            'message': 'Risk mapping feature not available'
        }), 503

    try:
        # Get historical summary from the risk mapping agent
        summary = risk_mapping_agent.get_historical_risk_summary()

        return jsonify({
            'status': 'success',
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/risk-mapping/reset', methods=['POST'])
def reset_risk_mapping():
    """Reset risk mapping history"""
    if not RISK_MAPPING_ENABLED or risk_mapping_agent is None:
        return jsonify({
            'status': 'error',
            'message': 'Risk mapping feature not available'
        }), 503

    try:
        risk_mapping_agent.reset_history()
        return jsonify({
            'status': 'success',
            'message': 'Risk mapping history reset successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def format_results(results, batch_data):
    """Format the agent results for the frontend"""
    if results['status'] != 'SUCCESS':
        return {
            'status': 'error',
            'message': results.get('error', 'Unknown error'),
            'system_state': results['system_state']
        }

    detection = results['detection_results']
    cyber = results['cyber_assessment']
    ops = results['operational_assessment']
    decisions = results['decisions']

    # Calculate actual vs predicted for metrics
    y_true = (batch_data['Normal/Attack'] == 1).astype(int).values if 'Normal/Attack' in batch_data.columns else None
    y_pred = detection['predictions']

    metrics = None
    if y_true is not None:
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        metrics = {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, zero_division=0)),
            'f1_score': float(f1_score(y_true, y_pred, zero_division=0)),
            'true_attacks': int(y_true.sum()),
            'true_normal': int(len(y_true) - y_true.sum())
        }

    response = {
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'system_state': results['system_state'],
        'batch_info': {
            'total_samples': len(batch_data),
            'anomalies_detected': detection['num_anomalies'],
            'anomaly_rate': detection['anomaly_rate']
        },
        'detection': {
            'num_anomalies': detection['num_anomalies'],
            'anomaly_rate': detection['anomaly_rate'],
            'attack_probabilities': detection['attack_probability'].tolist()[:100],  # Limit for response size
            'predictions': detection['predictions'].tolist()[:100],
            'confidence': detection['confidence'].tolist()[:100]
        },
        'cyber_risk': {
            'score': cyber['cyber_risk_score'],
            'level': cyber['risk_level'],
            'avg_attack_probability': cyber['avg_attack_probability'],
            'max_attack_probability': cyber['max_attack_probability'],
            'attack_signature': cyber['attack_signature'],
            'threat_assessment': cyber['threat_assessment']
        },
        'operational_risk': {
            'score': ops['operational_risk_score'],
            'level': ops['risk_level'],
            'fault_severity': ops['fault_severity'],
            'affected_systems': ops['affected_systems'],
            'estimated_downtime': ops['estimated_downtime_minutes'],
            'safety_impact': ops['safety_impact'],
            'performance_degradation': ops['performance_degradation']
        },
        'decisions': {
            'primary_threat': decisions['primary_threat'],
            'recommended_actions': decisions['recommended_actions'][:5],  # Top 5
            'stage_specific_actions': decisions['stage_specific_actions'][:3],  # Top 3
            'action_priority': decisions['action_priority'],
            'response_timeline': decisions['response_timeline'],
            'requires_human_approval': decisions['requires_human_approval'],
            'emergency_contacts': decisions['emergency_contacts']
        },
        'metrics': metrics,
        'execution_log': results['execution_log'][-10:]  # Last 10 log entries
    }

    # Add risk mapping data if available
    if 'risk_mapping' in results and results['risk_mapping']:
        response['risk_mapping'] = results['risk_mapping']

    return response


def simulation_loop():
    """Background thread that simulates real-time data processing"""
    global simulation_running

    print("Starting simulation loop...")

    while simulation_running:
        try:
            # Get next batch from simulator
            batch = data_simulator.get_next_batch()

            # Process through agents
            results = coordinator.process_data(batch)

            # Format and emit to frontend
            formatted_results = format_results(results, batch)

            socketio.emit('real_time_update', formatted_results)

            # Sleep for the configured delay
            time.sleep(data_simulator.delay)

        except Exception as e:
            print(f"Error in simulation loop: {str(e)}")
            socketio.emit('error', {'message': str(e)})
            break

    print("Simulation loop stopped")


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


@socketio.on('start_simulation')
def handle_start_simulation(data):
    """Start the real-time simulation"""
    global simulation_running, simulation_thread

    if coordinator is None:
        emit('error', {'message': 'System not initialized'})
        return

    if simulation_running:
        emit('error', {'message': 'Simulation already running'})
        return

    # Configure simulator
    batch_size = data.get('batch_size', 50)
    delay = data.get('delay', 3)

    data_simulator.batch_size = batch_size
    data_simulator.delay = delay

    # Start simulation
    simulation_running = True
    simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
    simulation_thread.start()

    emit('simulation_started', {
        'status': 'success',
        'batch_size': batch_size,
        'delay': delay
    })


@socketio.on('stop_simulation')
def handle_stop_simulation():
    """Stop the real-time simulation"""
    global simulation_running

    simulation_running = False

    emit('simulation_stopped', {'status': 'success'})


@socketio.on('reset_simulation')
def handle_reset_simulation():
    """Reset the simulation to the beginning"""
    if data_simulator:
        data_simulator.reset()
        emit('simulation_reset', {'status': 'success'})


if __name__ == '__main__':
    # Initialize system on startup
    initialize_system()

    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
