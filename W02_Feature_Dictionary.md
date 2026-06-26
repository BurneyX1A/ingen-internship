# W02 Feature Dictionary: Synthetic Aido Rover Fleet Telemetry

This feature dictionary documents engineered telemetry features for the synthetic Aido Rover fleet dataset. The dataset is structured as a panel with `unit_id × timestamp`, similar to a financial panel with `stock_id × date`.

The goal of this feature dictionary is to connect robot telemetry signals with quantitative finance concepts. Each feature includes a formula, robot interpretation, quant-finance analogy, expected distribution, and possible failure mode.

## Feature Dictionary Columns

| Column | Description |
|---|---|
| Feature | Name of the engineered feature |
| Formula | How the feature is computed |
| Robot Interpretation | What the feature means for Aido Rover telemetry |
| Quant Finance Analogy | Similar concept in equity or factor data |
| Expected Distribution | Expected statistical behavior |
| Failure Mode | What abnormal values may indicate |

## Features

| # | Feature | Formula | Robot Interpretation | Quant Finance Analogy | Expected Distribution | Failure Mode |
|---|---|---|---|---|---|---|
| 1 | `battery_soc` | Raw battery state of charge | Current remaining battery percentage for each rover | Price level / balance-sheet level variable | Bounded between 0 and 100 | Very low values may indicate depletion risk or poor charging cycle |
| 2 | `battery_voltage` | Raw battery voltage | Electrical voltage level of the rover battery | Fundamental level variable | Approximately normal around operating voltage | Sudden drops may indicate battery instability or sensor error |
| 3 | `speed` | Raw rover speed | Rover movement speed at each timestamp | Trading activity / turnover proxy | Right-skewed, non-negative | Persistent zero speed during active hours may indicate inactivity or failure |
| 4 | `cli_horizon` | Raw command look-ahead horizon | Planning or command horizon used by the rover | Forecast horizon / model look-ahead window | Positive continuous variable | Very low horizon may indicate limited planning capability |
| 5 | `motor_current_1` | Raw current draw from drive 1 | Electrical load on motor drive 1 | Raw factor exposure / operating load | Positive and right-skewed | High values may indicate heavy load, terrain resistance, or motor stress |
| 6 | `motor_current_avg` | `(motor_current_1 + motor_current_2 + motor_current_3 + motor_current_4) / 4` | Average electrical load across the four drive motors | Composite factor score | Positive and right-skewed | Sustained high values may indicate heavy workload or mechanical inefficiency |
| 7 | `motor_current_roll_mean_7d` | `rolling_mean(motor_current_1, 7D)` | Smoothed recent motor load for each rover | Rolling factor mean | Smooth positive series | Rising trend may indicate increasing load or degradation |
| 8 | `motor_current_roll_std_7d` | `rolling_std(motor_current_1, 7D)` | Volatility of recent motor current | Rolling volatility | Positive, right-skewed | High values may indicate unstable operation or rough terrain |
| 9 | `motor_current_roll_z` | `(motor_current_1 - rolling_mean_7d) / rolling_std_7d` | Measures whether motor current is unusually high relative to recent history | Rolling z-score / standardized factor | Approximately centered around 0 | Large positive values may indicate abnormal motor stress |
| 10 | `battery_soc_roll_mean_7d` | `rolling_mean(battery_soc, 7D)` | Smoothed battery level over recent history | Moving average / smoothed level | Smooth bounded series | Persistent decline may indicate weak charging or heavy usage |
| 11 | `battery_soc_roll_std_7d` | `rolling_std(battery_soc, 7D)` | Variability of battery state of charge | Rolling volatility of a level variable | Positive, usually small | High values may indicate unstable charging or irregular usage |
| 12 | `battery_soc_drawdown` | `battery_soc / rolling_max(battery_soc, 7D) - 1` | Current battery decline from recent maximum charge | Maximum drawdown | Less than or equal to 0 | Large negative values may indicate severe battery depletion |
| 13 | `battery_soc_slope` | `rolling_linear_slope(battery_soc, 7D)` | Direction and speed of battery depletion or recovery | Trend slope / momentum | Centered near 0 with negative tails | Strong negative slope may indicate abnormal drain |
| 14 | `task_success_ema` | `EMA(task_success, span = 20)` | Smoothed recent task success rate | Momentum factor / exponentially weighted signal | Bounded between 0 and 1 | Falling values may indicate declining reliability |
| 15 | `task_success_rate_7d` | `rolling_mean(task_success, 7D)` | Rolling completion rate for rover tasks | Rolling hit rate / performance factor | Bounded between 0 and 1 | Low values may indicate operational failure or poor signal conditions |
| 16 | `battery_soc_cs_pct_rank` | `rank_pct(battery_soc within timestamp)` | Rover's battery percentile relative to the fleet at the same timestamp | Cross-sectional factor percentile / sector-relative rank | Uniform-like between 0 and 1 | Persistently low percentile may identify weak battery units |
| 17 | `motor_current_1_cs_pct_rank` | `rank_pct(motor_current_1 within timestamp)` | Rover's motor-load percentile relative to the fleet | Sector-relative PE/PB percentile ranking | Uniform-like between 0 and 1 | Persistently high percentile may indicate inefficient or stressed motors |
| 18 | `rssi_cs_pct_rank` | `rank_pct(rssi within timestamp)` | Relative wireless signal quality compared with other rovers | Relative liquidity / data-quality rank | Uniform-like between 0 and 1 | Low percentile may indicate weak signal or poor coverage |
| 19 | `task_success_cs_pct_rank` | `rank_pct(task_success within timestamp)` | Relative task success position within the fleet | Cross-sectional quality rank | Discrete, bounded between 0 and 1 | Low values may indicate reliability issues |
| 20 | `rssi` | Raw received signal strength indicator | Wireless signal strength for rover communication | Liquidity / data availability proxy | Usually negative, approximately normal with tails | Very low values may lead to communication dropout |
| 21 | `gps_fix_quality` | Discrete GPS quality score | Quality of rover GPS localization | Data quality flag / quote reliability flag | Discrete values, usually high | Low or missing values may indicate poor localization |
| 22 | `imu_accel_magnitude` | `sqrt(imu_accel_x^2 + imu_accel_y^2 + imu_accel_z^2)` | Total acceleration magnitude from IMU | Realized movement intensity | Centered near gravity with movement-driven variation | Spikes may indicate impact, rough terrain, or sensor noise |
| 23 | `imu_gyro_magnitude` | `sqrt(imu_gyro_x^2 + imu_gyro_y^2 + imu_gyro_z^2)` | Total angular movement from gyroscope | Realized volatility of orientation | Positive and right-skewed | High values may indicate unstable turning or vibration |
| 24 | `joint_angle_range` | `max(joint_angle_1 ... joint_angle_6) - min(joint_angle_1 ... joint_angle_6)` | Spread of 6-DOF joint positions | Cross-sectional dispersion / factor spread | Positive continuous variable | Very high spread may indicate extreme arm posture or calibration issue |
| 25 | `sensor_consistency_ratio` | `abs(delta imu_accel_magnitude) / (abs(delta speed) + epsilon)` | Checks whether IMU movement is consistent with speed changes | Signal validation ratio / factor consistency check | Right-skewed with occasional spikes | Extreme values may indicate sensor drift or inconsistent telemetry |

## Self-Check Notes

- The feature dictionary contains more than 20 engineered or raw telemetry features.
- Each feature includes a robot telemetry interpretation and a quantitative finance analogy.
- Rolling features use the same logic as rolling financial indicators such as moving averages, rolling volatility, z-scores, drawdown, and momentum.
- Cross-sectional percentile ranks are computed within each timestamp, not globally across the full panel.
- Several features explicitly connect telemetry failure modes to financial-data issues such as stale quotes, missing vendor fields, low liquidity, or unstable factor signals.