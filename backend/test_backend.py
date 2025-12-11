"""
Quick test script to verify backend components
"""

import os
import sys

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from agents import (
            PerceptionAgent,
            FaultDetectionAgent,
            CyberRiskAssessmentAgent,
            OperationalRiskAssessmentAgent,
            DecisionMakingAgent,
            CoordinationAgent
        )
        print("  [OK] All agent classes imported successfully")
        return True
    except Exception as e:
        print(f"  [FAIL] Import error: {e}")
        return False

def test_models_exist():
    """Test if trained models exist"""
    print("\nTesting model files...")
    models = [
        'models/perception_agent.pkl',
        'models/fault_detection_model.pkl'
    ]

    all_exist = True
    for model in models:
        if os.path.exists(model):
            size = os.path.getsize(model) / (1024 * 1024)  # MB
            print(f"  [OK] {model} ({size:.2f} MB)")
        else:
            print(f"  [FAIL] {model} not found")
            all_exist = False

    return all_exist

def test_data_exists():
    """Test if data files exist"""
    print("\nTesting data files...")
    data_files = [
        'data/output1.csv',
        'data/output.csv',
        'data/test_data.csv',
        'data/realtime_data.csv'
    ]

    all_exist = True
    for file in data_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # MB
            print(f"  [OK] {file} ({size:.2f} MB)")
        else:
            print(f"  [FAIL] {file} not found")
            all_exist = False

    return all_exist

def test_agent_loading():
    """Test if agents can load models"""
    print("\nTesting agent initialization...")
    try:
        from agents import PerceptionAgent, FaultDetectionAgent

        perception = PerceptionAgent()
        perception.load('models/perception_agent.pkl')
        print("  [OK] PerceptionAgent loaded successfully")

        fault_detector = FaultDetectionAgent()
        fault_detector.load_model('models/fault_detection_model.pkl')
        print("  [OK] FaultDetectionAgent loaded successfully")

        return True
    except Exception as e:
        print(f"  [FAIL] Error loading agents: {e}")
        return False

def test_data_processing():
    """Test if data can be processed"""
    print("\nTesting data processing...")
    try:
        import pandas as pd
        from agents import (
            PerceptionAgent,
            FaultDetectionAgent,
            CyberRiskAssessmentAgent,
            OperationalRiskAssessmentAgent,
            DecisionMakingAgent,
            CoordinationAgent
        )

        # Load agents
        perception = PerceptionAgent()
        perception.load('models/perception_agent.pkl')

        fault_detector = FaultDetectionAgent()
        fault_detector.load_model('models/fault_detection_model.pkl')

        cyber_risk = CyberRiskAssessmentAgent()
        operational_risk = OperationalRiskAssessmentAgent()
        decision = DecisionMakingAgent()

        coordinator = CoordinationAgent()
        coordinator.register_agents(
            perception,
            fault_detector,
            cyber_risk,
            operational_risk,
            decision
        )

        # Load test data
        test_data = pd.read_csv('data/test_data.csv')
        sample_batch = test_data.iloc[:10]

        # Process batch
        results = coordinator.process_data(sample_batch)

        if results['status'] == 'SUCCESS':
            print("  [OK] Data processed successfully")
            print(f"    - Detected {results['detection_results']['num_anomalies']} anomalies")
            print(f"    - Cyber risk: {results['cyber_assessment']['risk_level']}")
            print(f"    - Operational risk: {results['operational_assessment']['risk_level']}")
            return True
        else:
            print(f"  [FAIL] Processing failed: {results.get('error')}")
            return False

    except Exception as e:
        print(f"  [FAIL] Error processing data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*70)
    print("BACKEND SYSTEM TEST")
    print("="*70)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Model Files", test_models_exist()))
    results.append(("Data Files", test_data_exists()))
    results.append(("Agent Loading", test_agent_loading()))
    results.append(("Data Processing", test_data_processing()))

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    for test_name, passed in results:
        status = "[OK] PASSED" if passed else "[FAIL] FAILED"
        print(f"{test_name:20s} {status}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n" + "="*70)
        print("ALL TESTS PASSED! Backend is ready to run.")
        print("="*70)
        print("\nStart the server with: python app.py")
        print("Then test with: curl http://localhost:5000/api/health")
    else:
        print("\nSome tests failed. Please check the errors above.")

    sys.exit(0 if all_passed else 1)
