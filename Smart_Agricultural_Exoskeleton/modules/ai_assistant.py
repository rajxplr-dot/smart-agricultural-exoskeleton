"""
MODULE 4: AI ASSISTANCE SYSTEM
Rule-based Contextual AI Reasoning Engine for Farm Worker Assistance.
Provides dynamic ergonomic recommendations and transparent causal explanations.
NOTE: Transparent Python-based deterministic heuristics. No external paid APIs or opaque black-box models.
"""

from typing import Dict, Any, List


def generate_ai_recommendation(
    sensor_reading: Dict[str, Any],
    posture_info: Dict[str, Any],
    fatigue_info: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generates structured, contextual AI recommendations and ergonomic action plans
    grounded in worker physiological state and posture.
    """
    fatigue_score = fatigue_info.get("fatigue_score", 0.0)
    risk_level = fatigue_info.get("risk_level", "Low")
    posture = sensor_reading.get("posture", "Standing")
    heart_rate = sensor_reading.get("heart_rate_bpm", 75)
    workload = sensor_reading.get("workload_percent", 50.0)
    hours = sensor_reading.get("working_hours", 2.0)
    primary_driver = fatigue_info.get("primary_driver", "Physical Workload")

    action_items: List[str] = []
    exoskeleton_advice: str = ""
    suggested_break_min: int = 0
    priority_level: str = "NORMAL"

    # Core logic based on risk tier
    if risk_level == "Low":
        priority_level = "LOW / ROUTINE"
        suggested_break_min = 0
        action_items = [
            "Maintain comfortable posture and fluid continuous pacing.",
            "Continue routine physiological telemetry monitoring.",
            "Maintain regular hydration intake (250 ml water every 45-60 min).",
            "Perform light shoulder and hamstring mobility stretches between task batches.",
        ]
        if posture == "Bending":
            exoskeleton_advice = "Back Support Mode can remain in Standby or Low-Assist (10-15 Nm) to prevent cumulative fatigue."
        elif posture == "Lifting":
            exoskeleton_advice = "Lifting Mode recommended on low torque boost for upcoming crate movements."
        else:
            exoskeleton_advice = "Exoskeleton can operate in Passive or Walking Assistance mode."

    elif risk_level == "Moderate":
        priority_level = "ELEVATED / CAUTION"
        suggested_break_min = 10
        action_items = [
            f"Fatigue accumulation detected (Risk Score: {fatigue_score}/100). Consider taking a short 10-minute rest under field shade.",
            f"Reduce repetitive manual cycle rate to alleviate {primary_driver}.",
            "Review spinal posture: avoid trunk flexion past 45° without lower limb support.",
            "Hydrate with electrolyte-infused water to counteract metabolic strain.",
        ]
        if posture == "Bending":
            exoskeleton_advice = "Engage BACK SUPPORT MODE at Medium Assistance (20-25 Nm) to offload lumbar erector spinae muscles."
        elif posture == "Lifting":
            exoskeleton_advice = "Engage LIFTING ASSISTANCE MODE at 70% torque assist; perform 2-person lifts for loads over 20 kg."
        elif posture == "Walking":
            exoskeleton_advice = "Engage WALKING ASSISTANCE MODE to match cadence and reduce metabolic expenditure."
        else:
            exoskeleton_advice = "Switch Exoskeleton to Rest / Standby Mode during seated breaks."

    else:  # High
        priority_level = "CRITICAL / IMMEDIATE ACTION"
        suggested_break_min = 25
        action_items = [
            f"CRITICAL: Immediate 20-25 minute rest pause required. Fatigue score reached {fatigue_score}/100.",
            f"Heart rate ({heart_rate} BPM) and workload ({workload}%) exceed safe continuous limits.",
            "Pause the current simulated work session and transition to a shaded seated posture.",
            "Worker should be monitored for signs of heat stress or acute musculoskeletal strain.",
            "Request assistance from field supervisor or co-workers before resuming heavy manual tasks.",
        ]
        exoskeleton_advice = (
            "LOCK OR DISENGAGE MOTORS: Switch Exoskeleton to REST MODE immediately. "
            "Do not rely on active robotic torque when worker cardiovascular limits are saturated."
        )

    # Explanation of contributing parameters
    factors_summary = (
        f"Recommendation formulated from combined inputs: Heart Rate ({heart_rate} BPM), "
        f"Workload Exertion ({workload}%), Shift Duration ({hours:.1f} hrs), and Posture [{posture}]. "
        f"The primary fatigue catalyst identified is '{primary_driver}'."
    )

    return {
        "priority_level": priority_level,
        "risk_level": risk_level,
        "fatigue_score": fatigue_score,
        "action_items": action_items,
        "suggested_break_minutes": suggested_break_min,
        "exoskeleton_directive": exoskeleton_advice,
        "factors_summary": factors_summary,
        "transparency_note": "Rule logic derived from agricultural ergonomic guidelines and biomechanical load limits.",
    }


def query_ai_knowledge_base(query: str, current_context: Dict[str, Any]) -> str:
    """
    Simulated Q&A expert reasoning assistant for viva and faculty demonstrations.
    Answers technical questions about exoskeleton mechanics, ergonomics, and AI heuristics.
    """
    q = query.lower()
    fatigue = current_context.get("fatigue_info", {})
    posture = current_context.get("posture_info", {})

    if "why" in q and ("risk" in q or "moderate" in q or "high" in q or "score" in q):
        return (
            f"Reasoning breakdown: The current fatigue risk score is {fatigue.get('fatigue_score', 'N/A')}/100 "
            f"({fatigue.get('risk_level', 'N/A')}). The algorithm evaluated: "
            f"1) Cardiovascular stress from heart rate ({fatigue.get('contributions', {}).get('Cardiovascular Stress (HR)', 'N/A')} pts), "
            f"2) Task workload percentage ({fatigue.get('contributions', {}).get('Physical Workload Rate', 'N/A')} pts), "
            f"3) Shift duration ({fatigue.get('contributions', {}).get('Continuous Duration Fatigue', 'N/A')} pts), and "
            f"4) Biomechanical posture penalty ({fatigue.get('contributions', {}).get('Biomechanical Postural Strain', 'N/A')} pts). "
            f"Primary contributing driver is '{fatigue.get('primary_driver', 'Workload')}'."
        )
    elif "torque" in q or "exoskeleton" in q or "motor" in q:
        return (
            "Exoskeleton Torque Protocol: The system utilizes simulated quasi-passive elastic bands combined with "
            "brushless DC actuators at the hip and lumbar joints. In Back Support Mode, torque is proportional to spine "
            "flexion angle (approx. 0.4 Nm per degree, capped at 30 Nm). In Lifting Mode, peak parallel torque of 25-35 Nm "
            "is delivered during knee extension to transfer loads safely to the ground."
        )
    elif "ergonomic" in q or "bending" in q or "reba" in q:
        return (
            f"Ergonomic Evaluation: The detected posture is '{posture.get('detected_posture', 'Bending')}' with an estimated "
            f"REBA index of {posture.get('reba_score', 'N/A')}/12. Continuous bending induces anterior shear forces on the "
            f"L4/L5 spinal vertebrae exceeding 2,500 N without assistive mechanisms. The exoskeleton counteracts this with "
            "elastic spinal counter-torque."
        )
    elif "formula" in q or "algorithm" in q or "calculate" in q:
        return (
            "Fatigue Algorithm Formulation: Risk Score = 0.30*(Normalized HR) + 0.30*(Workload %) + "
            "0.20*(Duration / 8 hrs * 100) + 0.20*(Posture Strain Weight) + Heat Modifier. "
            "Thresholds: 0-34 (Low), 35-64 (Moderate), 65-100 (High)."
        )
    else:
        return (
            f"AI AgriTech Advisory: Current worker is engaged in {current_context.get('sensor_reading', {}).get('activity', 'farm activity')}. "
            f"Fatigue level is {fatigue.get('risk_level', 'Normal')}. "
            "All telemetry parameters are within simulated observation thresholds."
        )
