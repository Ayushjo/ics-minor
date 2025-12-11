"""
Training Script for Multi-Agent ICS System
Trains the models and saves them for the backend to use
"""

from agents import PerceptionAgent, FaultDetectionAgent
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import os

if __name__ == "__main__":
    print("="*70)
    print("MULTI-AGENT ICS SYSTEM - MODEL TRAINING")
    print("="*70)

    # Check if data files exist
    if not os.path.exists('data/output1.csv') or not os.path.exists('data/output.csv'):
        print("\nData files not found!")
        print("Please run: python generate_dummy_data.py")
        exit(1)

    # Create models directory
    os.makedirs('models', exist_ok=True)

    print("\n[1/5] Loading data...")
    df1 = pd.read_csv('data/output1.csv')
    df2 = pd.read_csv('data/output.csv')

    # Merge datasets
    df_raw = pd.concat([df1, df2], ignore_index=True)
    df_raw = df_raw.sample(frac=1, random_state=42).reset_index(drop=True)
    df_raw = df_raw.drop_duplicates()

    print(f"Total samples: {len(df_raw)}")
    print(f"Label distribution:")
    print(df_raw['Normal/Attack'].value_counts())

    print("\n[2/5] Encoding labels...")
    le = LabelEncoder()
    df_raw['Normal/Attack'] = le.fit_transform(df_raw['Normal/Attack'])
    print(f"Label mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")

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
    print("  1. Run the backend: python app.py")
    print("  2. Backend will load these models automatically")
    print("  3. System ready for real-time monitoring!")

    print("\n" + "="*70)
