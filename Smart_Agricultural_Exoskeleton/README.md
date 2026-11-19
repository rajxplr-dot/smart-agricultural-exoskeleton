# Smart Agricultural Exoskeleton for Farm Workers with AI Assistance

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, software-based agricultural worker assistance simulation and biomechatronic decision-support platform designed for academic demonstration and engineering project viva presentations.

---

## 1. Project Introduction

Agricultural workers worldwide perform physically grueling manual labor, including:
- **Continuous bending** during rice transplanting, seedling planting, and ground-level harvesting.
- **Heavy lifting** of crop sacks, fertilizer bags, and produce crates.
- **Extended walking** across uneven field furrows carrying heavy knapsack chemical sprayers.
- **Prolonged work hours** under direct sun and heat.

These repetitive activities cause severe occupational health hazards, leading to acute fatigue and chronic **Work-Related Musculoskeletal Disorders (WMSDs)**, particularly lumbar spine (L4/L5 disc) damage.

The **Smart Agricultural Exoskeleton for Farm Workers with AI Assistance** demonstrates the control software, sensor fusion heuristics, fatigue-risk estimation, and biomechatronic assistance logic governing an intelligent wearable agricultural exoskeleton—**100% simulated in software** without requiring physical motors or hardware sensors.

---

## 2. Problem Statement & Objectives

### Problem
Physical agricultural labor involves high biomechanical strain. While industrial manufacturing uses advanced robotic exoskeletons, farm workers lack accessible assistive technology. Developing physical hardware requires substantial capital, high-torque planetary actuators, and safety clearances. However, the core engineering foundation lies in the **software intelligence** that detects posture, estimates fatigue, and commands assistive torque.

### Objectives
1. **Simulate Multi-parameter Physiological Telemetry:** Generate realistic synthetic farm worker telemetry (Heart Rate, Workload %, Spine Flexion Angle, Muscle Effort, Duration).
2. **Rule-Based Posture & Ergonomic Analysis:** Detect postures (Standing, Bending, Lifting, Walking) and compute illustrative REBA (Rapid Entire Body Assessment) ergonomic risk scores.
3. **Transparent Fatigue-Risk Scoring Algorithm:** Calculate a normalized 0–100 fatigue risk score based on cardiovascular exertion, task workload, duration, and posture.
4. **Contextual AI Assistance:** Provide transparent, priority-graded ergonomic advisories and work-rest schedules without paid external APIs.
5. **Conceptual 4-Mode Exoskeleton Simulation:** Model assistive joint torque offloading across Back Support, Lifting Assistance, Walking Assistance, and Rest modes.
6. **Data Management & Reporting:** Save and export full telemetry logs to CSV and provide an interactive analytics dashboard.

---

## 3. Technology Stack

- **Programming Language:** Python 3.10+
- **Web Application & UI:** Streamlit (with customized AgriTech CSS styling)
- **Data Processing & Storage:** Pandas, NumPy, CSV
- **Interactive Visualizations:** Plotly (Express & Graph Objects)
- **Machine Learning / Analytics:** Scikit-learn (summary heuristics)
- **Platform Compatibility:** Windows, macOS, Linux (Zero paid APIs, zero external databases, 100% local execution)

---

## 4. Project Architecture & Directory Structure

```
Smart_Agricultural_Exoskeleton/
│
├── app.py                      # Main Streamlit web application & multi-page router
│
├── modules/
│   ├── __init__.py             # Python package indicator
│   ├── sensor_simulation.py    # Generates synthetic physiological & biomechanical data
│   ├── posture_analysis.py     # Rule-based ergonomic classification & REBA indices
│   ├── fatigue_analysis.py     # Mathematical fatigue-risk scoring algorithm
│   ├── ai_assistant.py         # Contextual heuristic AI recommendations & Viva Q&A
│   ├── exoskeleton_simulation.py# 4-mode biomechatronic torque assistance model
│   └── data_manager.py         # CSV persistence, summaries, and report downloads
│
├── data/
│   └── sample_worker_data.csv  # Local reproducible demonstration dataset (>= 20 records)
│
├── assets/
│   └── logo.png                # High-resolution AgriTech project branding logo
│
├── requirements.txt            # Python dependencies
├── README.md                   # Setup, execution, and architecture guide
└── PROJECT_DOCUMENTATION.md    # In-depth academic project engineering report
```

---

## 5. Main Functional Modules

| Module | Name | Primary Function |
|---|---|---|
| **Module 1** | Worker Monitoring | Simulates worker HR, workload %, shift duration, spine angle, muscle effort, and ambient temp. |
| **Module 2** | Posture Detection | Classifies posture (Standing, Bending, Lifting, Walking), estimates spinal shear, and assigns REBA score. |
| **Module 3** | Fatigue Risk Estimation | Multi-parameter weighted algorithm calculating an explainable risk score (0–100) with low/moderate/high tiers. |
| **Module 4** | AI Assistance System | Contextual heuristic advisor delivering prioritized rest plans, hydration alerts, and viva Q&A responses. |
| **Module 5** | Exoskeleton Simulation | Biomechatronic mode controller (Back Support, Lifting, Walking, Rest) computing active torque and muscle relief %. |
| **Module 6** | Analytics Dashboard | Interactive Plotly graphs: HR progression, fatigue trends, posture distribution, and workload correlation. |
| **Module 7** | Data Management & Reports | Exports CSV telemetry reports, allows record filtering, and provides data reset functionality. |

---

## 6. Installation & Execution Guide

### Step 1: Open VS Code or Terminal
Open a command prompt or PowerShell window on your Windows laptop.

### Step 2: Navigate to the Project Directory
```powershell
cd C:\Users\rajni\.gemini\antigravity\scratch\Smart_Agricultural_Exoskeleton
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```powershell
streamlit run app.py
```
*(Alternatively: `python -m streamlit run app.py`)*

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 7. How to Demonstrate During College Project Viva

1. **Start at Overview (Page 1):** Point out the real-time KPI metrics (Heart Rate, Workload, Posture, Fatigue Score, Exoskeleton Mode). Highlight the professional AgriTech design and explain that all telemetry is software-simulated for safety and demonstration reliability.
2. **Click "Generate New Sensor Readings":** Show the viva examiner how clicking the button instantly advances the worker's shift, updates heart rate and flexion angle, and triggers new AI recommendations.
3. **Show Posture Analysis (Page 3):** Explain the difference in lumbar disc pressure between Standing and Bending. Use the interactive Posture Scenario Simulator to demonstrate the REBA risk index.
4. **Explain Fatigue Scoring Formula (Page 4):** Walk through the mathematical formula:
   $$\text{Fatigue Score} = 0.30(S_{HR}) + 0.30(S_{WL}) + 0.20(S_{DUR}) + 0.20(S_{POST}) + \Delta_{Heat}$$
   Show the pie chart breaking down parameter contributions.
5. **Demonstrate AI Viva Q&A (Page 4):** Select a preset question (e.g., *"Why is the worker flagged with Moderate risk?"*) and click **Run AI Query Inference** to showcase the explainable AI reasoning.
6. **Switch Exoskeleton Modes (Page 5):** Demonstrate the 4 modes:
   - **Back Support Mode:** Active for bending (24.5 Nm torque, 38% lumbar relief).
   - **Lifting Assistance Mode:** High torque bursts (30.0 Nm torque, 44% relief).
   - **Walking Assistance Mode:** Gait cadence synchronization (14.0 Nm).
   - **Rest Mode:** Clutch disengaged (0 Nm, passive standby).
7. **Show Analytics & Export CSV (Pages 6 & 7):** Demonstrate the Plotly time-series charts and download a CSV report with one click.

---

## 8. Limitations & Future Scope

### Limitations
- **Software Simulation:** Relies on simulated sensor telemetry rather than physical wearable biosensors.
- **Rule-Based Posture Inference:** Operates on simulated kinematic parameters; does not process camera video feeds.
- **Illustrative Thresholds:** Ergonomic and fatigue scoring thresholds are academic demonstration models, not clinically certified medical diagnostic tools.

### Future Scope
- **Physical Exoskeleton Hardware:** Integration of lightweight carbon-fiber/aluminum frames with high-torque brushless DC motors.
- **Real Wearable Sensor Integration:** Interfacing physical heart rate monitors (PPG) and surface electromyography (sEMG) bands via BLE/WiFi.
- **Computer Vision Posture Tracking:** Deploying MediaPipe or OpenPose with a smartphone camera for real-time field posture estimation.
- **Edge AI & IoT Deployment:** Running micro-ML inference models on ESP32 or Raspberry Pi for real-time off-grid telemetry streaming.

---

## 9. Academic Disclaimer

This project is developed for educational and academic demonstration purposes as part of an undergraduate engineering curriculum. The ergonomic metrics, fatigue scores, and exoskeleton telemetry are illustrative demonstration simulations and should not be used as clinical occupational safety certifications.
