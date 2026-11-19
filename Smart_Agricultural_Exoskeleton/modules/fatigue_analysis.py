"""
MODULE 3: FATIGUE RISK ESTIMATION
Transparent mathematical algorithm for workload-related fatigue risk estimation.
Formula evaluates physiological, exertion, temporal, and ergonomic components.
NOTE: Illustrative demonstration thresholds; not clinically validated medical limits.
"""

from typing import Dict, Any


def calculate_fatigue_risk(
    heart_rate_bpm: float,
    workload_percent: float,
    working_hours: float,
    posture: str,
    ambient_temp_c: float = 28.0,
) -> Dict[str, Any]:
    """
    Calculates a transparent mathematical fatigue-risk score (0 to 100).
    Formula components:
      1. Cardiovascular Exertion (30%): Heart rate relative to resting baseline (60-140 BPM).
      2. Workload Intensity (30%): Worker reported exertion percentage.
      3. Cumulative Duration (20%): Exposure time across a standard 8-hour farm shift.
      4. Biomechanical Posture Strain (20%): Ergonomic strain factor based on posture.
      5. Heat Factor Modifier: +2 to +5 points if ambient temperature exceeds 32°C.
    """
    # 1. Heart Rate Sub-score (normalized between 60 BPM and 140 BPM)
    hr_clamped = max(60.0, min(150.0, float(heart_rate_bpm)))
    hr_score = ((hr_clamped - 60.0) / (140.0 - 60.0)) * 100.0
    hr_score = max(0.0, min(100.0, hr_score))

    # 2. Workload Sub-score
    wl_score = max(0.0, min(100.0, float(workload_percent)))

    # 3. Duration Fatigue Accumulation (scaled against 8-hour threshold)
    duration_clamped = max(0.0, min(10.0, float(working_hours)))
    duration_score = (duration_clamped / 8.0) * 100.0
    duration_score = max(0.0, min(100.0, duration_score))

    # 4. Posture Ergonomic Multiplier
    posture_weights = {
        "standing": 30.0,
        "walking": 50.0,
        "bending": 85.0,
        "lifting": 95.0,
    }
    clean_posture = "standing"
    for p_key in posture_weights:
        if p_key in posture.lower():
            clean_posture = p_key
            break
    posture_score = posture_weights[clean_posture]

    # Weighted Sum Formula
    w_hr = 0.30
    w_wl = 0.30
    w_dur = 0.20
    w_post = 0.20

    raw_score = (
        (w_hr * hr_score)
        + (w_wl * wl_score)
        + (w_dur * duration_score)
        + (w_post * posture_score)
    )

    # Environmental Heat Stress Modifier
    heat_mod = 0.0
    if ambient_temp_c > 35.0:
        heat_mod = 4.0
    elif ambient_temp_c > 32.0:
        heat_mod = 2.0

    final_score = round(min(100.0, max(0.0, raw_score + heat_mod)), 1)

    # Demonstration Classification Thresholds:
    # 0 - 34: Low
    # 35 - 64: Moderate
    # 65 - 100: High
    if final_score <= 34.0:
        risk_level = "Low"
        badge_color = "#16A34A"  # Green
        status_label = "Optimal / Safe Operating Envelope"
        risk_icon = "🟢"
    elif final_score <= 64.0:
        risk_level = "Moderate"
        badge_color = "#F59E0B"  # Amber
        status_label = "Elevated Fatigue Risk / Caution Advised"
        risk_icon = "🟡"
    else:
        risk_level = "High"
        badge_color = "#DC2626"  # Red
        status_label = "Critical Fatigue Risk / Immediate Rest Advised"
        risk_icon = "🔴"

    # Identify primary contributing driver
    contributions = {
        "Cardiovascular Stress (HR)": round(w_hr * hr_score, 1),
        "Physical Workload Rate": round(w_wl * wl_score, 1),
        "Continuous Duration Fatigue": round(w_dur * duration_score, 1),
        "Biomechanical Postural Strain": round(w_post * posture_score, 1),
    }
    primary_driver = max(contributions, key=contributions.get)

    # Explanation construction
    explanation = (
        f"Total fatigue risk calculated at {final_score}/100 ({risk_level}). "
        f"The primary strain factor is {primary_driver} ({contributions[primary_driver]} pts). "
        f"Heart rate: {int(heart_rate_bpm)} BPM ({contributions['Cardiovascular Stress (HR)']} pts), "
        f"Workload: {workload_percent:.1f}% ({contributions['Physical Workload Rate']} pts), "
        f"Continuous Shift: {working_hours:.1f} hrs ({contributions['Continuous Duration Fatigue']} pts), "
        f"Posture [{posture.title()}]: ({contributions['Biomechanical Postural Strain']} pts)."
    )
    if heat_mod > 0:
        explanation += f" Elevated field temperature ({ambient_temp_c}°C) added +{heat_mod} thermal stress pts."

    return {
        "fatigue_score": final_score,
        "risk_level": risk_level,
        "badge_color": badge_color,
        "status_label": status_label,
        "risk_icon": risk_icon,
        "progress_ratio": final_score / 100.0,
        "contributions": contributions,
        "subscores": {
            "heart_rate_subscore": round(hr_score, 1),
            "workload_subscore": round(wl_score, 1),
            "duration_subscore": round(duration_score, 1),
            "posture_subscore": round(posture_score, 1),
        },
        "primary_driver": primary_driver,
        "explanation": explanation,
        "disclaimer": "Illustrative demonstration model for academic presentation. Not clinically validated.",
    }
