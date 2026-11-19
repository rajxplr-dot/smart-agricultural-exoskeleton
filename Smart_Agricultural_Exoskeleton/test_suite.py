"""
COMPREHENSIVE AUTOMATED TEST SUITE
Smart Agricultural Exoskeleton for Farm Workers with AI Assistance
Validates all modules, algorithms, edge cases, and data persistence.
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules import (
    sensor_simulation,
    posture_analysis,
    fatigue_analysis,
    ai_assistant,
    exoskeleton_simulation,
    data_manager,
)


class TestSmartAgriculturalExoskeleton(unittest.TestCase):

    def test_01_sensor_simulation_single(self):
        reading = sensor_simulation.generate_single_reading()
        self.assertIsInstance(reading, dict)
        self.assertIn("heart_rate_bpm", reading)
        self.assertIn("workload_percent", reading)
        self.assertIn("posture", reading)
        self.assertTrue(50 <= reading["heart_rate_bpm"] <= 170)
        self.assertTrue(0 <= reading["workload_percent"] <= 100)
        self.assertTrue(reading["is_simulated"])

    def test_02_sensor_simulation_initial_dataset(self):
        dataset = sensor_simulation.generate_initial_dataset(n_records=25, seed=42)
        self.assertEqual(len(dataset), 25)
        for r in dataset:
            self.assertIn("heart_rate_bpm", r)
            self.assertIn("posture", r)
            self.assertIn("working_hours", r)

    def test_03_posture_analysis(self):
        for post in ["Standing", "Bending", "Lifting", "Walking"]:
            res = posture_analysis.analyze_posture(post, flexion_angle_deg=45.0, workload_percent=60.0)
            self.assertEqual(res["detected_posture"], post)
            self.assertIn("ergonomic_risk_level", res)
            self.assertIn("reba_score", res)
            self.assertIn("posture_guidance", res)
            self.assertTrue(1.0 <= res["reba_score"] <= 12.0)

    def test_04_fatigue_risk_calculation(self):
        # Low risk scenario
        low_res = fatigue_analysis.calculate_fatigue_risk(
            heart_rate_bpm=68, workload_percent=30.0, working_hours=1.0, posture="Standing", ambient_temp_c=26.0
        )
        self.assertEqual(low_res["risk_level"], "Low")
        self.assertTrue(0 <= low_res["fatigue_score"] <= 34.0)

        # High risk scenario
        high_res = fatigue_analysis.calculate_fatigue_risk(
            heart_rate_bpm=140, workload_percent=92.0, working_hours=7.5, posture="Lifting", ambient_temp_c=36.0
        )
        self.assertEqual(high_res["risk_level"], "High")
        self.assertTrue(65.0 <= high_res["fatigue_score"] <= 100.0)

        # Moderate risk scenario
        mod_res = fatigue_analysis.calculate_fatigue_risk(
            heart_rate_bpm=105, workload_percent=65.0, working_hours=4.0, posture="Walking", ambient_temp_c=30.0
        )
        self.assertEqual(mod_res["risk_level"], "Moderate")
        self.assertTrue(35.0 <= mod_res["fatigue_score"] <= 64.0)

    def test_05_ai_assistant_recommendation(self):
        reading = sensor_simulation.generate_single_reading()
        post_info = posture_analysis.analyze_posture(reading["posture"])
        fat_info = fatigue_analysis.calculate_fatigue_risk(
            reading["heart_rate_bpm"], reading["workload_percent"], reading["working_hours"], reading["posture"]
        )
        rec = ai_assistant.generate_ai_recommendation(reading, post_info, fat_info)
        self.assertIn("priority_level", rec)
        self.assertIn("action_items", rec)
        self.assertIn("exoskeleton_directive", rec)
        self.assertTrue(len(rec["action_items"]) >= 2)

    def test_06_ai_knowledge_base_qa(self):
        ctx = {
            "sensor_reading": {"activity": "Rice Transplanting", "posture": "Bending"},
            "posture_info": {"detected_posture": "Bending", "reba_score": 8.5},
            "fatigue_info": {"fatigue_score": 62.0, "risk_level": "Moderate", "primary_driver": "Posture"},
        }
        ans = ai_assistant.query_ai_knowledge_base("Why is the worker flagged with Moderate risk?", ctx)
        self.assertIn("fatigue", ans.lower())

    def test_07_exoskeleton_modes(self):
        for mode in ["BACK SUPPORT MODE", "LIFTING ASSISTANCE MODE", "WALKING ASSISTANCE MODE", "REST MODE"]:
            telemetry = exoskeleton_simulation.get_exoskeleton_telemetry(mode, battery_pct=85.0, worker_flexion_deg=30.0)
            self.assertEqual(telemetry["mode_name"], mode)
            self.assertIn("active_torque_nm", telemetry)
            self.assertIn("estimated_muscle_relief_pct", telemetry)

    def test_08_data_manager_flow(self):
        records = data_manager.initialize_data_store()
        self.assertTrue(len(records) >= 20)

        # Enrich a new record and append
        raw = sensor_simulation.generate_single_reading()
        enriched = data_manager.enrich_record(raw)
        records.append(enriched)

        # Summary stats
        stats = data_manager.compute_summary_statistics(records)
        self.assertTrue(stats["total_records"] >= 21)
        self.assertTrue(stats["avg_heart_rate"] > 0)

        # CSV bytes
        csv_bytes = data_manager.generate_csv_download_bytes(records)
        self.assertTrue(len(csv_bytes) > 100)

        # Reset
        clean_recs = data_manager.reset_monitoring_data()
        self.assertEqual(len(clean_recs), 25)


if __name__ == "__main__":
    unittest.main()
