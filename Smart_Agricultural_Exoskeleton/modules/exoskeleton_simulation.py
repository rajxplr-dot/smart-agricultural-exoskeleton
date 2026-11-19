"""
MODULE 5: EXOSKELETON ASSISTANCE SIMULATION
Simulates the conceptual biomechatronic operation of a Smart Agricultural Exoskeleton.
NOTE: Conceptual software simulation only. Does not control physical motors or actuators.
"""

from typing import Dict, Any


EXOSKELETON_MODES = {
    "BACK SUPPORT MODE": {
        "mode_id": "M_BACK_SUPPORT",
        "description": "Engages lumbar spine counter-torque mechanism designed for prolonged bending activities like transplanting, weeding, and low-level harvesting.",
        "target_activity": "Bending / Harvesting / Planting",
        "actuator_state": "ACTIVE EXTENSION",
        "nominal_torque_nm": 24.5,
        "max_torque_nm": 32.0,
        "nominal_power_w": 110.0,
        "muscle_relief_pct": 38.0,
        "primary_joints": ["Lumbar Spine Actuator", "Sacroiliac Elastic Support"],
        "badge_color": "#16A34A",
        "status_text": "ACTIVE LUMBAR TORQUE BOOST",
        "icon": "🛡️",
        "engineering_details": (
            "Applies proportional counter-moment to the upper torso via quasi-passive torsion springs "
            "and brushless DC actuators at the L4/L5 spinal joint, transferring load directly to the thighs."
        ),
    },
    "LIFTING ASSISTANCE MODE": {
        "mode_id": "M_LIFTING",
        "description": "Delivers dynamic parallel torque bursts to hip and knee joints during upward load lifting phases, protecting the lower lumbar spine.",
        "target_activity": "Lifting / Loading Sacks & Crates",
        "actuator_state": "SYNCHRONOUS BURST",
        "nominal_torque_nm": 30.0,
        "max_torque_nm": 42.0,
        "nominal_power_w": 165.0,
        "muscle_relief_pct": 44.0,
        "primary_joints": ["Bilateral Hip Motors", "Bilateral Knee Assist Bands", "Lumbar Spine"],
        "badge_color": "#D97706",
        "status_text": "HIGH TORQUE ASSIST READY",
        "icon": "⚡",
        "engineering_details": (
            "Detects vertical acceleration and knee extension using simulated IMU signals. Provides synchronized "
            "concentric torque assistance up to 42 Nm to reduce peak quadriceps and spinal disc compression."
        ),
    },
    "WALKING ASSISTANCE MODE": {
        "mode_id": "M_WALKING",
        "description": "Generates rhythmic hip flexion-extension cadence assistance to lower metabolic expenditure when walking across mud, furrows, or carrying sprayers.",
        "target_activity": "Walking / Field Patrol / Spraying",
        "actuator_state": "GAIT SYNCHRONIZATION",
        "nominal_torque_nm": 14.0,
        "max_torque_nm": 20.0,
        "nominal_power_w": 65.0,
        "muscle_relief_pct": 22.0,
        "primary_joints": ["Left Hip Servo", "Right Hip Servo"],
        "badge_color": "#0284C7",
        "status_text": "GAIT CADENCE SYNCHRONIZED",
        "icon": "🚶",
        "engineering_details": (
            "Uses simulated zero-velocity crossing phase detection to supply assistive push-off torque at terminal stance, "
            "reducing cardiovascular metabolic cost of transport by up to 20%."
        ),
    },
    "REST MODE": {
        "mode_id": "M_REST",
        "description": "Electromechanical clutches are fully disengaged, placing actuators in zero-impedance standby to permit natural seated resting and conserve power.",
        "target_activity": "Rest / Lunch Break / Seated Pauses",
        "actuator_state": "DISENGAGED / ZERO TORQUE",
        "nominal_torque_nm": 0.0,
        "max_torque_nm": 0.0,
        "nominal_power_w": 4.5,
        "muscle_relief_pct": 0.0,
        "primary_joints": ["All Actuators in Standby"],
        "badge_color": "#6B7280",
        "status_text": "PASSIVE STANDBY / CLUTCH DISENGAGED",
        "icon": "☕",
        "engineering_details": (
            "Actuator windings are disconnected via solid-state relays, eliminating back-EMF drag. Worker has complete "
            "unrestricted range of motion for comfortable recovery."
        ),
    },
}


def get_recommended_mode(posture: str, fatigue_risk_level: str) -> str:
    """
    Determines optimal conceptual exoskeleton mode based on real-time posture and fatigue state.
    """
    if fatigue_risk_level == "High":
        return "REST MODE"

    clean_p = posture.lower()
    if "bend" in clean_p:
        return "BACK SUPPORT MODE"
    elif "lift" in clean_p:
        return "LIFTING ASSISTANCE MODE"
    elif "walk" in clean_p:
        return "WALKING ASSISTANCE MODE"
    else:
        return "REST MODE"


def get_exoskeleton_telemetry(
    selected_mode: str,
    battery_pct: float = 84.0,
    worker_flexion_deg: float = 20.0,
) -> Dict[str, Any]:
    """
    Computes simulated real-time telemetry metrics for the active exoskeleton mode.
    """
    clean_mode = "REST MODE"
    for m in EXOSKELETON_MODES:
        if m.lower() in selected_mode.lower():
            clean_mode = m
            break

    profile = EXOSKELETON_MODES[clean_mode]

    # Calculate dynamic torque proportional to flexion if in back support
    if clean_mode == "BACK SUPPORT MODE":
        dynamic_torque = round(min(profile["max_torque_nm"], 8.0 + (worker_flexion_deg * 0.35)), 1)
        dynamic_power = round(min(150.0, 40.0 + (worker_flexion_deg * 1.5)), 1)
    elif clean_mode == "LIFTING ASSISTANCE MODE":
        dynamic_torque = profile["nominal_torque_nm"]
        dynamic_power = profile["nominal_power_w"]
    elif clean_mode == "WALKING ASSISTANCE MODE":
        dynamic_torque = profile["nominal_torque_nm"]
        dynamic_power = profile["nominal_power_w"]
    else:
        dynamic_torque = 0.0
        dynamic_power = 4.5

    # Actuator operating temperature simulation
    actuator_temp = round(32.0 + (dynamic_power / 10.0), 1)

    return {
        "mode_name": clean_mode,
        "mode_id": profile["mode_id"],
        "description": profile["description"],
        "target_activity": profile["target_activity"],
        "actuator_state": profile["actuator_state"],
        "status_text": profile["status_text"],
        "badge_color": profile["badge_color"],
        "icon": profile["icon"],
        "active_torque_nm": dynamic_torque,
        "max_torque_capacity_nm": profile["max_torque_nm"],
        "power_consumption_w": dynamic_power,
        "estimated_muscle_relief_pct": profile["muscle_relief_pct"],
        "actuator_temp_c": actuator_temp,
        "battery_pct": battery_pct,
        "primary_joints": profile["primary_joints"],
        "engineering_details": profile["engineering_details"],
        "is_simulation": True,
    }
