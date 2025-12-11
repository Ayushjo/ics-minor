"""
Compatible Data Generator - Matches Original SWaT Schema
Generates realistic attack data with exact column names from original system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class CompatibleSWaTGenerator:
    """Generate data matching original schema with realistic attack patterns"""

    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)

        # Exact sensor specifications matching original schema
        self.sensor_specs = {
            # Stage 1 - Raw Water Supply
            'FIT101': {'range': (1.8, 2.2), 'normal': 2.0, 'noise': 0.05},
            'LIT101': {'range': (800, 1000), 'normal': 900, 'noise': 15},
            'MV101': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P101': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P102': {'range': (0, 2), 'normal': 1, 'noise': 0.1},

            # Stage 2 - Chemical Dosing
            'AIT201': {'range': (200, 400), 'normal': 300, 'noise': 12},
            'AIT202': {'range': (180, 380), 'normal': 280, 'noise': 10},
            'AIT203': {'range': (150, 300), 'normal': 225, 'noise': 8},
            'FIT201': {'range': (1.0, 1.4), 'normal': 1.2, 'noise': 0.03},
            'MV201': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P201': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P202': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P203': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P204': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P205': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P206': {'range': (0, 2), 'normal': 1, 'noise': 0.1},

            # Stage 3 - Ultrafiltration
            'DPIT301': {'range': (3, 8), 'normal': 5.5, 'noise': 0.3},
            'FIT301': {'range': (2.2, 2.8), 'normal': 2.5, 'noise': 0.06},
            'LIT301': {'range': (600, 900), 'normal': 750, 'noise': 20},
            'MV301': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'MV302': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'MV303': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'MV304': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P301': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P302': {'range': (0, 2), 'normal': 1, 'noise': 0.1},

            # Stage 4 - UV Dechlorination
            'AIT401': {'range': (30, 90), 'normal': 60, 'noise': 4},
            'AIT402': {'range': (25, 85), 'normal': 55, 'noise': 3.5},
            'FIT401': {'range': (1.8, 2.4), 'normal': 2.1, 'noise': 0.05},
            'LIT401': {'range': (400, 700), 'normal': 550, 'noise': 18},
            'P401': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P402': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P403': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P404': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'UV401': {'range': (0, 100), 'normal': 85, 'noise': 5},

            # Stage 5 - Reverse Osmosis
            'AIT501': {'range': (50, 150), 'normal': 100, 'noise': 6},
            'AIT502': {'range': (45, 140), 'normal': 95, 'noise': 5.5},
            'AIT503': {'range': (40, 130), 'normal': 90, 'noise': 5},
            'AIT504': {'range': (35, 125), 'normal': 85, 'noise': 4.5},
            'FIT501': {'range': (1.5, 2.0), 'normal': 1.75, 'noise': 0.04},
            'FIT502': {'range': (0.8, 1.3), 'normal': 1.05, 'noise': 0.03},
            'FIT503': {'range': (0.6, 1.1), 'normal': 0.85, 'noise': 0.02},
            'FIT504': {'range': (0.5, 1.0), 'normal': 0.75, 'noise': 0.02},
            'P501': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P502': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'PIT501': {'range': (20, 40), 'normal': 30, 'noise': 1.5},
            'PIT502': {'range': (15, 35), 'normal': 25, 'noise': 1.2},
            'PIT503': {'range': (10, 30), 'normal': 20, 'noise': 1.0},

            # Stage 6 - Backwash
            'FIT601': {'range': (1.2, 1.8), 'normal': 1.5, 'noise': 0.04},
            'P601': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P602': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'P603': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
        }

        # Column order must match original
        self.column_order = [
            'Timestamp',
            'FIT101', 'LIT101', 'MV101', 'P101', 'P102',
            'AIT201', 'AIT202', 'AIT203', 'FIT201', 'MV201', 'P201', 'P202', 'P203', 'P204', 'P205', 'P206',
            'DPIT301', 'FIT301', 'LIT301', 'MV301', 'MV302', 'MV303', 'MV304', 'P301', 'P302',
            'AIT401', 'AIT402', 'FIT401', 'LIT401', 'P401', 'P402', 'P403', 'P404', 'UV401',
            'AIT501', 'AIT502', 'AIT503', 'AIT504', 'FIT501', 'FIT502', 'FIT503', 'FIT504', 'P501', 'P502', 'PIT501', 'PIT502', 'PIT503',
            'FIT601', 'P601', 'P602', 'P603',
            'Normal/Attack'
        ]

        # Attack patterns with realistic implementations
        self.attack_types = [
            'sensor_spike', 'sensor_drop', 'sensor_flatline', 'sensor_oscillation',
            'pump_manipulation', 'valve_manipulation', 'multi_stage_attack', 'data_injection'
        ]

    def generate_normal_sample(self, timestamp):
        """Generate one normal sample"""
        sample = {'Timestamp': timestamp, 'Normal/Attack': 0}

        for sensor, spec in self.sensor_specs.items():
            if spec['noise'] == 0:
                sample[sensor] = spec['normal']
            else:
                sample[sensor] = np.clip(
                    np.random.normal(spec['normal'], spec['noise']),
                    spec['range'][0],
                    spec['range'][1]
                )

        return sample

    def inject_attack(self, sample, attack_type, severity_level):
        """Inject attack into sample based on type and severity"""
        attacked = sample.copy()
        attacked['Normal/Attack'] = 1

        # Select random sensors to attack
        all_sensors = list(self.sensor_specs.keys())

        if severity_level == 'critical':
            num_sensors = random.randint(8, 15)
            multiplier = random.uniform(3.0, 5.0)
        elif severity_level == 'high':
            num_sensors = random.randint(5, 10)
            multiplier = random.uniform(2.0, 3.0)
        elif severity_level == 'medium':
            num_sensors = random.randint(3, 6)
            multiplier = random.uniform(1.5, 2.0)
        else:  # low
            num_sensors = random.randint(1, 3)
            multiplier = random.uniform(1.2, 1.5)

        target_sensors = random.sample(all_sensors, min(num_sensors, len(all_sensors)))

        for sensor in target_sensors:
            spec = self.sensor_specs[sensor]

            if attack_type == 'sensor_spike':
                attacked[sensor] = min(spec['range'][1], sample[sensor] * multiplier)

            elif attack_type == 'sensor_drop':
                attacked[sensor] = max(spec['range'][0], sample[sensor] / multiplier)

            elif attack_type == 'sensor_flatline':
                # Stuck at abnormal value
                attacked[sensor] = spec['normal'] * (multiplier if multiplier < 2 else 0.5)

            elif attack_type == 'sensor_oscillation':
                # Rapid oscillation
                oscillation = np.sin(random.uniform(0, 2*np.pi)) * spec['normal'] * (multiplier - 1)
                attacked[sensor] = np.clip(
                    spec['normal'] + oscillation,
                    spec['range'][0],
                    spec['range'][1]
                )

            elif attack_type == 'pump_manipulation':
                if sensor.startswith('P'):
                    # Flip pump state or set to abnormal value
                    attacked[sensor] = random.choice([0, 2]) if sample[sensor] == 1 else 1

            elif attack_type == 'valve_manipulation':
                if sensor.startswith('MV'):
                    attacked[sensor] = np.clip(
                        sample[sensor] * multiplier,
                        spec['range'][0],
                        spec['range'][1]
                    )

            elif attack_type == 'multi_stage_attack':
                # Coordinated attack across stages
                if sensor.startswith(('FIT', 'LIT', 'PIT')):
                    attacked[sensor] = np.clip(
                        sample[sensor] * multiplier,
                        spec['range'][0],
                        spec['range'][1]
                    )

            elif attack_type == 'data_injection':
                # Subtle false data
                noise_factor = (multiplier - 1) * spec['normal']
                attacked[sensor] = np.clip(
                    spec['normal'] + random.uniform(-noise_factor, noise_factor),
                    spec['range'][0],
                    spec['range'][1]
                )

        return attacked

    def generate_dataset(self, num_samples=10000, attack_rate=0.40):
        """Generate complete dataset with attacks"""
        print(f"Generating {num_samples} samples with {attack_rate*100:.0f}% attack rate...")

        num_attacks = int(num_samples * attack_rate)
        num_normal = num_samples - num_attacks

        data = []
        start_time = datetime.now()

        # Severity distribution
        severities = ['low', 'medium', 'high', 'critical']
        severity_weights = [0.35, 0.35, 0.20, 0.10]

        # Generate normal samples
        for i in range(num_normal):
            timestamp = start_time + timedelta(seconds=i*3)
            sample = self.generate_normal_sample(timestamp)
            data.append(sample)

            if i % 1000 == 0:
                print(f"  Normal: {i}/{num_normal}")

        # Generate attack samples
        for i in range(num_attacks):
            timestamp = start_time + timedelta(seconds=(num_normal + i)*3)
            base_sample = self.generate_normal_sample(timestamp)

            attack_type = random.choice(self.attack_types)
            severity = random.choices(severities, weights=severity_weights)[0]

            attacked_sample = self.inject_attack(base_sample, attack_type, severity)
            data.append(attacked_sample)

            if i % 1000 == 0:
                print(f"  Attacks: {i}/{num_attacks}")

        # Convert to DataFrame with exact column order
        df = pd.DataFrame(data)
        df = df[self.column_order]

        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)

        print(f"\nGeneration complete!")
        print(f"  Total: {len(df)}")
        print(f"  Normal: {len(df[df['Normal/Attack']==0])}")
        print(f"  Attacks: {len(df[df['Normal/Attack']==1])}")
        print(f"  Attack rate: {(len(df[df['Normal/Attack']==1])/len(df))*100:.1f}%")

        return df


def main():
    """Generate realistic datasets"""
    generator = CompatibleSWaTGenerator(seed=42)

    os.makedirs('data', exist_ok=True)

    print("="*70)
    print("COMPATIBLE REALISTIC DATA GENERATOR")
    print("="*70)
    print()

    # Dataset 1: High attack rate for simulation
    print("Dataset 1: Real-time simulation (40% attacks)")
    print("-"*70)
    df1 = generator.generate_dataset(num_samples=15000, attack_rate=0.40)
    df1.to_csv('data/realtime_simulation_v2.csv', index=False)
    print(f"Saved: data/realtime_simulation_v2.csv\n")

    # Dataset 2: Test data
    print("Dataset 2: Test data (35% attacks)")
    print("-"*70)
    df2 = generator.generate_dataset(num_samples=5000, attack_rate=0.35)
    df2.to_csv('data/test_data_v2.csv', index=False)
    print(f"Saved: data/test_data_v2.csv\n")

    print("="*70)
    print("DATASETS READY!")
    print("="*70)


if __name__ == '__main__':
    main()
