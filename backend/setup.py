"""
Setup script for the Multi-Agent ICS Backend
Prepares the environment and generates necessary data
"""

import os
import sys
import subprocess

def create_directories():
    """Create necessary directory structure"""
    print("Creating directory structure...")
    directories = ['data', 'models', 'logs']

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ Created {directory}/")


def generate_dummy_data():
    """Generate dummy datasets"""
    print("\nGenerating dummy datasets...")
    try:
        from generate_dummy_data import generate_demo_datasets
        generate_demo_datasets()
        print("  ✓ Dummy data generated successfully!")
        return True
    except Exception as e:
        print(f"  ✗ Error generating data: {str(e)}")
        return False


def check_agent_code():
    """Check if agent code exists"""
    print("\nChecking for agent code...")
    if os.path.exists('agents.py'):
        print("  ✓ agents.py found!")
        return True
    else:
        print("  ✗ agents.py not found!")
        print("\n  Please make sure agents.py exists in this directory.")
        print("  The file should include:")
        print("    - PerceptionAgent")
        print("    - FaultDetectionAgent")
        print("    - CyberRiskAssessmentAgent")
        print("    - OperationalRiskAssessmentAgent")
        print("    - DecisionMakingAgent")
        print("    - CoordinationAgent")
        print("    - load_and_merge_data function")
        return False


def check_models():
    """Check if trained models exist"""
    print("\nChecking for trained models...")
    required_models = [
        'models/perception_agent.pkl',
        'models/fault_detection_model.pkl'
    ]

    all_exist = True
    for model_path in required_models:
        if os.path.exists(model_path):
            print(f"  ✓ {model_path} found!")
        else:
            print(f"  ✗ {model_path} not found!")
            all_exist = False

    if not all_exist:
        print("\n  You need to train the models first.")
        print("  Run your training script to generate:")
        print("    - perception_agent.pkl")
        print("    - fault_detection_model.pkl")
        print("  Then move them to the models/ directory")

    return all_exist


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("  ✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("  ✗ Error installing dependencies")
        return False


def main():
    print("="*60)
    print("Multi-Agent ICS Backend - Setup")
    print("="*60)

    # Step 1: Create directories
    create_directories()

    # Step 2: Generate dummy data
    data_success = generate_dummy_data()

    # Step 3: Check for agent code
    agent_exists = check_agent_code()

    # Step 4: Check for trained models
    models_exist = check_models()

    # Step 5: Install dependencies
    print("\nWould you like to install dependencies now? (y/n): ", end='')
    try:
        response = input().lower()
    except:
        response = 'n'

    if response == 'y':
        deps_installed = install_dependencies()
    else:
        print("  Skipping dependency installation")
        deps_installed = False

    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)
    print(f"  Directory structure: ✓")
    print(f"  Dummy data: {'✓' if data_success else '✗'}")
    print(f"  Agent code: {'✓' if agent_exists else '✗'}")
    print(f"  Trained models: {'✗ (Need to train)' if not models_exist else '✓'}")
    print(f"  Dependencies: {'✓' if deps_installed else '✗ (Run: pip install -r requirements.txt)'}")

    if agent_exists and data_success:
        print("\n✓ Data generation complete!")
        if not models_exist:
            print("\n⚠ Next step: Train your models")
            print("  1. Make sure you have output1.csv and output.csv in data/")
            print("  2. Run your agent training script")
            print("  3. It will create perception_agent.pkl and fault_detection_model.pkl")
            print("  4. These will be saved to models/ directory")
            print("  5. Then you can run: python app.py")
        else:
            print("\n✓ Everything ready! You can now run the server:")
            print("  python app.py")
    else:
        print("\n⚠ Setup incomplete. Please address the items marked with ✗ above.")

    print("="*60)


if __name__ == "__main__":
    main()
