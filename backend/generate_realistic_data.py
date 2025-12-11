"""
Advanced Realistic Data Generator for SWaT System
Generates highly realistic sensor data with diverse attack scenarios at varying severity levels
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class AdvancedSWaTGenerator:
    """Generate ultra-realistic SWaT sensor data with sophisticated attack patterns"""

    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)

        # 51 sensors across 6 stages with realistic operating ranges
        self.sensor_specs = {
            # Stage 1 - Raw Water Supply (8 sensors)
            'FIT-101': {'range': (1.8, 2.2), 'normal': 2.0, 'noise': 0.05},
            'LIT-101': {'range': (800, 1000), 'normal': 900, 'noise': 15},
            'P-101': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'P-102': {'range': (0, 1), 'normal': 0, 'noise': 0},
            'MV-101': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'AIT-101': {'range': (200, 400), 'normal': 300, 'noise': 10},
            'AIT-102': {'range': (150, 350), 'normal': 250, 'noise': 8},
            'DPIT-101': {'range': (0, 5), 'normal': 2.5, 'noise': 0.2},

            # Stage 2 - Chemical Dosing (9 sensors)
            'FIT-201': {'range': (1.0, 1.4), 'normal': 1.2, 'noise': 0.03},
            'AIT-201': {'range': (200, 400), 'normal': 300, 'noise': 12},
            'AIT-202': {'range': (180, 380), 'normal': 280, 'noise': 10},
            'AIT-203': {'range': (150, 300), 'normal': 225, 'noise': 8},
            'P-201': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'P-202': {'range': (0, 1), 'normal': 0, 'noise': 0},
            'P-203': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'P-204': {'range': (0, 1), 'normal': 0, 'noise': 0},
            'MV-201': {'range': (0, 2), 'normal': 1, 'noise': 0.1},

            # Stage 3 - Ultrafiltration (10 sensors)
            'FIT-301': {'range': (2.2, 2.8), 'normal': 2.5, 'noise': 0.06},
            'LIT-301': {'range': (600, 900), 'normal': 750, 'noise': 20},
            'DPIT-301': {'range': (3, 8), 'normal': 5.5, 'noise': 0.3},
            'P-301': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'P-302': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'MV-301': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'MV-302': {'range': (0, 2), 'normal': 1, 'noise': 0.1},
            'AIT-301': {'range': (100, 250), 'normal': 175, 'noise': 7},
            'AIT-302': {'range': (120, 280), 'normal': 200, 'noise': 9},
            'AIT-303': {'range': (90, 220), 'normal': 155, 'noise': 6},

            # Stage 4 - UV Dechlorination (8 sensors)
            'FIT-401': {'range': (1.8, 2.4), 'normal': 2.1, 'noise': 0.05},
            'LIT-401': {'range': (400, 700), 'normal': 550, 'noise': 18},
            'AIT-401': {'range': (30, 90), 'normal': 60, 'noise': 4},
            'AIT-402': {'range': (25, 85), 'normal': 55, 'noise': 3.5},
            'P-401': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'P-402': {'range': (0, 1), 'normal': 0, 'noise': 0},
            'P-403': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'UV-401': {'range': (0, 100), 'normal': 85, 'noise': 5},

            # Stage 5 - Reverse Osmosis (8 sensors)
            'FIT-501': {'range': (1.5, 2.0), 'normal': 1.75, 'noise': 0.04},
            'FIT-502': {'range': (0.8, 1.3), 'normal': 1.05, 'noise': 0.03},
            'FIT-503': {'range': (0.6, 1.1), 'normal': 0.85, 'noise': 0.02},
            'PIT-501': {'range': (20, 40), 'normal': 30, 'noise': 1.5},
            'PIT-502': {'range': (15, 35), 'normal': 25, 'noise': 1.2},
            'P-501': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'P-502': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'AIT-501': {'range': (50, 150), 'normal': 100, 'noise': 6},

            # Stage 6 - Backwash (8 sensors)
            'FIT-601': {'range': (1.2, 1.8), 'normal': 1.5, 'noise': 0.04},
            'LIT-601': {'range': (300, 600), 'normal': 450, 'noise': 15},
            'P-601': {'range': (0, 1), 'normal': 0, 'noise': 0},
            'P-602': {'range': (0, 1), 'normal': 0, 'noise': 0},
            'P-603': {'range': (0, 1), 'normal': 1, 'noise': 0},
            'DPIT-601': {'range': (1, 6), 'normal': 3.5, 'noise': 0.25},
            'AIT-601': {'range': (80, 180), 'normal': 130, 'noise': 7},
            'AIT-602': {'range': (70, 170), 'normal': 120, 'noise': 6.5},
        }

        # Attack pattern definitions with severity levels
        self.attack_patterns = {
            'sensor_spike': {
                'description': 'Sudden spike in sensor readings',
                'severity_multipliers': {'low': 1.3, 'medium': 1.8, 'high': 2.5, 'critical': 4.0}
            },
            'sensor_drop': {
                'description': 'Sudden drop in sensor readings',
                'severity_multipliers': {'low': 0.7, 'medium': 0.5, 'high': 0.3, 'critical': 0.1}
            },
            'sensor_flatline': {
                'description': 'Sensor reading stuck at constant value',
                'severity_multipliers': {'low': 0.95, 'medium': 0.90, 'high': 0.85, 'critical': 0.80}
            },
            'sensor_oscillation': {
                'description': 'Rapid oscillation in sensor readings',
                'severity_multipliers': {'low': 0.15, 'medium': 0.30, 'high': 0.50, 'critical': 0.80}
            },
            'pump_manipulation': {
                'description': 'Unauthorized pump state changes',
                'severity_multipliers': {'low': None, 'medium': None, 'high': None, 'critical': None}
            },
            'valve_manipulation': {
                'description': 'Unauthorized valve position changes',
                'severity_multipliers': {'low': 0.3, 'medium': 0.5, 'high': 0.8, 'critical': 1.2}
            },
            'multi_stage_cascade': {
                'description': 'Coordinated attack across multiple stages',
                'severity_multipliers': {'low': 1.2, 'medium': 1.5, 'high': 2.0, 'critical': 3.0}
            },
            'data_injection': {
                'description': 'False data injection attack',
                'severity_multipliers': {'low': 1.1, 'medium': 1.4, 'high': 1.9, 'critical': 2.8}
            }
        }

    def generate_normal_sample(self):
        """Generate a single normal (non-attack) data sample"""
        sample = {}
        for sensor, spec in self.sensor_specs.items():
            if spec['noise'] == 0:  # Binary sensors (pumps, valves)
                sample[sensor] = spec['normal']
            else:
                # Add realistic gaussian noise
                sample[sensor] = np.clip(
                    np.random.normal(spec['normal'], spec['noise']),
                    spec['range'][0],
                    spec['range'][1]
                )
        sample['Normal/Attack'] = 0
        sample['Attack_Type'] = 'Normal'
        sample['Attack_Severity'] = 'None'
        sample['Affected_Stage'] = 0
        return sample

    def inject_attack(self, sample, attack_type, severity, target_sensors):
        """Inject a specific attack pattern into a sample"""
        attacked_sample = sample.copy()
        multiplier = self.attack_patterns[attack_type]['severity_multipliers'][severity]

        if attack_type == 'sensor_spike':
            for sensor in target_sensors:
                spec = self.sensor_specs[sensor]
                attacked_sample[sensor] = min(
                    spec['range'][1],
                    sample[sensor] * multiplier
                )

        elif attack_type == 'sensor_drop':
            for sensor in target_sensors:
                spec = self.sensor_specs[sensor]
                attacked_sample[sensor] = max(
                    spec['range'][0],
                    sample[sensor] * multiplier
                )

        elif attack_type == 'sensor_flatline':
            for sensor in target_sensors:
                spec = self.sensor_specs[sensor]
                # Flatline at abnormal value
                attacked_sample[sensor] = spec['normal'] * multiplier

        elif attack_type == 'sensor_oscillation':
            for sensor in target_sensors:
                spec = self.sensor_specs[sensor]
                oscillation = np.sin(np.random.uniform(0, 2*np.pi)) * spec['normal'] * multiplier
                attacked_sample[sensor] = np.clip(
                    spec['normal'] + oscillation,
                    spec['range'][0],
                    spec['range'][1]
                )

        elif attack_type == 'pump_manipulation':
            for sensor in target_sensors:
                if 'P-' in sensor:
                    # Flip pump state
                    attacked_sample[sensor] = 1 - sample[sensor]

        elif attack_type == 'valve_manipulation':
            for sensor in target_sensors:
                if 'MV-' in sensor:
                    spec = self.sensor_specs[sensor]
                    attacked_sample[sensor] = np.clip(
                        sample[sensor] * multiplier,
                        spec['range'][0],
                        spec['range'][1]
                    )

        elif attack_type == 'multi_stage_cascade':
            # Affect multiple sensors across different stages
            for sensor in target_sensors:
                spec = self.sensor_specs[sensor]
                if 'FIT-' in sensor or 'LIT-' in sensor:
                    attacked_sample[sensor] = np.clip(
                        sample[sensor] * multiplier,
                        spec['range'][0],
                        spec['range'][1]
                    )

        elif attack_type == 'data_injection':
            for sensor in target_sensors:
                spec = self.sensor_specs[sensor]
                # Inject subtly wrong data
                attacked_sample[sensor] = np.clip(
                    spec['normal'] + np.random.uniform(-1, 1) * spec['normal'] * (multiplier - 1),
                    spec['range'][0],
                    spec['range'][1]
                )

        attacked_sample['Normal/Attack'] = 1
        attacked_sample['Attack_Type'] = attack_type
        attacked_sample['Attack_Severity'] = severity

        return attacked_sample

    def get_stage_sensors(self, stage):
        """Get all sensors for a specific stage"""
        stage_map = {
            1: ['FIT-101', 'LIT-101', 'P-101', 'P-102', 'MV-101', 'AIT-101', 'AIT-102', 'DPIT-101'],
            2: ['FIT-201', 'AIT-201', 'AIT-202', 'AIT-203', 'P-201', 'P-202', 'P-203', 'P-204', 'MV-201'],
            3: ['FIT-301', 'LIT-301', 'DPIT-301', 'P-301', 'P-302', 'MV-301', 'MV-302', 'AIT-301', 'AIT-302', 'AIT-303'],
            4: ['FIT-401', 'LIT-401', 'AIT-401', 'AIT-402', 'P-401', 'P-402', 'P-403', 'UV-401'],
            5: ['FIT-501', 'FIT-502', 'FIT-503', 'PIT-501', 'PIT-502', 'P-501', 'P-502', 'AIT-501'],
            6: ['FIT-601', 'LIT-601', 'P-601', 'P-602', 'P-603', 'DPIT-601', 'AIT-601', 'AIT-602']
        }
        return stage_map.get(stage, [])

    def generate_dataset(self, total_samples=10000, attack_percentage=0.35):
        """
        Generate a realistic dataset with diverse attack scenarios

        Args:
            total_samples: Total number of samples to generate
            attack_percentage: Percentage of samples that should be attacks (0.0 to 1.0)
        """
        data = []
        num_attacks = int(total_samples * attack_percentage)
        num_normal = total_samples - num_attacks

        print(f"Generating {total_samples} samples ({num_normal} normal, {num_attacks} attacks)...")

        # Severity distribution (more low/medium, fewer critical)
        severity_dist = {
            'low': 0.35,
            'medium': 0.35,
            'high': 0.20,
            'critical': 0.10
        }

        # Attack type distribution
        attack_types = list(self.attack_patterns.keys())
        attack_weights = [15, 15, 10, 10, 12, 12, 8, 18]  # Weighted distribution

        # Generate normal samples
        for i in range(num_normal):
            data.append(self.generate_normal_sample())
            if i % 1000 == 0:
                print(f"  Normal samples: {i}/{num_normal}")

        # Generate attack samples with varying severity
        for i in range(num_attacks):
            # Select attack type
            attack_type = random.choices(attack_types, weights=attack_weights)[0]

            # Select severity
            severity = random.choices(
                list(severity_dist.keys()),
                weights=list(severity_dist.values())
            )[0]

            # Select target stage and sensors
            target_stage = random.randint(1, 6)
            stage_sensors = self.get_stage_sensors(target_stage)

            # For critical attacks, affect more sensors
            if severity == 'critical':
                num_sensors = random.randint(3, min(6, len(stage_sensors)))
            elif severity == 'high':
                num_sensors = random.randint(2, min(4, len(stage_sensors)))
            elif severity == 'medium':
                num_sensors = random.randint(1, min(3, len(stage_sensors)))
            else:  # low
                num_sensors = random.randint(1, 2)

            target_sensors = random.sample(stage_sensors, num_sensors)

            # Generate base sample and inject attack
            base_sample = self.generate_normal_sample()
            attacked_sample = self.inject_attack(base_sample, attack_type, severity, target_sensors)
            attacked_sample['Affected_Stage'] = target_stage
            attacked_sample['Num_Affected_Sensors'] = num_sensors

            data.append(attacked_sample)

            if i % 1000 == 0:
                print(f"  Attack samples: {i}/{num_attacks}")

        # Convert to DataFrame and shuffle
        df = pd.DataFrame(data)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)

        # Add timestamp
        start_time = datetime.now()
        df['Timestamp'] = [start_time + timedelta(seconds=i*3) for i in range(len(df))]

        print(f"\nDataset generation complete!")
        print(f"  Total samples: {len(df)}")
        print(f"  Normal samples: {len(df[df['Normal/Attack']==0])}")
        print(f"  Attack samples: {len(df[df['Normal/Attack']==1])}")
        print(f"\nAttack severity distribution:")
        for sev in ['low', 'medium', 'high', 'critical']:
            count = len(df[df['Attack_Severity']==sev])
            pct = (count / len(df)) * 100
            print(f"  {sev.capitalize()}: {count} ({pct:.1f}%)")
        print(f"\nAttack type distribution:")
        for at in attack_types:
            count = len(df[df['Attack_Type']==at])
            pct = (count / len(df)) * 100 if len(df) > 0 else 0
            print(f"  {at}: {count} ({pct:.1f}%)")

        return df


def main():
    """Generate multiple realistic datasets"""
    generator = AdvancedSWaTGenerator(seed=42)

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    print("="*60)
    print("ADVANCED REALISTIC SWAT DATA GENERATOR")
    print("="*60)
    print()

    # Dataset 1: High attack rate for real-time simulation
    print("Dataset 1: Real-time simulation data (high attack rate)")
    print("-"*60)
    df1 = generator.generate_dataset(total_samples=15000, attack_percentage=0.40)
    df1.to_csv('data/realtime_simulation.csv', index=False)
    print(f"Saved to: data/realtime_simulation.csv")
    print()

    # Dataset 2: Balanced dataset for testing
    print("\nDataset 2: Test data (balanced)")
    print("-"*60)
    df2 = generator.generate_dataset(total_samples=5000, attack_percentage=0.35)
    df2.to_csv('data/test_data.csv', index=False)
    print(f"Saved to: data/test_data.csv")
    print()

    # Dataset 3: Critical scenarios dataset
    print("\nDataset 3: Critical scenarios (very high severity)")
    print("-"*60)
    # Generate with higher critical attack percentage
    generator_critical = AdvancedSWaTGenerator(seed=123)
    df3 = generator_critical.generate_dataset(total_samples=3000, attack_percentage=0.50)
    df3.to_csv('data/critical_scenarios.csv', index=False)
    print(f"Saved to: data/critical_scenarios.csv")
    print()

    print("="*60)
    print("ALL DATASETS GENERATED SUCCESSFULLY!")
    print("="*60)


if __name__ == '__main__':
    main()
