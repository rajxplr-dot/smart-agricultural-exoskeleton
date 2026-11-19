"""
MODULE 1: SENSOR SIMULATION
Simulates physiological and biomechanical sensor telemetry for farm workers.
NOTE: All readings are 100% software-simulated for academic demonstration.
"""

import datetime
import random
import numpy as np
from typing import Dict, Any, List

# Standard demonstration workers
DEMO_WORKERS = [
    {"id": "AGRI-WRK-101", "name": "Ramesh Kumar", "age": 38, "experience_yrs": 15},
    {"id": "AGRI-WRK-102", "name": "Sunita Devi", "age": 34, "experience_yrs": 11},
    {"id": "AGRI-WRK-103", "name": "Rajesh Patil", "age": 42, "experience_yrs": 18},
    {"id": "AGRI-WRK-104", "name": "Anil Verma", "age": 29, "experience_yrs": 7},
]

# Standard agricultural activities mapped to typical postures and biomechanics
AGRICULTURAL_ACTIVITIES = [
    {
        "activity": "Rice Transplanting / Weeding",
        "posture": "Bending",
        "hr_range": (90, 130),
        "workload_range": (60, 90),
        "flexion_range": (45.0, 85.0),
        "emg_range": (60.0, 92.0),
    },
    {
        "activity": "Lifting Heavy Produce Bags / Crates",
        "posture": "Lifting",
        "hr_range": (100, 145),
        "workload_range": (70, 95),
        "flexion_range": (35.0, 75.0),
        "emg_range": (70.0, 98.0),
    },
    {
        "activity": "Knapsack Chemical Spraying / Field Walk",
        "posture": "Walking",
        "hr_range": (85, 120),
        "workload_range": (45, 75),
        "flexion_range": (10.0, 30.0),
        "emg_range": (40.0, 70.0),
    },
    {
        "activity": "Vegetable Sorting & Packing",
        "posture": "Standing",
        "hr_range": (70, 95),
        "workload_range": (30, 55),
        "flexion_range": (5.0, 20.0),
        "emg_range": (25.0, 50.0),
    },
]


def generate_single_reading(
    worker_index: int = 0,
    activity_override: str = None,
    current_duration_hours: float = None,
    previous_reading: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Generates a single coherent simulated sensor reading for a farm worker.
    """
    worker = DEMO_WORKERS[worker_index % len(DEMO_WORKERS)]

    # Select activity profile
    if activity_override:
        matching = [a for a in AGRICULTURAL_ACTIVITIES if a["activity"] == activity_override]
        act_profile = matching[0] if matching else random.choice(AGRICULTURAL_ACTIVITIES)
    else:
        act_profile = random.choice(AGRICULTURAL_ACTIVITIES)

    # Calculate hours (smooth progression if previous exists)
    if current_duration_hours is not None:
        hours = round(current_duration_hours, 2)
    elif previous_reading is not None and "working_hours" in previous_reading:
        step = round(random.uniform(0.15, 0.40), 2)
        hours = round(min(8.5, previous_reading["working_hours"] + step), 2)
    else:
        hours = round(random.uniform(1.0, 6.5), 1)

    # Fatigue drift: as working hours increase, heart rate baseline rises slightly
    hour_drift = min(15, int(hours * 2.2))

    hr_min, hr_max = act_profile["hr_range"]
    heart_rate = int(random.randint(hr_min, hr_max) + hour_drift * 0.4)
    heart_rate = max(60, min(160, heart_rate))

    wl_min, wl_max = act_profile["workload_range"]
    workload = round(random.uniform(wl_min, wl_max) + (hour_drift * 0.3), 1)
    workload = max(20.0, min(100.0, workload))

    fl_min, fl_max = act_profile["flexion_range"]
    spine_flexion = round(random.uniform(fl_min, fl_max), 1)

    emg_min, emg_max = act_profile["emg_range"]
    muscle_effort = round(random.uniform(emg_min, emg_max), 1)

    ambient_temp = round(random.uniform(26.0, 37.0), 1)

    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": timestamp_str,
        "worker_id": worker["id"],
        "worker_name": worker["name"],
        "age": worker["age"],
        "experience_years": worker["experience_yrs"],
        "activity": act_profile["activity"],
        "posture": act_profile["posture"],
        "heart_rate_bpm": heart_rate,
        "workload_percent": workload,
        "working_hours": hours,
        "spine_flexion_deg": spine_flexion,
        "muscle_effort_percent": muscle_effort,
        "ambient_temp_c": ambient_temp,
        "monitoring_status": "ACTIVE (Simulated)",
        "is_simulated": True,
    }


def generate_initial_dataset(n_records: int = 25, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Generates a reproducible demonstration time-series dataset of at least 20 records.
    Uses fixed seed for academic consistency across initial demonstrations.
    """
    random.seed(seed)
    np.random.seed(seed)

    records = []
    base_time = datetime.datetime.now() - datetime.timedelta(hours=6.5)

    worker = DEMO_WORKERS[0]  # Primary demo worker: Ramesh Kumar
    accumulated_hours = 0.5

    for i in range(n_records):
        # Progress through a realistic agricultural shift
        if i < 7:
            act_profile = AGRICULTURAL_ACTIVITIES[0]  # Transplanting / Bending
        elif i < 13:
            act_profile = AGRICULTURAL_ACTIVITIES[1]  # Lifting Produce
        elif i < 19:
            act_profile = AGRICULTURAL_ACTIVITIES[2]  # Walking / Spraying
        else:
            act_profile = AGRICULTURAL_ACTIVITIES[3]  # Sorting / Standing

        accumulated_hours = round(0.5 + (i * 0.25), 2)
        time_stamp = base_time + datetime.timedelta(minutes=i * 15)

        hr_drift = min(18, int(accumulated_hours * 2.5))
        hr_min, hr_max = act_profile["hr_range"]
        heart_rate = int(random.randint(hr_min, hr_max) + hr_drift * 0.5)

        wl_min, wl_max = act_profile["workload_range"]
        workload = round(float(np.clip(random.uniform(wl_min, wl_max) + hr_drift * 0.3, 20.0, 98.0)), 1)

        fl_min, fl_max = act_profile["flexion_range"]
        flexion = round(random.uniform(fl_min, fl_max), 1)

        emg_min, emg_max = act_profile["emg_range"]
        emg = round(random.uniform(emg_min, emg_max), 1)

        temp = round(27.0 + (i * 0.35) + random.uniform(-0.8, 0.8), 1)

        record = {
            "timestamp": time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
            "worker_id": worker["id"],
            "worker_name": worker["name"],
            "age": worker["age"],
            "experience_years": worker["experience_yrs"],
            "activity": act_profile["activity"],
            "posture": act_profile["posture"],
            "heart_rate_bpm": heart_rate,
            "workload_percent": workload,
            "working_hours": accumulated_hours,
            "spine_flexion_deg": flexion,
            "muscle_effort_percent": emg,
            "ambient_temp_c": temp,
            "monitoring_status": "ACTIVE (Simulated)",
            "is_simulated": True,
        }
        records.append(record)

    return records
