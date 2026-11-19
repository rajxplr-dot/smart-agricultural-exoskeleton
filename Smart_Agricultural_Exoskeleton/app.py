"""
=============================================================================
SMART AGRICULTURAL EXOSKELETON FOR FARM WORKERS WITH AI ASSISTANCE
Academic Engineering Software Prototype & Simulation Dashboard
Technology Stack: Streamlit, Pandas, NumPy, Plotly, Scikit-learn
=============================================================================
"""

import os
import sys
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure project root is in sys.path
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

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Agri-Exoskeleton AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional AgriTech Color Palette CSS
CUSTOM_CSS = """
<style>
    /* Global Background and Typography */
    .stApp {
        background-color: #F5F8F5;
        color: #17211B;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Headers styling */
    h1, h2, h3, h4 {
        color: #14532D !important;
        font-weight: 700 !important;
    }
    
    /* Card Component */
    .agri-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(20, 83, 45, 0.05), 0 2px 4px -1px rgba(20, 83, 45, 0.03);
        margin-bottom: 16px;
    }
    
    .agri-card-header {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #16A34A;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .agri-card-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #17211B;
    }
    
    .agri-card-subtitle {
        font-size: 0.82rem;
        color: #64748B;
        margin-top: 4px;
    }
    
    /* Badges */
    .badge-green {
        background-color: #DCFCE7;
        color: #14532D;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        border: 1px solid #86EFAC;
    }
    .badge-amber {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        border: 1px solid #FCD34D;
    }
    .badge-red {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        border: 1px solid #FCA5A5;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #14532D;
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #16A34A;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
    }
    
    /* Banner */
    .simulation-banner {
        background: linear-gradient(90deg, #14532D 0%, #16A34A 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT
# -----------------------------------------------------------------------------
if "records" not in st.session_state:
    st.session_state.records = data_manager.initialize_data_store()

if "current_reading" not in st.session_state or not st.session_state.current_reading:
    if st.session_state.records:
        st.session_state.current_reading = st.session_state.records[-1]
    else:
        raw_first = sensor_simulation.generate_single_reading()
        st.session_state.current_reading = data_manager.enrich_record(raw_first)
        st.session_state.records = [st.session_state.current_reading]

if "worker_idx" not in st.session_state:
    st.session_state.worker_idx = 0

if "exoskeleton_mode" not in st.session_state:
    rec_mode = exoskeleton_simulation.get_recommended_mode(
        st.session_state.current_reading.get("posture", "Bending"),
        st.session_state.current_reading.get("fatigue_risk_level", "Low"),
    )
    st.session_state.exoskeleton_mode = rec_mode

if "auto_sync_exo" not in st.session_state:
    st.session_state.auto_sync_exo = True


def trigger_generate_reading(activity_override=None):
    """Callback to generate a new simulated sensor reading and update session state."""
    last_rec = st.session_state.current_reading
    raw_new = sensor_simulation.generate_single_reading(
        worker_index=st.session_state.worker_idx,
        activity_override=activity_override,
        previous_reading=last_rec,
    )
    enriched = data_manager.enrich_record(raw_new)
    st.session_state.records.append(enriched)
    st.session_state.current_reading = enriched

    # Save to CSV
    data_manager.save_records_to_csv(st.session_state.records)

    # Auto sync exoskeleton mode if enabled
    if st.session_state.auto_sync_exo:
        st.session_state.exoskeleton_mode = exoskeleton_simulation.get_recommended_mode(
            enriched.get("posture", "Standing"),
            enriched.get("fatigue_risk_level", "Low"),
        )


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    # Logo & Brand Header
    logo_path = os.path.join(PROJECT_ROOT, "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)
    else:
        st.markdown("### 🌾 AGRI-EXO")

    st.markdown("## **Agri-Exoskeleton AI**")
    st.caption("Smart Worker Assistance Simulation | College Engineering Project")

    st.markdown("---")

    # Primary Navigation
    NAV_PAGES = [
        "1. Overview",
        "2. Worker Monitoring",
        "3. Posture Analysis",
        "4. AI Assistance",
        "5. Exoskeleton Simulation",
        "6. Analytics",
        "7. Reports",
        "8. About Project",
    ]
    selected_page = st.radio("Navigation Menu", NAV_PAGES, index=0)

    st.markdown("---")

    # Fast Action Button
    st.markdown("### ⚡ Quick Telemetry Generator")
    if st.button("Generate New Sensor Readings", key="sidebar_gen_btn", use_container_width=True):
        trigger_generate_reading()
        st.toast("Generated new simulated sensor reading!", icon="🌾")
        st.rerun()

    st.caption("ℹ️ *Generates real-time coherent synthetic physiological telemetry.*")

    st.markdown("---")
    st.markdown("### 👨‍🌾 Active Worker")
    worker_names = [f"{w['name']} ({w['id']})" for w in sensor_simulation.DEMO_WORKERS]
    chosen_worker = st.selectbox(
        "Select Worker",
        worker_names,
        index=st.session_state.worker_idx,
        label_visibility="collapsed",
    )
    new_idx = worker_names.index(chosen_worker)
    if new_idx != st.session_state.worker_idx:
        st.session_state.worker_idx = new_idx
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color: #64748B;'>Status: <b>100% Software Simulated</b><br>No physical hardware required.<br>Designed for Faculty Demonstration & Viva.</small>",
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 4. GLOBAL BANNER (DISCLAIMER & ACTIVE METRICS)
# -----------------------------------------------------------------------------
cur = st.session_state.current_reading
posture_info = posture_analysis.analyze_posture(
    cur.get("posture", "Standing"),
    cur.get("spine_flexion_deg", 0.0),
    cur.get("workload_percent", 50.0),
)
fatigue_info = fatigue_analysis.calculate_fatigue_risk(
    cur.get("heart_rate_bpm", 75),
    cur.get("workload_percent", 50.0),
    cur.get("working_hours", 2.0),
    cur.get("posture", "Standing"),
    cur.get("ambient_temp_c", 28.0),
)
ai_info = ai_assistant.generate_ai_recommendation(cur, posture_info, fatigue_info)
exo_info = exoskeleton_simulation.get_exoskeleton_telemetry(
    st.session_state.exoskeleton_mode,
    battery_pct=84.0,
    worker_flexion_deg=cur.get("spine_flexion_deg", 25.0),
)


# =============================================================================
# PAGE 1: OVERVIEW DASHBOARD
# =============================================================================
if selected_page == "1. Overview":
    st.markdown(
        f"""
        <div class="simulation-banner">
            <div>
                <h3 style="color: white !important; margin: 0; font-size: 1.3rem;">SMART AGRICULTURAL EXOSKELETON FOR FARM WORKERS WITH AI ASSISTANCE</h3>
                <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.88rem;">
                    Active Worker: <b>{cur.get('worker_name')} ({cur.get('worker_id')})</b> | Shift Duration: <b>{cur.get('working_hours', 1.0):.1f} hrs</b> | Telemetry: <b>SIMULATED LIVE</b>
                </p>
            </div>
            <div>
                <span style="background: rgba(255,255,255,0.25); padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">
                    🟢 {cur.get('monitoring_status', 'ACTIVE')}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top KPI Metrics Cards Row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        hr = cur.get("heart_rate_bpm", 75)
        hr_color = "#16A34A" if hr < 100 else ("#D97706" if hr < 130 else "#DC2626")
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">❤️ Heart Rate</div>
                <div class="agri-card-value" style="color: {hr_color};">{hr} <span style="font-size: 1rem; font-weight: 400;">BPM</span></div>
                <div class="agri-card-subtitle">Resting Baseline: 70 BPM</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        wl = cur.get("workload_percent", 50.0)
        wl_color = "#16A34A" if wl < 60 else ("#D97706" if wl < 80 else "#DC2626")
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">⚡ Workload Rate</div>
                <div class="agri-card-value" style="color: {wl_color};">{wl:.1f} <span style="font-size: 1rem; font-weight: 400;">%</span></div>
                <div class="agri-card-subtitle">Exertion intensity level</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        post = cur.get("posture", "Standing")
        p_badge = "badge-green" if post == "Standing" else ("badge-amber" if post == "Walking" else "badge-red")
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">🧘 Current Posture</div>
                <div class="agri-card-value" style="font-size: 1.45rem;">{post}</div>
                <div class="agri-card-subtitle"><span class="{p_badge}">{posture_info['ergonomic_risk_level']} Risk</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        f_score = fatigue_info["fatigue_score"]
        f_level = fatigue_info["risk_level"]
        f_badge = "badge-green" if f_level == "Low" else ("badge-amber" if f_level == "Moderate" else "badge-red")
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">🛡️ Fatigue Risk Score</div>
                <div class="agri-card-value" style="color: {fatigue_info['badge_color']};">{f_score} <span style="font-size: 0.9rem; font-weight: 400;">/100</span></div>
                <div class="agri-card-subtitle"><span class="{f_badge}">{f_level} Risk</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c5:
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">🦾 Exoskeleton Mode</div>
                <div class="agri-card-value" style="font-size: 1.15rem; color: #14532D;">{exo_info['icon']} {exo_info['mode_name']}</div>
                <div class="agri-card-subtitle" style="color: #16A34A; font-weight: 600;">{exo_info['status_text']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Secondary Showcase: Two-column layout
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.markdown("### 🤖 Latest AI Ergonomic Recommendation")
        st.markdown(
            f"""
            <div class="agri-card" style="border-left: 5px solid {fatigue_info['badge_color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 1rem; font-weight: 700; color: #14532D;">Priority: {ai_info['priority_level']}</span>
                    <span class="{'badge-green' if ai_info['risk_level']=='Low' else ('badge-amber' if ai_info['risk_level']=='Moderate' else 'badge-red')}">
                        Fatigue Score: {ai_info['fatigue_score']}/100
                    </span>
                </div>
                <p style="font-size: 0.92rem; color: #334155; margin-bottom: 12px;">
                    <b>Primary Strain Catalyst:</b> {fatigue_info['primary_driver']}
                </p>
                <div style="margin-bottom: 14px;">
                    <b>Action Plan:</b>
                    <ul style="margin-top: 6px; padding-left: 20px; font-size: 0.9rem; color: #1E293B;">
                        {''.join([f'<li style="margin-bottom: 4px;">{item}</li>' for item in ai_info['action_items']])}
                    </ul>
                </div>
                <div style="background-color: #F8FAFC; padding: 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                    <b>🦾 Exoskeleton Advisory Directive:</b><br>
                    <span style="font-size: 0.88rem; color: #0F172A;">{ai_info['exoskeleton_directive']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 📈 Recent Physiological Trends")
        df_hist = data_manager.get_records_dataframe(st.session_state.records).tail(15)
        if not df_hist.empty and len(df_hist) >= 2:
            fig_trends = go.Figure()
            fig_trends.add_trace(
                go.Scatter(
                    x=df_hist["working_hours"],
                    y=df_hist["heart_rate_bpm"],
                    mode="lines+markers",
                    name="Heart Rate (BPM)",
                    line=dict(color="#DC2626", width=2.5),
                    marker=dict(size=6),
                )
            )
            fig_trends.add_trace(
                go.Scatter(
                    x=df_hist["working_hours"],
                    y=df_hist["fatigue_risk_score"],
                    mode="lines+markers",
                    name="Fatigue Risk (0-100)",
                    line=dict(color="#16A34A", width=2.5),
                    marker=dict(size=6),
                )
            )
            fig_trends.update_layout(
                margin=dict(l=20, r=20, t=25, b=20),
                height=260,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="Shift Working Hours",
                yaxis_title="Value",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#FFFFFF",
            )
            st.plotly_chart(fig_trends, use_container_width=True)

    with col_right:
        st.markdown("### 🦾 Active Exoskeleton Telemetry")
        st.markdown(
            f"""
            <div class="agri-card" style="border-left: 5px solid #16A34A;">
                <div class="agri-card-header">Current Mode: {exo_info['mode_name']}</div>
                <p style="font-size: 0.88rem; color: #475569; margin-bottom: 12px;">{exo_info['description']}</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Active Torque Output</small><br>
                        <b style="font-size: 1.25rem; color: #14532D;">{exo_info['active_torque_nm']} Nm</b>
                    </div>
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Estimated Lumbar Relief</small><br>
                        <b style="font-size: 1.25rem; color: #16A34A;">{exo_info['estimated_muscle_relief_pct']}%</b>
                    </div>
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Power Draw</small><br>
                        <b style="font-size: 1.25rem; color: #334155;">{exo_info['power_consumption_w']} W</b>
                    </div>
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Actuator Temp</small><br>
                        <b style="font-size: 1.25rem; color: #D97706;">{exo_info['actuator_temp_c']} °C</b>
                    </div>
                </div>
                <p style="font-size: 0.82rem; color: #64748B; margin: 0;">
                    <b>Target Actuators:</b> {', '.join(exo_info['primary_joints'])}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 📊 Rapid Module Navigation")
        nav_c1, nav_c2 = st.columns(2)
        with nav_c1:
            st.info("🧘 **Posture Analysis**\nInspect lumbar flexion, REBA score & ergonomic guidance.")
            st.warning("🦾 **Exoskeleton Simulator**\nTest 4 assistance modes & biomechatronic relief.")
        with nav_c2:
            st.success("🤖 **AI Assistance Hub**\nExplore reasoning matrix & interactive viva Q&A.")
            st.info("📑 **Reports & CSV Data**\nExport telemetry history & statistical metrics.")


# =============================================================================
# PAGE 2: WORKER MONITORING SYSTEM
# =============================================================================
elif selected_page == "2. Worker Monitoring":
    st.markdown("## 🩺 Worker Telemetry Monitoring System")
    st.caption("Real-time physiological, biomechanical, and environmental sensor simulation.")

    # Control Bar
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.2, 1.2, 1.0])
    with ctrl_col1:
        st.markdown(f"**Current Subject:** `{cur.get('worker_name')} ({cur.get('worker_id')})`")
        st.markdown(f"**Experience:** `{cur.get('experience_years', 12)} years` | **Age:** `{cur.get('age', 35)} yrs`")
    with ctrl_col2:
        activity_choices = [a["activity"] for a in sensor_simulation.AGRICULTURAL_ACTIVITIES]
        chosen_act = st.selectbox("Simulate Specific Activity Override", ["Auto / Coherent"] + activity_choices)
    with ctrl_col3:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Generate New Sensor Readings", key="mon_gen_btn", use_container_width=True):
            act_override = None if chosen_act == "Auto / Coherent" else chosen_act
            trigger_generate_reading(activity_override=act_override)
            st.toast("Sensor telemetry stream updated!", icon="🩺")
            st.rerun()

    st.markdown("---")

    # Gauges Row using Plotly
    g1, g2, g3, g4 = st.columns(4)

    with g1:
        # Heart Rate Gauge
        hr_val = cur.get("heart_rate_bpm", 75)
        fig_hr = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=hr_val,
                title={"text": "Heart Rate (BPM)", "font": {"size": 16, "color": "#14532D"}},
                gauge={
                    "axis": {"range": [50, 160], "tickwidth": 1},
                    "bar": {"color": "#DC2626" if hr_val > 125 else ("#F59E0B" if hr_val > 95 else "#16A34A")},
                    "steps": [
                        {"range": [50, 95], "color": "#DCFCE7"},
                        {"range": [95, 125], "color": "#FEF3C7"},
                        {"range": [125, 160], "color": "#FEE2E2"},
                    ],
                    "threshold": {
                        "line": {"color": "black", "width": 2},
                        "thickness": 0.75,
                        "value": 140,
                    },
                },
            )
        )
        fig_hr.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hr, use_container_width=True)

    with g2:
        # Workload Gauge
        wl_val = cur.get("workload_percent", 50.0)
        fig_wl = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=wl_val,
                number={"suffix": "%"},
                title={"text": "Workload Intensity", "font": {"size": 16, "color": "#14532D"}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#16A34A" if wl_val < 60 else ("#F59E0B" if wl_val < 80 else "#DC2626")},
                    "steps": [
                        {"range": [0, 60], "color": "#E2E8F0"},
                        {"range": [60, 80], "color": "#FEF3C7"},
                        {"range": [80, 100], "color": "#FEE2E2"},
                    ],
                },
            )
        )
        fig_wl.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_wl, use_container_width=True)

    with g3:
        # Spine Flexion Angle Gauge
        flex_val = cur.get("spine_flexion_deg", 20.0)
        fig_flex = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=flex_val,
                number={"suffix": "°"},
                title={"text": "Spine Flexion Angle", "font": {"size": 16, "color": "#14532D"}},
                gauge={
                    "axis": {"range": [0, 90]},
                    "bar": {"color": "#DC2626" if flex_val > 55 else ("#F59E0B" if flex_val > 30 else "#16A34A")},
                    "steps": [
                        {"range": [0, 30], "color": "#DCFCE7"},
                        {"range": [30, 55], "color": "#FEF3C7"},
                        {"range": [55, 90], "color": "#FEE2E2"},
                    ],
                },
            )
        )
        fig_flex.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_flex, use_container_width=True)

    with g4:
        # Muscle Effort (sEMG %) Gauge
        emg_val = cur.get("muscle_effort_percent", 45.0)
        fig_emg = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=emg_val,
                number={"suffix": "%"},
                title={"text": "Muscle Effort (sEMG)", "font": {"size": 16, "color": "#14532D"}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#16A34A" if emg_val < 50 else ("#F59E0B" if emg_val < 75 else "#DC2626")},
                    "steps": [
                        {"range": [0, 50], "color": "#E2E8F0"},
                        {"range": [50, 75], "color": "#FEF3C7"},
                        {"range": [75, 100], "color": "#FEE2E2"},
                    ],
                },
            )
        )
        fig_emg.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_emg, use_container_width=True)

    # Detailed Telemetry Breakdown Cards
    det_c1, det_c2, det_c3 = st.columns(3)
    with det_c1:
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">Activity & Ergonomics</div>
                <p style="margin: 0; font-size: 1.05rem; font-weight: 600;">{cur.get('activity')}</p>
                <div style="margin-top: 8px;">Posture: <b>{cur.get('posture')}</b></div>
                <div style="margin-top: 4px;">Spine Flexion: <b>{cur.get('spine_flexion_deg', 0)}°</b></div>
                <div style="margin-top: 4px;">Muscle Effort: <b>{cur.get('muscle_effort_percent', 0)}%</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with det_c2:
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">Shift & Exposure</div>
                <p style="margin: 0; font-size: 1.05rem; font-weight: 600;">Working Hours: {cur.get('working_hours', 1.0):.1f} hrs</p>
                <div style="margin-top: 8px;">Ambient Temperature: <b>{cur.get('ambient_temp_c', 28)}°C</b></div>
                <div style="margin-top: 4px;">Heart Rate: <b>{cur.get('heart_rate_bpm')} BPM</b></div>
                <div style="margin-top: 4px;">Workload: <b>{cur.get('workload_percent'):.1f}%</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with det_c3:
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">Status & Simulation Mode</div>
                <p style="margin: 0; font-size: 1.05rem; font-weight: 600; color: #16A34A;">{cur.get('monitoring_status')}</p>
                <div style="margin-top: 8px;">Timestamp: <b>{cur.get('timestamp')}</b></div>
                <div style="margin-top: 4px;">Synthetic Mode: <b>Randomized Physical Coherence</b></div>
                <div style="margin-top: 4px; color: #64748B;"><small>Disclaimers: Telemetry simulated for demonstration</small></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 📋 Recent Telemetry Stream History")
    df_recent = data_manager.get_records_dataframe(st.session_state.records).tail(8)[
        ["timestamp", "activity", "posture", "heart_rate_bpm", "workload_percent", "working_hours", "fatigue_risk_score", "fatigue_risk_level"]
    ]
    st.dataframe(df_recent, use_container_width=True)


# =============================================================================
# PAGE 3: POSTURE DETECTION AND ANALYSIS
# =============================================================================
elif selected_page == "3. Posture Analysis":
    st.markdown("## 🧘 Posture Detection and Biomechanical Analysis")
    st.caption("Rule-based ergonomic classification and musculoskeletal strain assessment.")

    st.info(
        "💡 **Academic Methodology Notice:** Operates on rule-based algorithmic classification of simulated "
        "biomechanical markers (spine flexion angle, muscular effort, task load). "
        "Does NOT require camera hardware or deep-learning computer vision."
    )

    # Active Posture Breakdown Card
    p_col1, p_col2 = st.columns([1.1, 0.9])

    with p_col1:
        st.markdown(
            f"""
            <div class="agri-card" style="border-left: 6px solid {posture_info['risk_badge_color']};">
                <div class="agri-card-header">Active Detected Posture</div>
                <h2 style="margin: 0 0 8px 0; color: #14532D !important;">{posture_info['detected_posture']}</h2>
                <div style="margin-bottom: 12px;">
                    <span style="font-weight: 600;">Category:</span> {posture_info['posture_category']}<br>
                    <span style="font-weight: 600;">Ergonomic Risk:</span> 
                    <span style="color: {posture_info['risk_badge_color']}; font-weight: 700;">{posture_info['ergonomic_risk_level']}</span> |
                    <span style="font-weight: 600;">REBA Risk Index:</span> <b>{posture_info['reba_score']}/12</b>
                </div>
                <div style="background-color: #F8FAFC; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #E2E8F0;">
                    <b>⚠️ Biomechanical Strain Profile:</b><br>
                    <span style="font-size: 0.9rem; color: #334155;">{posture_info['spinal_strain_description']}</span>
                </div>
                <div style="background-color: #F0FDF4; padding: 12px; border-radius: 8px; border: 1px solid #BBF7D0;">
                    <b>🛡️ Ergonomic Corrective Guidance:</b><br>
                    <span style="font-size: 0.9rem; color: #166534;">{posture_info['posture_guidance']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with p_col2:
        st.markdown("### 🧪 Posture Scenario Simulator")
        st.caption("Select any posture to inspect ergonomic limits during viva demonstration:")
        sim_posture = st.selectbox("Inspect Posture Profile", ["Standing", "Bending", "Lifting", "Walking"])
        sim_res = posture_analysis.POSTURE_DATABASE[sim_posture]

        st.markdown(
            f"""
            <div class="agri-card">
                <b>Posture Profile:</b> {sim_posture}<br>
                <b>Base Category:</b> {sim_res['category']}<br>
                <b>Base Risk Tier:</b> <span style="color: {sim_res['risk_badge_color']}; font-weight: 700;">{sim_res['base_risk']}</span><br>
                <b>Typical REBA Scale:</b> {sim_res['reba_range'][0]} - {sim_res['reba_range'][1]} / 12<br>
                <b>Ergonomic Risk Weight:</b> {sim_res['risk_weight']*100:.0f}%<br>
                <div style="margin-top: 10px; font-size: 0.88rem; color: #475569;">
                    <b>Guidance:</b> {sim_res['guidance']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Posture Distribution in Current Dataset
    st.markdown("### 📊 Dataset Posture Distribution Analysis")
    dist_info = posture_analysis.compute_posture_distribution(st.session_state.records)

    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        # Donut Chart
        labels = list(dist_info["counts"].keys())
        values = list(dist_info["counts"].values())
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.45,
                    marker=dict(colors=["#16A34A", "#DC2626", "#D97706", "#0284C7"]),
                )
            ]
        )
        fig_donut.update_layout(
            title="Posture Occurrence Breakdown",
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c_chart2:
        # Bar Chart of Average Workload per Posture
        df_all = data_manager.get_records_dataframe(st.session_state.records)
        if not df_all.empty and "posture" in df_all.columns:
            df_grp = df_all.groupby("posture")["workload_percent"].mean().reset_index()
            fig_bar = px.bar(
                df_grp,
                x="posture",
                y="workload_percent",
                color="posture",
                title="Average Workload Intensity per Posture (%)",
                color_discrete_map={"Standing": "#16A34A", "Bending": "#DC2626", "Lifting": "#D97706", "Walking": "#0284C7"},
            )
            fig_bar.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)


# =============================================================================
# PAGE 4: AI ASSISTANCE SYSTEM
# =============================================================================
elif selected_page == "4. AI Assistance":
    st.markdown("## 🤖 Contextual AI Assistance System")
    st.caption("Transparent heuristic reasoning engine formulating personalized worker guidance.")

    st.markdown(
        f"""
        <div class="simulation-banner">
            <div>
                <h4 style="color: white !important; margin: 0;">AI DECISION MATRIX: {ai_info['priority_level']}</h4>
                <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.88rem;">
                    Derived from real-time telemetry inputs (Heart Rate: {cur.get('heart_rate_bpm')} BPM | Workload: {cur.get('workload_percent'):.1f}% | Posture: {cur.get('posture')})
                </p>
            </div>
            <div>
                <span class="{'badge-green' if ai_info['risk_level']=='Low' else ('badge-amber' if ai_info['risk_level']=='Moderate' else 'badge-red')}">
                    {ai_info['risk_level']} Fatigue Tier
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_rec1, col_rec2 = st.columns([1.1, 0.9])

    with col_rec1:
        st.markdown("### 📋 Prescribed Ergonomic Action Plan")
        for idx, item in enumerate(ai_info["action_items"]):
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border-left: 4px solid #16A34A; border-radius: 8px; padding: 12px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <b>Step {idx+1}:</b> {item}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if ai_info["suggested_break_minutes"] > 0:
            st.warning(f"⏱️ **Recommended Break:** Mandatory {ai_info['suggested_break_minutes']} minute seated rest in shaded field area.")
        else:
            st.success("⏱️ **Pacing:** Continue current work schedule with standard hydration intervals.")

    with col_rec2:
        st.markdown("### 🧮 Fatigue Score Component Breakdown")
        cb = fatigue_info["contributions"]
        df_cb = pd.DataFrame(
            {
                "Parameter": list(cb.keys()),
                "Score Contribution (pts)": list(cb.values()),
            }
        )
        fig_pie_cb = px.pie(
            df_cb,
            names="Parameter",
            values="Score Contribution (pts)",
            title=f"Total Risk: {fatigue_info['fatigue_score']}/100",
            color_discrete_sequence=["#DC2626", "#D97706", "#2563EB", "#16A34A"],
        )
        fig_pie_cb.update_layout(height=260, margin=dict(l=10, r=10, t=35, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie_cb, use_container_width=True)

        st.caption(f"**Primary Risk Driver:** `{fatigue_info['primary_driver']}`")

    st.markdown("---")

    # Interactive Viva / Faculty Q&A Assistant Hub
    st.markdown("### 🎓 Interactive Academic Viva Q&A Hub")
    st.caption("Ask technical questions to demonstrate AI reasoning during faculty evaluations:")

    preset_questions = [
        "Why is the worker flagged with the current risk score?",
        "How does the exoskeleton decide torque and assistance mode?",
        "What biomechanical risks occur during sustained rice transplanting?",
        "Explain the mathematical formulation behind the fatigue score.",
    ]
    selected_preset = st.selectbox("Select Common Viva Demonstration Question:", preset_questions)

    custom_q = st.text_input("Or enter a custom question for the AI Assistant:")
    query_to_run = custom_q.strip() if custom_q.strip() else selected_preset

    if st.button("Run AI Query Inference", key="viva_q_btn"):
        ctx = {
            "sensor_reading": cur,
            "posture_info": posture_info,
            "fatigue_info": fatigue_info,
        }
        answer = ai_assistant.query_ai_knowledge_base(query_to_run, ctx)
        st.markdown(
            f"""
            <div style="background-color: #F0FDF4; border-left: 5px solid #16A34A; border-radius: 8px; padding: 16px; margin-top: 10px;">
                <b style="color: #14532D;">🤖 AI Assistant Explanation:</b><br>
                <p style="margin-top: 8px; font-size: 0.95rem; color: #17211B;">{answer}</p>
                <small style="color: #64748B;">Grounding: Evaluated using deterministic agricultural biomechanical heuristics.</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# PAGE 5: EXOSKELETON ASSISTANCE SIMULATION
# =============================================================================
elif selected_page == "5. Exoskeleton Simulation":
    st.markdown("## 🦾 Conceptual Exoskeleton Assistance Simulation")
    st.caption("Biomechatronic assistive mode controller and mechanical load offloading simulation.")

    st.warning(
        "⚠️ **Simulation Disclaimer:** Demonstrates conceptual software logic, control algorithms, and biomechatronic telemetry. "
        "Does not drive physical motors, actuators, or physical hardware."
    )

    # Mode Selector Tabs
    mode_names = list(exoskeleton_simulation.EXOSKELETON_MODES.keys())
    current_mode_idx = mode_names.index(st.session_state.exoskeleton_mode) if st.session_state.exoskeleton_mode in mode_names else 0

    exo_c1, exo_c2 = st.columns([1.2, 0.8])
    with exo_c1:
        st.markdown("### Select Simulated Assistance Mode:")
        chosen_mode = st.radio(
            "Assistance Modes",
            mode_names,
            index=current_mode_idx,
            horizontal=True,
            label_visibility="collapsed",
        )
        if chosen_mode != st.session_state.exoskeleton_mode:
            st.session_state.exoskeleton_mode = chosen_mode
            st.rerun()

    with exo_c2:
        st.markdown("### Automatic Mode Synchronization")
        sync_toggle = st.checkbox(
            "Auto-Sync Mode with Worker Posture",
            value=st.session_state.auto_sync_exo,
            help="Automatically switches exoskeleton mode according to the real-time posture.",
        )
        if sync_toggle != st.session_state.auto_sync_exo:
            st.session_state.auto_sync_exo = sync_toggle
            st.rerun()

        rec_mode = exoskeleton_simulation.get_recommended_mode(cur.get("posture", "Standing"), fatigue_info["risk_level"])
        st.caption(f"Suggested for current state: **{rec_mode}**")

    st.markdown("---")

    # Mode Telemetry Card
    exo_now = exoskeleton_simulation.get_exoskeleton_telemetry(
        st.session_state.exoskeleton_mode,
        battery_pct=84.0,
        worker_flexion_deg=cur.get("spine_flexion_deg", 25.0),
    )

    m_col1, m_col2 = st.columns([1.1, 0.9])

    with m_col1:
        st.markdown(
            f"""
            <div class="agri-card" style="border-left: 6px solid {exo_now['badge_color']};">
                <div class="agri-card-header">{exo_now['icon']} {exo_now['mode_name']} [{exo_now['mode_id']}]</div>
                <h3 style="margin: 0 0 8px 0; color: #14532D !important;">Status: {exo_now['status_text']}</h3>
                <p style="color: #475569; font-size: 0.92rem; margin-bottom: 14px;">{exo_now['description']}</p>
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                    <b>⚙️ Engineering Biomechatronic Actuation:</b><br>
                    <span style="font-size: 0.88rem; color: #334155;">{exo_now['engineering_details']}</span>
                </div>
                <div style="font-size: 0.88rem; color: #1E293B;">
                    <b>Target Agricultural Activities:</b> {exo_now['target_activity']}<br>
                    <b>Active Articulations:</b> {', '.join(exo_now['primary_joints'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m_col2:
        # Actuator Telemetry Dashboard
        st.markdown(
            f"""
            <div class="agri-card">
                <div class="agri-card-header">Simulated Actuator Telemetry</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Active Assist Torque</small><br>
                        <b style="font-size: 1.4rem; color: #14532D;">{exo_now['active_torque_nm']} Nm</b>
                        <div style="font-size: 0.75rem; color: #64748B;">Max: {exo_now['max_torque_capacity_nm']} Nm</div>
                    </div>
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Lumbar Muscle Relief</small><br>
                        <b style="font-size: 1.4rem; color: #16A34A;">{exo_now['estimated_muscle_relief_pct']}%</b>
                        <div style="font-size: 0.75rem; color: #64748B;">Erector Spinae offload</div>
                    </div>
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Power Draw</small><br>
                        <b style="font-size: 1.4rem; color: #334155;">{exo_now['power_consumption_w']} W</b>
                        <div style="font-size: 0.75rem; color: #64748B;">24V DC battery bus</div>
                    </div>
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 8px;">
                        <small style="color: #64748B;">Actuator Temp</small><br>
                        <b style="font-size: 1.4rem; color: #D97706;">{exo_now['actuator_temp_c']} °C</b>
                        <div style="font-size: 0.75rem; color: #64748B;">Within safe thermal envelope</div>
                    </div>
                </div>
                <div style="margin-top: 12px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                        <span>Battery Reserve: <b>{exo_now['battery_pct']}%</b></span>
                        <span style="color: #16A34A;">Estimated Runtime: ~5.4 hrs</span>
                    </div>
                    <div style="background: #E2E8F0; border-radius: 4px; height: 8px; margin-top: 4px;">
                        <div style="background: #16A34A; width: {exo_now['battery_pct']}%; height: 8px; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Joint Load Radar Chart
    st.markdown("### 🕸️ Joint Assistance Distribution (Simulated)")
    joints = ["Lumbar L4/L5", "Left Hip", "Right Hip", "Left Knee", "Right Knee"]
    if exo_now["mode_name"] == "BACK SUPPORT MODE":
        load_vals = [90, 45, 45, 30, 30]
    elif exo_now["mode_name"] == "LIFTING ASSISTANCE MODE":
        load_vals = [85, 80, 80, 75, 75]
    elif exo_now["mode_name"] == "WALKING ASSISTANCE MODE":
        load_vals = [25, 70, 70, 40, 40]
    else:
        load_vals = [0, 0, 0, 0, 0]

    fig_radar = go.Figure()
    fig_radar.add_trace(
        go.Scatterpolar(
            r=load_vals + [load_vals[0]],
            theta=joints + [joints[0]],
            fill="toself",
            name="Assistance Load %",
            line=dict(color="#16A34A"),
            fillcolor="rgba(22, 163, 74, 0.25)",
        )
    )
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=320,
        margin=dict(l=40, r=40, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_radar, use_container_width=True)


# =============================================================================
# PAGE 6: ANALYTICS DASHBOARD
# =============================================================================
elif selected_page == "6. Analytics":
    st.markdown("## 📊 Historical Telemetry & Ergonomic Analytics")
    st.caption("Interactive Plotly visual analytics covering physiological, temporal, and postural telemetry.")

    df_hist = data_manager.get_records_dataframe(st.session_state.records)

    if df_hist.empty:
        st.warning("No telemetry records available. Click 'Generate New Sensor Readings' to create data.")
    else:
        # High-level Statistics Banner
        stats = data_manager.compute_summary_statistics(st.session_state.records)
        s1, s2, s3, s4, s5 = st.columns(5)
        with s1:
            st.metric("Total Records", stats["total_records"])
        with s2:
            st.metric("Avg Heart Rate", f"{stats['avg_heart_rate']} BPM")
        with s3:
            st.metric("Avg Workload", f"{stats['avg_workload']}%")
        with s4:
            st.metric("Max Shift Duration", f"{stats['max_hours']} hrs")
        with s5:
            st.metric("High Risk Incidents", stats["high_risk_count"])

        st.markdown("---")

        # Row 1: Heart Rate and Fatigue Trends
        c_an1, c_an2 = st.columns(2)

        with c_an1:
            fig_hr_hist = px.line(
                df_hist,
                x="working_hours",
                y="heart_rate_bpm",
                markers=True,
                title="Heart Rate Progression vs Shift Duration",
                labels={"working_hours": "Working Hours (hrs)", "heart_rate_bpm": "Heart Rate (BPM)"},
                color_discrete_sequence=["#DC2626"],
            )
            # Add safe threshold line
            fig_hr_hist.add_hline(y=100, line_dash="dash", line_color="#F59E0B", annotation_text="Moderate Limit (100 BPM)")
            fig_hr_hist.add_hline(y=130, line_dash="dot", line_color="#DC2626", annotation_text="High Limit (130 BPM)")
            fig_hr_hist.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_hr_hist, use_container_width=True)

        with c_an2:
            fig_fatigue_hist = px.line(
                df_hist,
                x="working_hours",
                y="fatigue_risk_score",
                markers=True,
                title="Fatigue Risk Score Accumulation Trend",
                labels={"working_hours": "Working Hours (hrs)", "fatigue_risk_score": "Fatigue Risk (0-100)"},
                color_discrete_sequence=["#16A34A"],
            )
            fig_fatigue_hist.add_hline(y=35, line_dash="dash", line_color="#F59E0B", annotation_text="Moderate Risk (35)")
            fig_fatigue_hist.add_hline(y=65, line_dash="dot", line_color="#DC2626", annotation_text="High Risk (65)")
            fig_fatigue_hist.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_fatigue_hist, use_container_width=True)

        # Row 2: Workload vs Heart Rate Scatter & REBA vs Hours
        c_an3, c_an4 = st.columns(2)

        with c_an3:
            fig_scatter = px.scatter(
                df_hist,
                x="workload_percent",
                y="heart_rate_bpm",
                color="fatigue_risk_level",
                size="working_hours",
                hover_data=["activity", "posture"],
                title="Workload % vs Heart Rate Correlation (Bubble Size = Hours)",
                color_discrete_map={"Low": "#16A34A", "Moderate": "#F59E0B", "High": "#DC2626"},
            )
            fig_scatter.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_scatter, use_container_width=True)

        with c_an4:
            fig_reba = px.bar(
                df_hist,
                x="working_hours",
                y="reba_score",
                color="posture",
                title="REBA Ergonomic Risk Score per Telemetry Sample",
                labels={"working_hours": "Working Hours", "reba_score": "REBA Score (1-12)"},
                color_discrete_map={"Standing": "#16A34A", "Bending": "#DC2626", "Lifting": "#D97706", "Walking": "#0284C7"},
            )
            fig_reba.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_reba, use_container_width=True)


# =============================================================================
# PAGE 7: REPORTS AND DATA MANAGEMENT
# =============================================================================
elif selected_page == "7. Reports":
    st.markdown("## 📑 Telemetry Reports & Local Data Management")
    st.caption("Export CSV reports, inspect worker records, or reset baseline demonstration data.")

    df_records = data_manager.get_records_dataframe(st.session_state.records)

    # Actions Bar: Export & Reset
    act_col1, act_col2 = st.columns([1.2, 0.8])

    with act_col1:
        st.markdown("### 📥 Download Monitoring Report")
        if not df_records.empty:
            csv_bytes = data_manager.generate_csv_download_bytes(st.session_state.records)
            timestamp_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agri_exoskeleton_report_{timestamp_now}.csv"
            st.download_button(
                label="📥 Download Complete Telemetry Report (CSV)",
                data=csv_bytes,
                file_name=filename,
                mime="text/csv",
                use_container_width=True,
            )
            st.caption(f"Includes all {len(df_records)} logged telemetry samples and AI recommendations.")

    with act_col2:
        st.markdown("### 🔄 Reset Session Data")
        confirm_reset = st.checkbox("Confirm reset to clean baseline (25 records)")
        if st.button("Reset Monitoring Data", disabled=not confirm_reset, use_container_width=True):
            st.session_state.records = data_manager.reset_monitoring_data()
            st.session_state.current_reading = st.session_state.records[-1]
            st.toast("Monitoring data reset to clean demonstration baseline!", icon="🔄")
            st.rerun()

    st.markdown("---")

    # Data Filter and View
    st.markdown("### 🗄️ Full Telemetry Records Table")
    filt_col1, filt_col2 = st.columns(2)
    with filt_col1:
        post_filter = st.multiselect("Filter by Posture:", ["Standing", "Bending", "Lifting", "Walking"], default=[])
    with filt_col2:
        risk_filter = st.multiselect("Filter by Fatigue Risk Tier:", ["Low", "Moderate", "High"], default=[])

    df_filtered = df_records.copy()
    if post_filter:
        df_filtered = df_filtered[df_filtered["posture"].isin(post_filter)]
    if risk_filter:
        df_filtered = df_filtered[df_filtered["fatigue_risk_level"].isin(risk_filter)]

    st.dataframe(df_filtered, use_container_width=True, height=380)
    st.caption(f"Displaying {len(df_filtered)} of {len(df_records)} recorded records.")


# =============================================================================
# PAGE 8: ABOUT PROJECT (ACADEMIC VIVA PRESENTATION GUIDE)
# =============================================================================
elif selected_page == "8. About Project":
    st.markdown("## ℹ️ Project Architecture & Academic Viva Guide")
    st.caption("College Engineering Project Dossier: SMART AGRICULTURAL EXOSKELETON FOR FARM WORKERS WITH AI ASSISTANCE")

    tab1, tab2, tab3, tab4 = st.tabs(["Abstract & Objectives", "Mathematical Formulation", "System Architecture", "Viva Q&A Cheatsheet"])

    with tab1:
        st.markdown(
            """
            ### 1. Abstract
            Agricultural laborers in developing and agrarian nations perform physically grueling manual tasks—such as 
            sustained bending during rice transplanting, heavy manual load carrying, knapsack chemical spraying, and weeding—under 
            harsh microclimatic conditions. These continuous biomechanical stresses cause early musculoskeletal disorders (MSDs), 
            specifically chronic lumbar back pain and joint degradation.
            
            This project introduces a **Smart Agricultural Exoskeleton for Farm Workers with AI Assistance**. 
            It is a 100% software-based engineering prototype demonstrating the integration of physiological sensor simulation, 
            rule-based ergonomic posture detection, a mathematical fatigue risk estimation algorithm, an explainable contextual 
            AI advisor, and a 4-mode biomechatronic exoskeleton simulation.
            
            ### 2. Key Objectives
            - **Simulate Real-time Physiological Telemetry:** Generate coherent synthetic farm worker data (Heart Rate, Workload %, Spine Flexion Angle, Duration).
            - **Algorithmic Ergonomic Posture Assessment:** Quantify postural risks (Standing, Bending, Lifting, Walking) and compute illustrative REBA scores.
            - **Mathematical Fatigue Risk Modeling:** Score cumulative fatigue on an intuitive 0–100 scale with transparent parameter attribution.
            - **Explainable AI Recommendations:** Provide immediate actionable ergonomic interventions without opaque black-box APIs.
            - **Conceptual Biomechatronic Exoskeleton Simulation:** Model assistive joint torque offloading across 4 operational modes.
            """
        )

    with tab2:
        st.markdown(
            r"""
            ### Mathematical Fatigue-Risk Scoring Formula
            
            The system employs a multi-attribute weighted scoring model calculating an index $S \in [0, 100]$:
            
            $$S = w_{HR} \cdot S_{HR} + w_{WL} \cdot S_{WL} + w_{DUR} \cdot S_{DUR} + w_{POST} \cdot S_{POST} + \Delta_{Heat}$$
            
            #### Parameter Normalization:
            1. **Cardiovascular Stress ($S_{HR}$, Weight $w_{HR} = 0.30$):**
               $$S_{HR} = \text{clip}\left(\frac{\text{HR} - 60}{140 - 60}, 0, 1\right) \times 100$$
            2. **Workload Intensity ($S_{WL}$, Weight $w_{WL} = 0.30$):**
               $$S_{WL} = \text{Workload Percentage} \in [0, 100]$$
            3. **Shift Duration Fatigue Accumulation ($S_{DUR}$, Weight $w_{DUR} = 0.20$):**
               $$S_{DUR} = \text{clip}\left(\frac{\text{Hours}}{8.0}, 0, 1.2\right) \times 100$$
            4. **Postural Ergonomic Multiplier ($S_{POST}$, Weight $w_{POST} = 0.20$):**
               - Standing: $30.0$ pts
               - Walking: $50.0$ pts
               - Bending: $85.0$ pts
               - Lifting: $95.0$ pts
            5. **Thermal Microclimate Modifier ($\Delta_{Heat}$):**
               - $+2.0$ pts if Ambient Temp $> 32^\circ\text{C}$
               - $+4.0$ pts if Ambient Temp $> 35^\circ\text{C}$
            
            #### Academic Classification Thresholds:
            - **$0 \le S \le 34$:** **Low Risk** (Normal physiological envelope; standard pacing)
            - **$35 \le S \le 64$:** **Moderate Risk** (Caution; fatigue accumulating; short rest advised)
            - **$65 \le S \le 100$:** **High Risk** (Critical fatigue; immediate work pause mandated)
            """
        )

    with tab3:
        st.markdown(
            """
            ### Modular System Architecture
            
            ```
            Smart_Agricultural_Exoskeleton/
            │
            ├── app.py                      # Main Streamlit Web Application & Navigation
            │
            ├── modules/
            │   ├── sensor_simulation.py    # Generates synthetic physiological & biomechanical data
            │   ├── posture_analysis.py     # Rule-based ergonomic classification & REBA indices
            │   ├── fatigue_analysis.py     # Mathematical fatigue scoring algorithm
            │   ├── ai_assistant.py         # Contextual heuristic AI recommendations & Viva Q&A
            │   ├── exoskeleton_simulation.py# 4-mode biomechatronic torque assistance model
            │   └── data_manager.py         # CSV persistence, summaries, and report downloads
            │
            ├── data/
            │   └── sample_worker_data.csv  # Local reproducible demonstration dataset
            │
            ├── assets/
            │   └── logo.png                # High-resolution project logo
            │
            ├── requirements.txt            # Python dependencies
            ├── README.md                   # Setup and execution guide
            └── PROJECT_DOCUMENTATION.md    # Comprehensive academic project report
            ```
            """
        )

    with tab4:
        st.markdown(
            """
            ### Academic Viva Questions & Answers Cheatsheet
            
            **Q1: Why is this project implemented purely in software without physical hardware?**  
            *Answer:* Physical agricultural exoskeletons require precision CNC machining, custom high-torque BLDC planetary gearboxes, and safety certifications before human deployment. This project establishes the software intelligence, sensor fusion algorithms, and control heuristics that govern such an exoskeleton, delivering a functional proof-of-concept ready for testing and validation.
            
            **Q2: How does the AI Assistant formulate recommendations?**  
            *Answer:* It uses a deterministic, rule-based expert heuristic matrix. It correlates the calculated fatigue score, heart rate, workload, and posture to generate clear, priority-rated ergonomic guidance with complete transparency (no black-box unexplainable decisions).
            
            **Q3: What are the 4 Exoskeleton Modes and when are they triggered?**  
            *Answer:*  
            1. **Back Support Mode:** Active during trunk bending (>30° flexion) to relieve erector spinae strain.
            2. **Lifting Assistance Mode:** Active during crate/sack lifts to provide torque bursts to hips and knees.
            3. **Walking Assistance Mode:** Active during furrow patrol or spraying to assist hip flexion-extension cadence.
            4. **Rest Mode:** Disengages clutches to permit unconstrained sitting and save battery.
            
            **Q4: What is the REBA score used in the Posture module?**  
            *Answer:* REBA (Rapid Entire Body Assessment) is an internationally recognized ergonomic postural assessment tool that scores musculoskeletal disorder risk on a scale from 1 (negligible) to 12+ (very high).
            
            **Q5: What are the future enhancements planned?**  
            *Answer:* Real wearable IMU/EMG hardware integration, on-device Edge AI inference, Computer Vision posture estimation via camera, and physical prototype fabrication.
            """
        )

# -----------------------------------------------------------------------------
# End of app.py
# -----------------------------------------------------------------------------
