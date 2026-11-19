"""
MODULE 2: POSTURE DETECTION AND ANALYSIS
Rule-based ergonomic posture classification and biomechanical assessment.
NOTE: Operates on simulated sensor and activity inputs. Not camera/vision-based.
"""

from typing import Dict, Any, List


# Ergonomic standards mapping based on illustrative biomechanical guidelines
POSTURE_DATABASE = {
    "Standing": {
        "category": "Static Upright Neutral",
        "base_risk": "Low",
        "risk_weight": 0.20,
        "reba_range": (1, 3),
        "spinal_strain_desc": "Minimal lumbar disc pressure; low muscular torque on thoracic spine.",
        "guidance": "Maintain balanced weight distribution across both feet. Use anti-fatigue matting if standing continuously on hard surfaces.",
        "risk_badge_color": "#16A34A",
    },
    "Walking": {
        "category": "Dynamic Locomotive",
        "base_risk": "Low to Moderate",
        "risk_weight": 0.35,
        "reba_range": (3, 5),
        "spinal_strain_desc": "Dynamic cyclic loading; elevated metabolic expenditure when carrying knapsack or tools.",
        "guidance": "Maintain a natural upright cadence. When traversing uneven furrows, keep knees slightly flexed to absorb ground impact.",
        "risk_badge_color": "#0284C7",
    },
    "Bending": {
        "category": "Sustained Lumbar Flexion",
        "base_risk": "High",
        "risk_weight": 0.85,
        "reba_range": (8, 10),
        "spinal_strain_desc": "Severe anterior shear on L4-L5 lumbar vertebrae; erector spinae muscles operate under continuous isometric strain.",
        "guidance": "WARNING: Prolonged trunk flexion detected! Perform spinal extension pauses every 15 minutes. Consider knee-supported squatting or engage Exoskeleton Back Support.",
        "risk_badge_color": "#DC2626",
    },
    "Lifting": {
        "category": "Dynamic Heavy Load Manual Handling",
        "base_risk": "Critical",
        "risk_weight": 0.95,
        "reba_range": (9, 12),
        "spinal_strain_desc": "High compressive torque exceeding 3,000 N on lower vertebral discs during load acceleration phase.",
        "guidance": "CRITICAL: Lift with quadriceps and glutes by bending knees, NOT the lumbar spine. Keep load close to center of mass. Avoid sudden spinal twisting.",
        "risk_badge_color": "#B91C1C",
    },
}


def analyze_posture(
    posture_name: str,
    flexion_angle_deg: float = 0.0,
    workload_percent: float = 50.0,
) -> Dict[str, Any]:
    """
    Performs comprehensive rule-based ergonomic and biomechanical analysis
    for the detected posture.
    """
    # Normalize posture name
    clean_posture = "Standing"
    for key in POSTURE_DATABASE:
        if key.lower() in posture_name.lower():
            clean_posture = key
            break

    profile = POSTURE_DATABASE[clean_posture]

    # Calculate dynamic ergonomic adjustments based on spine angle and workload
    risk_level = profile["base_risk"]
    if clean_posture == "Bending":
        if flexion_angle_deg > 65.0 or workload_percent > 75.0:
            risk_level = "Critical"
        else:
            risk_level = "High"
    elif clean_posture == "Walking":
        if workload_percent > 70.0:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
    elif clean_posture == "Standing":
        if workload_percent > 65.0:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

    # Illustrative REBA/RULA score calculation (scale 1 to 12)
    min_r, max_r = profile["reba_range"]
    reba_score = round(min_r + (flexion_angle_deg / 90.0) * (max_r - min_r) * 0.7 + (workload_percent / 100.0) * 1.5, 1)
    reba_score = min(12.0, max(1.0, reba_score))

    # Action urgency based on REBA score
    if reba_score >= 9.0:
        action_urgency = "Immediate Ergonomic Intervention Required"
    elif reba_score >= 7.0:
        action_urgency = "Corrective Action Necessary Soon"
    elif reba_score >= 4.0:
        action_urgency = "Further Ergonomic Monitoring Advised"
    else:
        action_urgency = "Acceptable Posture; Maintain Safe Ergonomics"

    return {
        "detected_posture": clean_posture,
        "posture_category": profile["category"],
        "ergonomic_risk_level": risk_level,
        "risk_weight": profile["risk_weight"],
        "reba_score": reba_score,
        "action_urgency": action_urgency,
        "spinal_strain_description": profile["spinal_strain_desc"],
        "posture_guidance": profile["guidance"],
        "risk_badge_color": profile["risk_badge_color"],
        "spine_flexion_angle": flexion_angle_deg,
    }


def compute_posture_distribution(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes statistical distribution and counts of postures across a dataset.
    """
    counts = {"Standing": 0, "Bending": 0, "Lifting": 0, "Walking": 0}
    for rec in records:
        post = rec.get("posture", "Standing")
        matched = False
        for k in counts:
            if k.lower() in post.lower():
                counts[k] += 1
                matched = True
                break
        if not matched:
            counts["Standing"] += 1

    total = sum(counts.values()) or 1
    percentages = {k: round((v / total) * 100, 1) for k, v in counts.items()}

    return {
        "counts": counts,
        "percentages": percentages,
        "total_records": total,
    }
