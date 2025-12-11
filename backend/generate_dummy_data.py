"""
Dummy Data Generator for SWaT System Simulation
Generates realistic-looking sensor data with controlled attack scenarios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class SWaTDataGenerator:
    """Generate dummy SWaT sensor data for demonstration"""

    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)

        # Define sensor ranges for each stage (based on SWaT system)
        self.sensor_specs = {
            # Stage 1 - Raw Water Supply
            'FIT-101': (0, 2.5),      # Flow meter
            'LIT-101': (500, 1200),    # Level sensor
            'P-101': (0, 1),           # Pump status
            'P-102': (0, 1),           # Pump status
            'MV-101': (0, 2),          # Motorized valve

            # Stage 2 - Chemical Dosing
            'FIT-201': (0, 1.5),
            'AIT-201': (0, 500),       # Analyzer
            'AIT-202': (0, 500),
            'P-201': (0, 1),
            'P-202': (0, 1),
            'P-203': (0, 1),

            # Stage 3 - Ultrafiltration
            'FIT-301': (0, 3.0),
            'LIT-301': (300, 1000),
            'DPIT-301': (0, 10),       # Differential pressure
            'P-301': (0, 1),
            'P-302': (0, 1),

            # Stage 4 - UV Dechlorination
            'FIT-401': (0, 2.5),
            'LIT-401': (200, 800),
            'AIT-401': (0, 100),
            'P-401': (0, 1),
            'P-402': (0, 1),

            # Stage 5 - Reverse Osmosis
            'FIT-501': (0, 2.0),
            'LIT-501': (300, 900),
            'PIT-501': (0, 15),        # Pressure
            'P-501': (0, 1),
            'P-502': (0, 1),

            # Stage 6 - Product Distribution
            'FIT-601': (0, 3.5),
            'LIT-601': (400, 1100),
            'P-601': (0, 1),
            'P-602': (0, 1),
        }

        self.sensor_names = list(self.sensor_specs.keys())

        # Attack patterns
        self.attack_patterns = [
            'sensor_spike',
            'sensor_drop',
            'sensor_flatline',
            'actuator_override',
            'pump_manipulation',
            'valve_manipulation'
        ]

    def generate_normal_data(self, n_samples=1000, start_time=None):
        """Generate normal operation data"""
        if start_time is None:
            start_time = datetime.now()

        data = {}

        # Generate timestamps
        timestamps = [start_time + timedelta(seconds=i) for i in range(n_samples)]
        data['Timestamp'] = timestamps

        # Generate sensor readings
        for sensor, (min_val, max_val) in self.sensor_specs.items():
            if sensor.startswith('P-') or sensor.startswith('MV-'):
                # Binary actuators (pumps, valves)
                # Normal operation: mostly on (1) with occasional switching
                base_state = np.random.choice([0, 1], size=n_samples, p=[0.2, 0.8])
                data[sensor] = base_state
            else:
                # Continuous sensors - generate smooth time series
                base_value = (min_val + max_val) / 2
                variation = (max_val - min_val) * 0.15

                # Create smooth signal with random walk
                values = []
                current = base_value
                for _ in range(n_samples):
                    current += np.random.normal(0, variation * 0.1)
                    current = np.clip(current, min_val, max_val)
                    values.append(current)

                data[sensor] = values

        # Normal/Attack label
        data['Normal/Attack'] = ['Normal'] * n_samples

        df = pd.DataFrame(data)
        return df

    def inject_attack(self, df, attack_type, start_idx, duration, affected_sensors=None):
        """Inject an attack pattern into normal data"""
        end_idx = min(start_idx + duration, len(df))

        if affected_sensors is None:
            # Random subset of sensors
            n_affected = random.randint(2, 5)
            affected_sensors = random.sample(self.sensor_names, n_affected)

        df_attacked = df.copy()

        for sensor in affected_sensors:
            min_val, max_val = self.sensor_specs[sensor]

            if attack_type == 'sensor_spike':
                # Sudden spike in sensor values
                spike_value = max_val * 1.5
                df_attacked.loc[start_idx:end_idx, sensor] = spike_value

            elif attack_type == 'sensor_drop':
                # Sudden drop to minimum
                df_attacked.loc[start_idx:end_idx, sensor] = min_val * 0.5

            elif attack_type == 'sensor_flatline':
                # Sensor stuck at one value
                stuck_value = df_attacked.loc[start_idx, sensor]
                df_attacked.loc[start_idx:end_idx, sensor] = stuck_value

            elif attack_type == 'actuator_override':
                # Actuator controlled by attacker
                if sensor.startswith('P-') or sensor.startswith('MV-'):
                    # Rapid switching
                    override_pattern = [random.choice([0, 1, 2]) for _ in range(end_idx - start_idx + 1)]
                    df_attacked.loc[start_idx:end_idx, sensor] = override_pattern

            elif attack_type == 'pump_manipulation':
                # Turn pumps on/off unexpectedly
                if sensor.startswith('P-'):
                    # Force opposite state
                    df_attacked.loc[start_idx:end_idx, sensor] = 1 - df_attacked.loc[start_idx:end_idx, sensor]

            elif attack_type == 'valve_manipulation':
                # Manipulate valve positions
                if sensor.startswith('MV-'):
                    df_attacked.loc[start_idx:end_idx, sensor] = 2  # Force open

        # Mark as attack
        df_attacked.loc[start_idx:end_idx, 'Normal/Attack'] = 'Attack'

        return df_attacked

    def generate_mixed_data(self, n_samples=5000, attack_probability=0.15):
        """Generate data with random attack injections"""
        # Generate base normal data
        df = self.generate_normal_data(n_samples)

        # Inject attacks at random intervals
        current_idx = 0
        while current_idx < n_samples:
            # Random normal period
            normal_duration = random.randint(100, 300)
            current_idx += normal_duration

            if current_idx >= n_samples:
                break

            # Randomly decide if attack occurs
            if random.random() < attack_probability:
                attack_type = random.choice(self.attack_patterns)
                attack_duration = random.randint(20, 100)
                affected = random.sample(self.sensor_names, random.randint(2, 4))

                df = self.inject_attack(df, attack_type, current_idx, attack_duration, affected)
                current_idx += attack_duration

        return df

    def save_dataset(self, df, filepath):
        """Save generated dataset to CSV"""
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        print(f"  Total samples: {len(df)}")
        print(f"  Attack samples: {(df['Normal/Attack'] == 'Attack').sum()}")
        print(f"  Normal samples: {(df['Normal/Attack'] == 'Normal').sum()}")


def generate_demo_datasets():
    """Generate demonstration datasets"""
    generator = SWaTDataGenerator()

    print("Generating demonstration datasets...")

    # 1. Training data (mostly normal)
    print("\n1. Training data...")
    train_normal = generator.generate_normal_data(n_samples=8000)
    train_attacks = generator.generate_mixed_data(n_samples=2000, attack_probability=1.0)
    train_df = pd.concat([train_normal, train_attacks], ignore_index=True)
    train_df = train_df.sample(frac=1).reset_index(drop=True)  # Shuffle
    generator.save_dataset(train_df, 'data/output1.csv')

    # 2. Additional normal data
    print("\n2. Additional normal data...")
    normal_df = generator.generate_normal_data(n_samples=5000)
    generator.save_dataset(normal_df, 'data/output.csv')

    # 3. Test data (mixed)
    print("\n3. Test data...")
    test_df = generator.generate_mixed_data(n_samples=3000, attack_probability=0.2)
    generator.save_dataset(test_df, 'data/test_data.csv')

    # 4. Real-time simulation data
    print("\n4. Real-time simulation data...")
    realtime_df = generator.generate_mixed_data(n_samples=10000, attack_probability=0.15)
    generator.save_dataset(realtime_df, 'data/realtime_data.csv')

    print("\n✓ All datasets generated successfully!")


if __name__ == "__main__":
    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Generate datasets
    generate_demo_datasets()
