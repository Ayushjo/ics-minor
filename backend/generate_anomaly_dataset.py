"""
Generate a dataset with realistic anomalies for testing risk mapping
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Generating dataset with anomalies...")

# Load existing dataset
df = pd.read_csv('data/realtime_simulation_v2.csv')
print(f"Loaded {len(df)} samples")

# Create a copy for modification
df_anomaly = df.copy()

# We'll inject anomalies into 40% of the data
total_samples = len(df_anomaly)
anomaly_count = int(total_samples * 0.4)

# Select random indices for anomalies
np.random.seed(42)
anomaly_indices = np.random.choice(total_samples, anomaly_count, replace=False)

print(f"Injecting {anomaly_count} anomalies...")

# Define sensor groups and their anomaly types
# Each group maps to specific risk categories

# Risk 1: Water Overflow - Level sensors
level_sensors = ['LIT-101', 'LIT-301', 'LIT-501', 'LIT-401', 'LIT-601']

# Risk 2: Pump Damage - Flow and pressure sensors
flow_sensors = ['FIT-101', 'FIT-201', 'FIT-301', 'FIT-401', 'FIT-501', 'FIT-502', 'FIT-503', 'FIT-601']
pressure_sensors = ['PIT-501', 'PIT-502', 'DPIT-101', 'DPIT-301', 'DPIT-601']

# Risk 3: Water Quality - Analyzer sensors
quality_sensors = ['AIT-101', 'AIT-102', 'AIT-201', 'AIT-202', 'AIT-203',
                   'AIT-301', 'AIT-302', 'AIT-303', 'AIT-401', 'AIT-402',
                   'AIT-501', 'AIT-601', 'AIT-602']

# Risk 4: Chemical Dosing - Chemical-related sensors
chemical_sensors = ['AIT-201', 'AIT-202', 'AIT-203', 'AIT-401', 'AIT-402']

# Risk 5: Process Interruption - Pumps and valves
pump_sensors = ['P-101', 'P-102', 'P-201', 'P-202', 'P-203', 'P-204',
                'P-301', 'P-302', 'P-401', 'P-402', 'P-403',
                'P-501', 'P-502', 'P-601', 'P-602', 'P-603']
valve_sensors = ['MV-101', 'MV-201', 'MV-301', 'MV-302']

# Inject anomalies
for idx in anomaly_indices:
    # Choose a risk type randomly
    risk_type = np.random.choice([
        'overflow', 'pump_damage', 'water_quality',
        'chemical_dosing', 'process_interruption'
    ], p=[0.25, 0.25, 0.20, 0.15, 0.15])  # Distribution of risk types

    if risk_type == 'overflow':
        # High level in tanks
        for sensor in level_sensors:
            if sensor in df_anomaly.columns:
                # Get normal value
                normal_val = df_anomaly.loc[idx, sensor]
                # Spike to very high (150-200% of normal)
                spike = normal_val * np.random.uniform(1.5, 2.0)
                df_anomaly.loc[idx, sensor] = spike

    elif risk_type == 'pump_damage':
        # Abnormal flow or pressure
        # Low flow (dry run)
        for sensor in flow_sensors[:2]:  # Affect 2 flow sensors
            if sensor in df_anomaly.columns:
                normal_val = df_anomaly.loc[idx, sensor]
                # Drop to very low (20-40% of normal)
                df_anomaly.loc[idx, sensor] = normal_val * np.random.uniform(0.2, 0.4)

        # High pressure (overpressure)
        for sensor in pressure_sensors[:1]:  # Affect 1 pressure sensor
            if sensor in df_anomaly.columns:
                normal_val = df_anomaly.loc[idx, sensor]
                # Spike to very high (180-250% of normal)
                df_anomaly.loc[idx, sensor] = normal_val * np.random.uniform(1.8, 2.5)

    elif risk_type == 'water_quality':
        # Abnormal analyzer readings
        for sensor in np.random.choice(quality_sensors, 3, replace=False):
            if sensor in df_anomaly.columns:
                normal_val = df_anomaly.loc[idx, sensor]
                # Random spike or drop
                if np.random.random() > 0.5:
                    df_anomaly.loc[idx, sensor] = normal_val * np.random.uniform(1.6, 2.2)
                else:
                    df_anomaly.loc[idx, sensor] = normal_val * np.random.uniform(0.3, 0.6)

    elif risk_type == 'chemical_dosing':
        # Chemical dosing issues
        for sensor in chemical_sensors:
            if sensor in df_anomaly.columns:
                normal_val = df_anomaly.loc[idx, sensor]
                # Significant deviation
                df_anomaly.loc[idx, sensor] = normal_val * np.random.uniform(0.4, 1.8)

    elif risk_type == 'process_interruption':
        # Pump/valve failures
        for sensor in np.random.choice(pump_sensors, 2, replace=False):
            if sensor in df_anomaly.columns:
                # Binary sensors - flip to opposite state
                df_anomaly.loc[idx, sensor] = 1 - df_anomaly.loc[idx, sensor]

# Mark anomalies in the dataset
df_anomaly['Normal/Attack'] = 0  # Normal
df_anomaly.loc[anomaly_indices, 'Normal/Attack'] = 1  # Attack/Anomaly

# Add timestamp if not present
if 'Timestamp' not in df_anomaly.columns:
    start_time = datetime.now()
    df_anomaly['Timestamp'] = [
        (start_time + timedelta(seconds=i*3)).isoformat()
        for i in range(len(df_anomaly))
    ]

# Save the new dataset
output_file = 'data/realtime_simulation_with_anomalies.csv'
df_anomaly.to_csv(output_file, index=False)

print(f"\n✓ Dataset saved to: {output_file}")
print(f"✓ Total samples: {len(df_anomaly)}")
print(f"✓ Anomalies: {anomaly_count} ({(anomaly_count/total_samples)*100:.1f}%)")
print(f"✓ Normal samples: {total_samples - anomaly_count} ({((total_samples-anomaly_count)/total_samples)*100:.1f}%)")

# Print anomaly distribution
print("\n📊 Anomaly Distribution:")
anomaly_df = df_anomaly[df_anomaly['Normal/Attack'] == 1]
print(f"   Total anomalies: {len(anomaly_df)}")

# Sample some anomalies
print("\n🔍 Sample anomalies created:")
sample_anomalies = df_anomaly[df_anomaly['Normal/Attack'] == 1].head(3)
for idx, row in sample_anomalies.iterrows():
    print(f"   Sample {idx}: Anomaly in multiple sensors")

print("\n✅ Done! Dataset ready for testing risk mapping.")
print("\nNext step: Update backend/app.py to use this file:")
print("   Change: data_file = 'data/realtime_simulation_with_anomalies.csv'")
