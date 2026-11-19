"""
MODULE 7: DATA MANAGEMENT AND REPORTS
Handles persistence, CSV exports, session history, and statistical aggregations.
"""

import os
import io
import pandas as pd
from typing import List, Dict, Any, Optional

from modules.sensor_simulation import generate_initial_dataset
from modules.posture_analysis import analyze_posture
from modules.fatigue_analysis import calculate_fatigue_risk
from modules.ai_assistant import generate_ai_recommendation

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CSV_PATH = os.path.join(DATA_DIR, "sample_worker_data.csv")


def enrich_record(raw_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enriches a raw sensor telemetry record with posture analysis,
    fatigue-risk estimation, and AI recommendations.
    """
    rec = dict(raw_record)

    # Posture Analysis
    posture_res = analyze_posture(
        posture_name=rec.get("posture", "Standing"),
        flexion_angle_deg=rec.get("spine_flexion_deg", 0.0),
        workload_percent=rec.get("workload_percent", 50.0),
    )

    # Fatigue Risk
    fatigue_res = calculate_fatigue_risk(
        heart_rate_bpm=rec.get("heart_rate_bpm", 75),
        workload_percent=rec.get("workload_percent", 50.0),
        working_hours=rec.get("working_hours", 2.0),
        posture=rec.get("posture", "Standing"),
        ambient_temp_c=rec.get("ambient_temp_c", 28.0),
    )

    # AI Recommendation
    ai_res = generate_ai_recommendation(
        sensor_reading=rec,
        posture_info=posture_res,
        fatigue_info=fatigue_res,
    )

    # Merge fields
    rec["ergonomic_risk_level"] = posture_res["ergonomic_risk_level"]
    rec["reba_score"] = posture_res["reba_score"]
    rec["posture_guidance"] = posture_res["posture_guidance"]

    rec["fatigue_risk_score"] = fatigue_res["fatigue_score"]
    rec["fatigue_risk_level"] = fatigue_res["risk_level"]
    rec["primary_fatigue_driver"] = fatigue_res["primary_driver"]

    rec["ai_priority"] = ai_res["priority_level"]
    rec["ai_recommendation"] = "; ".join(ai_res["action_items"][:2])
    rec["exoskeleton_directive"] = ai_res["exoskeleton_directive"]

    return rec


def initialize_data_store() -> List[Dict[str, Any]]:
    """
    Loads records from sample_worker_data.csv if it exists,
    otherwise generates reproducible demo dataset (at least 20 records) and saves it.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            if not df.empty:
                return df.to_dict(orient="records")
        except Exception:
            pass

    # Generate initial reproducible dataset of 25 records
    raw_records = generate_initial_dataset(n_records=25, seed=42)
    enriched = [enrich_record(r) for r in raw_records]
    save_records_to_csv(enriched)
    return enriched


def save_records_to_csv(records: List[Dict[str, Any]], filepath: Optional[str] = None) -> bool:
    """
    Saves the list of records to local CSV file.
    """
    target = filepath or CSV_PATH
    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        df = pd.DataFrame(records)
        df.to_csv(target, index=False)
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


def get_records_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts record list into clean Pandas DataFrame for display and plotting.
    """
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def compute_summary_statistics(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates summary aggregations across current session records.
    """
    if not records:
        return {
            "total_records": 0,
            "avg_heart_rate": 0,
            "peak_heart_rate": 0,
            "avg_workload": 0,
            "max_hours": 0,
            "avg_fatigue_score": 0,
            "high_risk_count": 0,
            "moderate_risk_count": 0,
            "low_risk_count": 0,
            "dominant_posture": "N/A",
        }

    df = pd.DataFrame(records)
    total = len(df)
    avg_hr = round(float(df["heart_rate_bpm"].mean()), 1)
    peak_hr = int(df["heart_rate_bpm"].max())
    avg_wl = round(float(df["workload_percent"].mean()), 1)
    max_hrs = round(float(df["working_hours"].max()), 1)
    avg_fatigue = round(float(df["fatigue_risk_score"].mean()), 1)

    low_count = int((df["fatigue_risk_level"] == "Low").sum())
    mod_count = int((df["fatigue_risk_level"] == "Moderate").sum())
    high_count = int((df["fatigue_risk_level"] == "High").sum())

    dominant_posture = str(df["posture"].mode().iloc[0]) if not df["posture"].empty else "N/A"

    return {
        "total_records": total,
        "avg_heart_rate": avg_hr,
        "peak_heart_rate": peak_hr,
        "avg_workload": avg_wl,
        "max_hours": max_hrs,
        "avg_fatigue_score": avg_fatigue,
        "high_risk_count": high_count,
        "moderate_risk_count": mod_count,
        "low_risk_count": low_count,
        "dominant_posture": dominant_posture,
    }


def generate_csv_download_bytes(records: List[Dict[str, Any]]) -> bytes:
    """
    Generates UTF-8 encoded CSV bytes for Streamlit download button.
    """
    df = pd.DataFrame(records)
    return df.to_csv(index=False).encode("utf-8")


def reset_monitoring_data() -> List[Dict[str, Any]]:
    """
    Resets monitoring data back to the clean 25-record baseline dataset.
    """
    raw_records = generate_initial_dataset(n_records=25, seed=42)
    enriched = [enrich_record(r) for r in raw_records]
    save_records_to_csv(enriched)
    return enriched
