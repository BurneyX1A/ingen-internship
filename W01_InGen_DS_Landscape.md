# W01 InGen DS Landscape

## 1. Objective

This document translates InGen Dynamics' Physical AI product landscape into a data science and quantitative finance framework. The goal is not to describe each robot only as a product, but to treat each platform as a data-generating system: what signals it produces, what KPIs those signals support, what time-series structure the data has, and which quantitative finance analogy best captures the mechanism.

The week-one bridge is built around five InGen platforms: **Aido Rover**, **Fari**, **Senpai**, **Sentinel Prime AI**, and **Origami AI / PIC 2.0**. Aido Rover is used as the primary data context because it produces the clearest high-frequency physical sensor stream: mobile autonomy, outdoor inspection, perception, safety, fleet telemetry, and incident events. Origami / PIC 2.0 is used as the orientation layer because the InGen materials position it as the common physical-intelligence architecture across multiple robot platforms.

The core analytical question is:

> How can data structures from Physical AI — sensors, robot state, uncertainty, safety gates, calibration, and fleet coordination — be mapped into familiar data science and quantitative finance concepts such as high-frequency market data, factor models, risk limits, anomaly detection, and portfolio monitoring?

---

## 2. Product Landscape

| Platform | Product Role | Primary Data Context | Best Quant / DS Analogy |
|---|---|---|---|
| **Aido Rover** | Autonomous outdoor inspection and security robot | High-frequency multimodal robot telemetry, perception, navigation, inspection, security events, battery and fleet state | High-frequency equity / futures time series with event-driven risk monitoring |
| **Fari** | Eldercare and healthcare AI companion robot | Passive health monitoring, resident interaction, fall/medication/mood events, caregiver workflows, EHR-linked records | Healthcare credit-risk / survival model with alternative behavioral data |
| **Senpai** | AI educational companion robot | Student engagement, adaptive learning progress, SEND adaptation, classroom interaction, teacher/parent dashboards | Multi-factor learning outcome model similar to factor investing |
| **Sentinel Prime AI** | Enterprise physical security intelligence platform | Video, identity, behavioral threat, weapon, vehicle, environmental, alert and incident escalation data | Fraud detection / market surveillance / real-time anomaly detection |
| **Origami AI / PIC 2.0** | Physical Intelligence Core and shared platform layer | Cross-robot data lake, sensor calibration, uncertainty, policy learning, task planning, safety, fleet orchestration | Quant research platform + risk engine + portfolio construction architecture |

---

## 3. Platform Data Analyst Profiles

### 3.1 Aido Rover

**Product role.**  
Aido Rover is an autonomous outdoor inspection and security robot for environments such as critical infrastructure, solar farms, airports, ports, campuses, agriculture, oil and gas, and government or military sites. The InGen documents describe it as an outdoor autonomous patrol and inspection robot with a 14-sensor suite, multi-terrain mobility, SLAM navigation, detection AI, inspection intelligence, fleet dashboarding, API events, and SEOM safety controls.

**Implied sensor streams and data volume.**  
Aido Rover is the richest week-one data source because it produces continuous mobile autonomy data. Its implied sensor streams include RGB / video frames, LiDAR or depth returns, thermal imagery, GPS / GNSS, IMU, wheel odometry, battery telemetry, motor current, obstacle and terrain measurements, environmental readings, camera detections, patrol-route state, docking / charging state, and fleet coordination events. These streams are high-volume and high-frequency: perception and navigation are naturally frame-level or sub-second data; safety and localization loops must update in near real time; incident and inspection events are lower-frequency but high-value labels.

The data should be modeled as a **multivariate streaming time series** with several layers:

1. **Raw sensor layer:** camera, LiDAR/depth, thermal, IMU, GPS, motor and battery streams.
2. **State-estimation layer:** pose, velocity, route progress, obstacle state, localization confidence.
3. **Detection layer:** person, vehicle, perimeter, infrastructure, environmental and inspection events.
4. **Decision layer:** patrol mode, route choice, stop/go command, dock/charge command, escalation level.
5. **Fleet layer:** robot availability, mission assignment, charger usage, maintenance flags.

**Primary KPI categories.**

| KPI Category | Example KPIs |
|---|---|
| Navigation performance | localization accuracy, route completion, patrol coverage, obstacle avoidance, GPS-denied recovery |
| Detection performance | precision, recall, false alert rate, detection latency, incident confirmation rate |
| Inspection value | infrastructure defect detection, thermal anomaly detection, vegetation / obstacle detection, evidence quality |
| Safety | SEOM block rate, near-miss count, emergency stop count, human proximity violations |
| Fleet operations | uptime, battery cycle health, docking success, mission utilization, mean time between failures |
| Commercial ROI | guard-hour substitution, avoided inspection cost, reduced downtime, insurance or compliance value |

**Quant finance analogy.**  
Aido Rover is most similar to **high-frequency equity or futures time-series data**. The analogy is not simply that both involve time series. The deeper structure is that both are noisy, high-frequency, multivariate streams generated by dynamic systems where decisions must be made before uncertainty is fully resolved.

In high-frequency trading, the analyst receives price ticks, order-book updates, volume, spread, volatility, and execution events. The goal is to infer the latent market state and act under uncertainty. Aido Rover receives sensor frames, LiDAR returns, GPS/IMU state, obstacle detections, battery state, and route events. The robot must infer the latent physical state and act safely. Both systems require state estimation, anomaly filtering, latency-aware decision rules, and risk controls.

**Mechanistic reason the analogy holds.**  
The analogy holds because Aido Rover data and high-frequency market data share four structural properties:

1. **Noise:** LiDAR vegetation scatter, thermal drift, GPS multipath, and camera occlusion resemble bid-ask bounce, quote noise, stale prices, and liquidity shocks.
2. **Latency:** both require decisions under strict timing limits; stale information can be harmful.
3. **Hidden state:** the true terrain, threat, obstruction, or asset condition is not directly observed, just as true market supply/demand is latent behind observed quotes.
4. **Risk gating:** SEOM / STUM safety checks function like pre-trade risk limits, volatility filters, and kill switches.

---

### 3.2 Fari

**Product role.**  
Fari is an eldercare and healthcare AI companion robot intended for care homes, assisted living, memory care, hospitals, and home care. The InGen materials describe Fari as a tabletop companion robot with resident-facing interaction, caregiver dashboards, family apps, EHR integration, continuous health monitoring, fall prevention, medication management, emotional companionship, and high SEOM ethical weighting.

**Implied sensor streams and data volume.**  
Fari produces a mixed stream of passive monitoring data and interaction data. Likely inputs include voice commands, conversation transcripts, resident display interactions, caregiver notes, medication reminders, fall events, movement / presence signals, mood or affect estimates, sleep and daily routine indicators, and EHR-linked structured fields. Compared with Aido Rover, Fari is less about outdoor high-frequency mobility and more about **longitudinal human-state monitoring**.

Data frequency varies by stream: passive presence and activity can be near-continuous; medication and fall alerts are event-driven; mood and social engagement metrics are daily or session-level; EHR fields are lower-frequency but clinically important. The key data object is not a single robot state; it is a **resident risk trajectory** over days, weeks, and months.

**Primary KPI categories.**

| KPI Category | Example KPIs |
|---|---|
| Health and safety | fall detection rate, medication adherence, incident response time, missed alert rate |
| Resident wellbeing | engagement frequency, mood stability, loneliness proxy, daily routine consistency |
| Clinical workflow | caregiver time saved, dashboard review efficiency, EHR documentation completeness |
| Family reassurance | family app usage, video call frequency, message response rate, consented update views |
| Ethical and privacy safety | consent compliance, SEOM violations, sensitive-data access control |
| Reliability | uptime, sensor availability, alert delivery success, device response latency |

**Quant finance analogy.**  
Fari is most similar to **credit-risk, insurance-risk, or survival-analysis modeling enriched by alternative data**. In credit risk, the analyst does not only look at a current balance; they look at a borrower trajectory: payment history, utilization, delinquency signals, macro context, and behavioral data. Fari similarly does not only classify one event; it observes a resident’s longitudinal condition and tries to detect deterioration, safety risk, or need for intervention before a severe incident occurs.

**Mechanistic reason the analogy holds.**  
The analogy holds because Fari and credit / survival models both convert sparse, noisy, and human-centered observations into a forward-looking risk estimate. A missed medication, reduced activity, abnormal sleep pattern, or low engagement can function like a widening credit spread or rising default probability: it is not the adverse event itself, but a leading indicator of possible future harm. The data analyst’s role is to distinguish random variation from persistent deterioration while respecting privacy, consent, and severe false-negative costs.

---

### 3.3 Senpai

**Product role.**  
Senpai is an AI educational companion robot for K-12, SEND, higher education, government training, and professional learning contexts. The InGen documents describe it as an adaptive, personalized learning platform with robot display states, teacher dashboard, student dashboard, parent app, adaptive curriculum, interactive projector, social-emotional learning module, and six SEND adaptation modes.

**Implied sensor streams and data volume.**  
Senpai generates educational interaction and learning-process data. Its streams likely include lesson events, quiz responses, engagement detections, gaze or attention proxies, speech/pronunciation data, curriculum progression, SEND adaptation mode, teacher interventions, parent app feedback, session duration, task completion, error patterns, and emotional or social learning indicators. The data is a combination of high-frequency classroom interaction signals and lower-frequency learning outcomes.

The important data structure is a **student-by-time-by-feature panel dataset**. Each student has repeated observations across lessons. Each lesson has content difficulty, modality, engagement, correctness, time-to-answer, hint usage, and adaptation strategy. This panel structure naturally supports factor-style modeling.

**Primary KPI categories.**

| KPI Category | Example KPIs |
|---|---|
| Learning outcomes | completion rate, mastery gain, pre/post improvement, retention, time-to-mastery |
| Engagement | attention score, session duration, voluntary interaction, dropout / disengagement rate |
| Adaptivity | curriculum match accuracy, hint effectiveness, content difficulty calibration |
| SEND support | adaptation usage, accessibility success, reduced teacher intervention load |
| Teacher workflow | dashboard actionability, lesson planning time saved, class-level progress visibility |
| Safety and ethics | child data privacy, SEOM content flags, age-appropriate response rate |

**Quant finance analogy.**  
Senpai is most similar to a **multi-factor model**. In the Fama-French logic, returns are not explained by one variable; they are decomposed into systematic factors such as market exposure, size, and value. Senpai’s learning outcomes are similarly not explained by one variable. They are produced by multiple observable and latent factors: baseline skill, content difficulty, engagement, attention, SEND adaptation mode, teacher involvement, session frequency, and social-emotional state.

**Mechanistic reason the analogy holds.**  
The analogy holds because both systems seek to explain an outcome as the weighted result of multiple persistent factors. A stock’s return may be decomposed into market, size, value, profitability, or investment exposure. A student’s learning progress may be decomposed into prior mastery, engagement, modality fit, difficulty level, assistive adaptation, and feedback quality. The analyst’s job is to estimate which factors are predictive, which are confounded, and which can be changed by intervention.

---

### 3.4 Sentinel Prime AI

**Product role.**  
Sentinel Prime AI is an enterprise physical security intelligence platform for corporate campuses, critical infrastructure, airports, hospitals, data centers, government, retail, and logistics. The InGen materials describe multiple hardware form factors, 27 AI detection functions, 14 sensors, a 5-model detection ensemble, STUM uncertainty gating, SEOM rules, operations dashboards, mobile supervisor apps, and integration with enterprise security systems.

**Implied sensor streams and data volume.**  
Sentinel generates video, acoustic, identity, environmental, access, and incident data. The core stream is likely continuous video and perception output, enriched by detections such as person, identity, gait, behavior, weapon, physical threat, vehicle, environmental hazard, smoke, fire, door/vibration, and abnormal motion. It also generates incident escalation events, supervisor acknowledgments, evidence objects, response actions, device health metrics, and integration events to systems such as VMS, access control, SIEM, SOC, or alerting tools.

Sentinel’s data is high-volume because video and detection streams are continuous. However, the business value is concentrated in **rare events**: true threats, safety hazards, access violations, weapons, fights, abandoned objects, and environmental incidents.

**Primary KPI categories.**

| KPI Category | Example KPIs |
|---|---|
| Detection quality | precision, recall, false alert rate, false negative rate, STUM calibration, detection latency |
| Incident response | time-to-alert, time-to-acknowledge, escalation accuracy, evidence completeness |
| Security operations | guard workload reduction, alert triage efficiency, incident closure time |
| Compliance and audit | tamper-evident evidence, access logs, retention compliance, audit completeness |
| System reliability | uptime, edge inference latency, camera/sensor health, network failover |
| Safety and ethics | SEOM blocked actions, privacy violations prevented, human review rate |

**Quant finance analogy.**  
Sentinel is most similar to **fraud detection, anti-money-laundering surveillance, and market abuse monitoring**. Most observations are normal. The analyst is searching for rare but costly anomalies in a high-volume event stream. The model must minimize false alerts because alert fatigue destroys operator trust, but it also must avoid missing severe events.

**Mechanistic reason the analogy holds.**  
The analogy holds because Sentinel and financial surveillance share the same class-imbalance and escalation structure. In fraud monitoring, a transaction stream is filtered through anomaly scores, rules, confidence thresholds, and human review. In Sentinel, perception events are filtered through detection confidence, STUM uncertainty, SEOM rules, and escalation ladders. In both systems, the model is not the final decision-maker; it is a triage engine that converts noisy data into prioritized human action.

---

### 3.5 Origami AI / PIC 2.0

**Product role.**  
Origami AI is the shared platform layer behind the InGen product family. The documents describe PIC 2.0 as a Physical Intelligence Core built from six foundation models and a broader edge-cloud architecture. The platform includes GRPO policy learning, STUM uncertainty modeling, SEOM safety, AMDC calibration, HTD-IRL task planning, CRL-MRS fleet AI, an Origami dashboard, cloud microservices, a data lake, developer tools, and vertical software bundles.

**Implied sensor streams and data volume.**  
Origami is not a single robot stream. It is the platform that standardizes streams across products. Its implied data layers include raw robot sensor data, validated telemetry, curated gold-layer data, event logs, calibration data, model outputs, policy artifacts, safety audit logs, fleet metrics, and user-facing dashboard data. The InGen materials describe a data lake structure and edge-cloud split, which means Origami should be treated as the analytical backbone for all downstream robot products.

**Primary KPI categories.**

| KPI Category | Example KPIs |
|---|---|
| Inference performance | edge latency, model throughput, cloud fallback rate, OTA update success |
| Model quality | policy reward, calibration error, uncertainty coverage, task success |
| Safety | SEOM audit pass rate, unsafe action blocks, safety-chain latency |
| Data platform health | ingestion success, data validation rate, schema consistency, gold-layer completeness |
| Fleet intelligence | multi-robot coordination efficiency, charger utilization, mission assignment quality |
| Developer ecosystem | API usage, SDK adoption, integration success, no-code AI/Robot Maker activity |

**Quant finance analogy.**  
Origami / PIC 2.0 is most similar to a **quant research platform combined with a portfolio risk engine**. A quant platform ingests raw data, cleans and validates it, estimates factors, runs models, generates signals, applies risk constraints, executes trades, and logs audit records. Origami ingests sensor data, calibrates it, estimates uncertainty, plans tasks, selects actions, applies safety constraints, actuates robots, and records audit events.

**Mechanistic reason the analogy holds.**  
The analogy holds because both systems are layered decision architectures. The value does not come from one isolated model; it comes from the pipeline. In quant finance, a profitable signal is useless if the data is stale, the risk model is wrong, the execution engine is slow, or compliance blocks the trade. In Physical AI, a navigation policy is unsafe if sensors are miscalibrated, uncertainty is high, task planning is wrong, or SEOM blocks the action. Origami’s six-model architecture maps naturally onto the quant stack: data cleaning, uncertainty modeling, signal generation, portfolio construction, risk control, and execution.

---

## 4. Quant-to-Physical-AI Bridge Table

| Physical AI Concept | Quant Finance / DS Analog | Mechanistic Reason |
|---|---|---|
| **Aido Rover raw sensor stream** | High-frequency equity / futures tick data | Both are high-frequency, noisy, multivariate streams. The system must infer latent state and act before full information is available. |
| **Robot localization and state estimation** | Latent state estimation in market microstructure | True physical position / terrain state is partially observed, like true supply-demand pressure behind observed prices and order-book updates. |
| **STUM uncertainty score** | Volatility estimate / confidence interval / model risk score | Both quantify when the model should trust its own output less. High uncertainty reduces action size or triggers human review. |
| **SEOM safety gate** | Risk limits, compliance constraints, VaR / kill switch | Both are hard constraints that can override an otherwise profitable or efficient action when risk exceeds policy limits. |
| **AMDC sensor calibration** | Data cleaning, price adjustment, corporate-action adjustment | Raw observations are not analysis-ready. Drift, multipath, occlusion, stale data, and sensor bias must be corrected before modeling. |
| **GRPO policy learning** | Alpha model / execution policy optimization | Both learn an action policy from historical reward, but the policy must be constrained by risk, uncertainty, and real-world frictions. |
| **HTD-IRL task planning** | Hierarchical portfolio construction | High-level objectives are decomposed into executable sub-tasks, just as portfolio objectives are decomposed into asset weights, constraints, and trades. |
| **CRL-MRS fleet coordination** | Portfolio allocation and multi-asset risk management | A fleet of robots resembles a portfolio of assets: resources must be allocated across units while balancing utilization, battery health, mission risk, and coverage. |
| **Predictive maintenance / robot health** | Credit default prediction / survival analysis | Component degradation is a time-to-event risk problem. Leading indicators raise the probability of future failure before the event occurs. |
| **Sentinel incident detection** | Fraud detection / AML / market surveillance | Most events are normal; the system must identify rare, costly anomalies while controlling false positives and alert fatigue. |
| **Fari resident health trajectory** | Credit-risk migration / insurance risk scoring | Resident state changes gradually. Small behavioral and health signals can indicate rising probability of future adverse events. |
| **Senpai adaptive learning factors** | Multi-factor return model | Learning outcomes are driven by multiple factors, not one variable. Progress is decomposed into engagement, baseline ability, content fit, support mode, and feedback quality. |
| **Origami data lake** | Quant data lake / research database | Both store raw, validated, and curated data for model training, backtesting, monitoring, and auditability. |
| **Dashboard KPIs** | Portfolio risk and performance dashboard | Both compress complex system state into actionable metrics for operators who need fast triage and trend awareness. |

### Three additional Burney-identified mechanistic mappings

1. **STUM uncertainty gate → volatility regime filter.**  
   In a trading system, a volatility filter reduces or blocks exposure when the market enters an unstable regime. In PIC 2.0, STUM reduces trust in perception or action when sensor confidence is low or temporal evidence is stale. The structural mechanism is the same: uncertainty is not merely reported; it changes the action policy.

2. **SEOM ethical safety → pre-trade risk and compliance controls.**  
   A trading system can produce a strong alpha signal, but compliance and risk systems can still block execution. A robot policy can produce a high-reward action, but SEOM can block it if it violates safety, privacy, ethical, or human-proximity constraints. The structural mechanism is override authority: risk control sits outside the optimizing model.

3. **CRL-MRS fleet coordination → portfolio rebalancing under constraints.**  
   Multi-robot operations require allocating tasks, chargers, patrol zones, and maintenance windows across a fleet. Portfolio management similarly allocates capital, risk budget, and liquidity across assets. The structural mechanism is constrained optimization across multiple units whose individual performance affects system-level performance.

---

## 5. Strongest Quant Analogy

The strongest quant analogy I found is:

> **Aido Rover's high-frequency physical sensor stream resembles high-frequency equity or futures market data.**

This analogy is strongest because it is mechanical rather than cosmetic. Aido Rover and a high-frequency trading system both operate in a dynamic environment where raw observations are noisy, incomplete, and time-sensitive. A trading system sees bids, asks, trades, order-book imbalance, volume, and volatility. Aido Rover sees camera frames, LiDAR/depth readings, thermal signals, GPS/IMU estimates, battery telemetry, obstacle detections, and route events. Neither system directly observes the true state. Each must infer it.

The decision problem is also structurally similar. A trading model must decide whether to trade, wait, reduce size, or cancel based on uncertain market conditions. Aido Rover must decide whether to move, stop, re-route, inspect, escalate, dock, or request human review based on uncertain physical conditions. In both cases, the cost of acting on bad data can be high. Bad market data can cause bad execution; bad robot perception can cause unsafe movement, missed detection, or failed inspection.

The deepest connection is the combination of **signal, uncertainty, and risk gating**. In quant finance, a signal is not enough: it must pass liquidity, volatility, exposure, compliance, and execution checks. In Aido Rover, a learned action is not enough: it must pass calibration, uncertainty, task-planning, and SEOM safety checks. That makes Aido Rover an excellent Physical AI case for translating quantitative time-series thinking into robotics data science.

---

## 6. References and Source Notes

### InGen / Origami source materials used

- `Aido_Rover_Product_Functionality_Plan.html`
- `Aido_Rover_Engineering_Handbook.html`
- `Aido_Rover_Detailed_Functionality.docx`
- `Fari_Product_Functionality_Plan.html`
- `fari_engineering_handbook.html`
- `Fari_Detailed_Functionality.docx`
- `Senpai_Product_Functionality_Plan (1).html`
- `Senpai_Engineering_Handbook.html`
- `Senpai_Detailed_Functionality.docx`
- `Sentinel_Prime_AI_Product_Functionality_Plan.html`
- `sentinel_prime_ai_engineering_handbook.html`
- `Sentinel_Prime_AI_Detailed_Functionality.docx`
- `Origami_AI_Platform_Product_Functionality_Plan.html`
- `origami_ai_platform_engineering_handbook.html`
- `Origami_AI_Platform_Detailed_Functionality.docx`
- `Origami_AI_1Platform_Paper.html`

### External methodology references

- International Federation of Robotics, **World Robotics 2025 — Service Robots**, public materials and abstract.
- Eugene F. Fama and Kenneth R. French, **“Common Risk Factors in the Returns on Stocks and Bonds,”** *Journal of Financial Economics*, 1993.
- Jiachen Li, Shihao Li, Jian Chu, Wei Li, Dongmei Chen, **“Fleet-Level Battery-Health-Aware Scheduling for Autonomous Mobile Robots,”** arXiv, 2026.
- OpenBot-Fleet / robot fleet learning literature as supporting context for fleet-level robotics data systems.
- Predictive maintenance and health-monitoring literature for mobile robots and long-duration physical systems.

---

## 7. Self-Check

- Each quant analogy explains a **structural mechanism**, not just a surface resemblance.
- Each platform is described as a **data-generating system** with sensor streams, KPI categories, and an analytical analog.
- Aido Rover is explicitly mapped to **high-frequency equity / futures time series**.
- The bridge table includes more than three additional mechanistic mappings beyond the base product descriptions.
- The environment verification notebook separately confirms Python 3.11 and the required Python toolchain.
