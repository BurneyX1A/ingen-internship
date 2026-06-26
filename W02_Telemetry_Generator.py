"""
W02_Telemetry_Generator.py
Synthetic Aido Rover fleet telemetry generator.
This script creates a reproducible panel-style telemetry dataset:
    unit_id x timestamp
The dataset is designed to mimic robot fleet sensor data while keeping
a clear analogy to financial panel data such as stock_id x date.

Example:
    python W02_Telemetry_Generator.py \
        --units 40 \
        --days 3 \
        --freq 1min \
        --seed 42 \
        --output data/w02_telemetry_sample.parquet
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

def generate_telemetry(
    n_units: int = 40,
    n_days: int = 3,
    freq: str = "1min",
    seed: int = 42,
    start: str = "2026-06-15",

) -> pd.DataFrame:

    """
    Generate synthetic telemetry data for an Aido Rover fleet.
    Parameters
    ----------
    n_units : int
        Number of rover units.
    n_days : int
        Number of days to simulate.
    freq : str
        Pandas frequency string, such as "1min", "10s", or "1s".
    seed : int
        Random seed for reproducibility.
    start : str
        Start date of the simulated telemetry.
    Returns
    -------
    pd.DataFrame
        Multi-index DataFrame indexed by unit_id and timestamp.
    """
    
    rng = np.random.default_rng(seed)

    timestamps = pd.date_range(
        start=start,
        end=pd.Timestamp(start) + pd.Timedelta(days=n_days),
        freq=freq,
        inclusive="left",
    )
    
    records = []
    
    for unit_num in range(n_units):
        unit_id = f"AR_{unit_num:03d}"

        # Unit-level characteristics.
        # These make each rover slightly different, like firm-specific traits in equity data.
        efficiency = rng.normal(loc=1.0, scale=0.05)
        sensor_noise = rng.uniform(0.8, 1.2)
        battery_health = rng.normal(loc=1.0, scale=0.04)
        motor_resistance = rng.normal(loc=1.0, scale=0.06)

        # Some units are intentionally more failure-prone.
        failure_prone = rng.random() < 0.15
        
        initial_soc = rng.uniform(88, 100)
        soc = initial_soc
        
        for ts in timestamps:
            hour = ts.hour
            minute_of_day = ts.hour * 60 + ts.minute

            # Daily operating cycle.
            # Rovers are more active during daytime and less active at night.
            daytime_activity = 0.5 + 0.5 * np.sin(
                2 * np.pi * (minute_of_day - 360) / 1440
            )
            daytime_activity = np.clip(daytime_activity, 0.05, 1.0)

            # Speed in m/s.
            speed = (
                0.4
                + 1.8 * daytime_activity
                + rng.normal(0, 0.25 * sensor_noise)
            )
            speed = max(speed, 0)

            # CLI horizon: simplified command look-ahead / planning horizon.
            cli_horizon = (
                5
                + 8 * daytime_activity
                + rng.normal(0, 1.0)
            )
            cli_horizon = max(cli_horizon, 1)
            
            # Motor current for 4 drives.
            # Higher speed and higher resistance cause higher current.
            motor_base = 2.0 + 2.5 * speed * motor_resistance
            motor_currents = {
                f"motor_current_{i}": max(
                    0,
                    motor_base
                    + rng.normal(0, 0.35 * sensor_noise)
                    + rng.normal(0, 0.15)
                )
                for i in range(1, 5)
            }
            
            avg_motor_current = np.mean(list(motor_currents.values()))
            
            # Battery depletion depends on motor current, speed, and battery health.
            depletion = (
                0.0008 * avg_motor_current / battery_health
                + 0.0005 * speed
                + rng.normal(0, 0.00005)
            )
            depletion = max(depletion, 0)
            
            soc -= depletion
            
            # Simulate charging during low-activity night period.
            if hour in [1, 2, 3, 4] and rng.random() < 0.85:
                soc += rng.uniform(0.01, 0.04)
                
            soc = np.clip(soc, 0, 100)
            
            battery_voltage = 19.0 + 5.0 * (soc / 100) + rng.normal(0, 0.08)
            
            # GPS and RSSI.
            rssi = (
                -45
                - 15 * (1 - daytime_activity)
                + rng.normal(0, 4.0 * sensor_noise)
            )

            gps_fix_quality = 3
            if rssi < -65:
                gps_fix_quality = 2
            if rssi < -75:
                gps_fix_quality = 1
            if rssi < -85:
                gps_fix_quality = 0
                
            # IMU acceleration and gyroscope.
            imu_accel_x = speed * 0.15 + rng.normal(0, 0.08 * sensor_noise)
            imu_accel_y = rng.normal(0, 0.06 * sensor_noise)
            imu_accel_z = 9.81 + rng.normal(0, 0.05 * sensor_noise)
            imu_gyro_x = rng.normal(0, 0.02 * sensor_noise)
            imu_gyro_y = rng.normal(0, 0.02 * sensor_noise)
            imu_gyro_z = speed * 0.03 + rng.normal(0, 0.02 * sensor_noise)
            
            # Joint angles for 6-DOF arm.
            joint_angles = {}
            for j in range(1, 7):
                joint_angles[f"joint_angle_{j}"] = (
                    20 * np.sin(2 * np.pi * minute_of_day / 1440 + j)
                    + 5 * speed
                    + rng.normal(0, 2.0 * sensor_noise)
                )
            
            # Task success probability.
            # Low battery, weak RSSI, and failure-prone units reduce success.
            success_prob = 0.96
            success_prob -= 0.25 if soc < 20 else 0
            success_prob -= 0.15 if gps_fix_quality <= 1 else 0
            success_prob -= 0.10 if failure_prone else 0
            success_prob -= 0.03 * max(avg_motor_current - 7, 0)
            success_prob = np.clip(success_prob, 0.05, 0.99)
            
            task_success = int(rng.random() < success_prob)

            record = {
                "unit_id": unit_id,
                "timestamp": ts,
                "speed": speed,
                "cli_horizon": cli_horizon,
                "battery_voltage": battery_voltage,
                "battery_soc": soc,
                "gps_fix_quality": gps_fix_quality,
                "rssi": rssi,
                "task_success": task_success,
                "imu_accel_x": imu_accel_x,
                "imu_accel_y": imu_accel_y,
                "imu_accel_z": imu_accel_z,
                "imu_gyro_x": imu_gyro_x,
                "imu_gyro_y": imu_gyro_y,
                "imu_gyro_z": imu_gyro_z,
                **motor_currents,
                **joint_angles,
            }

            records.append(record)
        
    df = pd.DataFrame.from_records(records)
    
    # Add realistic missingness.
    # This is useful for the Week 2 missingness EDA requirement.
    df = add_missingness(df, rng)

    # Panel-style index: unit_id x timestamp.
    df = df.set_index(["unit_id", "timestamp"]).sort_index()
    return df

def add_missingness(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Add synthetic missingness patterns to telemetry data.
    Missingness is not purely random:
    - GPS-related missingness increases when RSSI is weak.
    - IMU channels have rare sensor dropouts.
    - Motor current channels have occasional missing readings.
    """

    df = df.copy()
    
    weak_signal = df["rssi"] < -72
    
    # GPS missingness under weak signal.
    gps_missing_mask = weak_signal & (rng.random(len(df)) < 0.20)
    df.loc[gps_missing_mask, "gps_fix_quality"] = np.nan

    # RSSI occasional dropout.
    rssi_missing_mask = rng.random(len(df)) < 0.01
    df.loc[rssi_missing_mask, "rssi"] = np.nan
    
    # IMU occasional missingness.
    imu_cols = [
        "imu_accel_x",
        "imu_accel_y",
        "imu_accel_z",
        "imu_gyro_x",
        "imu_gyro_y",
        "imu_gyro_z",
    ]
    imu_missing_mask = rng.random(len(df)) < 0.005
    df.loc[imu_missing_mask, imu_cols] = np.nan
    
    # Motor current sensor gaps.
    motor_cols = [f"motor_current_{i}" for i in range(1, 5)]
    motor_missing_mask = rng.random(len(df)) < 0.003
    df.loc[motor_missing_mask, motor_cols] = np.nan
    
    return df

def save_dataframe(df: pd.DataFrame, output_path: str) -> None:
    """
    Save DataFrame to parquet or csv based on file extension.
    """
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path)
    else:
        raise ValueError("Output file must end with .parquet or .csv")
    
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic Aido Rover fleet telemetry data."
    )

    parser.add_argument(
        "--units",
        type=int,
        default=40,
        help="Number of rover units to simulate.",
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=3,
        help="Number of days to simulate.",
    )

    parser.add_argument(
        "--freq",
        type=str,
        default="1min",
        help='Sampling frequency, such as "1min", "10s", or "1s".',
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/w02_telemetry_sample.parquet",
        help="Output path ending in .parquet or .csv.",
    )

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    
    df = generate_telemetry(
        n_units=args.units,
        n_days=args.days,
        freq=args.freq,
        seed=args.seed,
    )

    save_dataframe(df, args.output)

    print("Synthetic telemetry generation complete.")
    print(f"Output path: {args.output}")
    print(f"Shape: {df.shape}")
    print(f"Index names: {df.index.names}")
    print("\nPreview:")
    print(df.head())

if __name__ == "__main__":
    main()