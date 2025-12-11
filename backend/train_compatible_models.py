"""
Training Script for Multi-Agent ICS System - Using Compatible Data
Trains models using the compatible realistic data (FIT101 format, not FIT-101)
"""

from agents import PerceptionAgent, FaultDetectionAgent
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import os

if __name__ == "__main__":
    print("="*70)
    print("MULTI-AGENT ICS SYSTEM - COMPATIBLE MODEL TRAINING")
    print("="*70)

    # Check if compatible data exists
    if not os.path.exists('data/realtime_simulation_v2.csv'):
        print("\nCompatible data file not found!")
        print("Please run: python generate_compatible_data.py")
        exit(1)

    # Create models directory
    os.makedirs('models', exist_ok=True)

    print("\n[1/5] Loading compatible data...")
    df_raw = pd.read_csv('data/realtime_simulation_v2.csv')

    print(f"Total samples: {len(df_raw)}")
    print(f"Columns: {list(df_raw.columns[:10])}...")  # Show first 10 columns
    print(f"\nLabel distribution:")
    print(df_raw['Normal/Attack'].value_counts())

    # Verify schema (should be FIT101, not FIT-101)
    sensor_sample = [col for col in df_raw.columns if col.startswith('FIT')][:3]
    print(f"\nSensor name format check: {sensor_sample}")
    if any('-' in col for col in sensor_sample):
        print("WARNING: Data still contains hyphens in sensor names!")
        exit(1)
    else:
        print("[OK] Schema verified: Using correct format (FIT101, not FIT-101)")

    print("\n[2/5] Preparing labels...")
    # Labels are already 0/1 in the compatible data
    print(f"Label mapping: 0=Normal, 1=Attack")
    print(f"Attack samples: {df_raw['Normal/Attack'].sum()}")
    print(f"Normal samples: {len(df_raw) - df_raw['Normal/Attack'].sum()}")

    print("\n[3/5] Splitting data...")
    train_df, test_df = train_test_split(
        df_raw,
        test_size=0.2,
        random_state=42,
        stratify=df_raw['Normal/Attack']
    )

    print(f"Train set: {len(train_df)} samples")
    print(f"Test set: {len(test_df)} samples")

    print("\n[4/5] Training PerceptionAgent...")
    perception_agent = PerceptionAgent()
    perception_agent.fit(train_df)

    X_train, _ = perception_agent.preprocess(train_df)
    X_test, _ = perception_agent.preprocess(test_df)

    y_train = train_df['Normal/Attack'].values
    y_test = test_df['Normal/Attack'].values

    print(f"Training features shape: {X_train.shape}")
    print(f"Testing features shape: {X_test.shape}")

    print("\n[5/5] Training FaultDetectionAgent (Random Forest)...")
    print("This may take 2-3 minutes...")
    fault_detector = FaultDetectionAgent()
    fault_detector.train(X_train, y_train)

    print("\nEvaluating on test set...")
    results_test = fault_detector.detect(X_test)

    print("\nClassification Report:")
    print(classification_report(y_test, results_test['predictions'],
                                target_names=['Normal', 'Attack']))

    acc = accuracy_score(y_test, results_test['predictions'])
    print(f"\nTest Accuracy: {acc*100:.2f}%")

    print("\nSaving models...")
    perception_agent.save('models/perception_agent.pkl')
    fault_detector.save_model('models/fault_detection_model.pkl')

    print("\n" + "="*70)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)

    print("\nModels saved:")
    print("  - models/perception_agent.pkl")
    print("  - models/fault_detection_model.pkl")

    print("\nNext steps:")
    print("  1. Kill any running backend processes")
    print("  2. Run the backend: python app.py")
    print("  3. Backend will load these NEW models automatically")
    print("  4. System ready for real-time monitoring with realistic data!")

    print("\n" + "="*70)
