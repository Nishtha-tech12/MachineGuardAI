# ============================================================
# MachineGuardAI — Streamlit Frontend
# AI-Powered Predictive Maintenance System
# ============================================================

import streamlit as st

# ── Page configuration ───────────────────────────────────────
st.set_page_config(
    page_title="MachineGuardAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — industrial blue & white theme ────────────────
st.markdown(
    """
    <style>
        /* ---- Global background & font ---- */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f0f4f8;
            font-family: 'Segoe UI', sans-serif;
        }

        /* ---- Top header bar ---- */
        [data-testid="stHeader"] {
            background-color: #0a2540;
        }

        /* ---- Sidebar ---- */
        [data-testid="stSidebar"] {
            background-color: #0a2540;
        }
        [data-testid="stSidebar"] * {
            color: #cbd5e1 !important;
        }
        .sidebar-logo {
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff !important;
            letter-spacing: 0.3px;
            padding: 4px 0 12px 0;
        }
        .sidebar-nav-item {
            display: block;
            padding: 10px 14px;
            border-radius: 7px;
            font-size: 0.92rem;
            font-weight: 500;
            color: #94a3b8 !important;
            text-decoration: none;
            margin-bottom: 4px;
            transition: background 0.15s;
        }
        .sidebar-nav-item.active {
            background-color: #1d6fce22;
            color: #93c5fd !important;
            border-left: 3px solid #1d6fce;
        }
        .sidebar-status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 7px;
        }

        /* ── Hero section ── */
        .hero {
            background-color: #0a2540;
            border-radius: 14px;
            padding: 56px 48px 52px 48px;
            margin-bottom: 36px;
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: "";
            position: absolute;
            top: -60px; right: -60px;
            width: 260px; height: 260px;
            border-radius: 50%;
            background: #1d6fce18;
        }
        .hero-eyebrow {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            color: #60a5fa;
            margin-bottom: 16px;
        }
        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.2;
            margin: 0 0 18px 0;
            letter-spacing: -0.5px;
        }
        .hero-title span {
            color: #60a5fa;
        }
        .hero-desc {
            font-size: 1rem;
            color: #94a3b8;
            line-height: 1.7;
            max-width: 580px;
            margin: 0 0 32px 0;
        }
        .hero-badge {
            display: inline-block;
            background-color: #1d3a5f;
            color: #93c5fd;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 5px 14px;
            border-radius: 20px;
            margin-right: 8px;
            border: 1px solid #1d6fce44;
        }

        /* ── Feature cards ── */
        .feature-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 28px 24px;
            height: 100%;
            transition: border-color 0.2s;
        }
        .feature-card:hover {
            border-color: #1d6fce;
        }
        .feature-icon {
            width: 44px;
            height: 44px;
            background-color: #eff6ff;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            margin-bottom: 16px;
        }
        .feature-card h4 {
            color: #0a2540;
            font-size: 1rem;
            font-weight: 700;
            margin: 0 0 8px 0;
        }
        .feature-card p {
            color: #64748b;
            font-size: 0.88rem;
            line-height: 1.6;
            margin: 0;
        }

        /* ── Info cards (welcome section) ── */
        .info-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #1d6fce;
            border-radius: 10px;
            padding: 26px 28px;
            margin-bottom: 20px;
        }
        .info-card h3 {
            color: #0a2540;
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0 0 10px 0;
        }
        .info-card p {
            color: #4b5563;
            font-size: 0.92rem;
            line-height: 1.65;
            margin: 0;
        }

        /* ── Section heading ── */
        .section-heading {
            font-size: 1.3rem;
            font-weight: 700;
            color: #0a2540;
            border-bottom: 2px solid #dbeafe;
            padding-bottom: 10px;
            margin-bottom: 24px;
        }

        /* ── CTA card ── */
        .cta-card {
            background: linear-gradient(135deg, #0a2540 0%, #1a4a7a 100%);
            border-radius: 12px;
            padding: 36px 32px;
            color: #ffffff;
            margin-bottom: 20px;
        }
        .cta-card h3 {
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0 0 10px 0;
            color: #ffffff;
        }
        .cta-card p {
            font-size: 0.92rem;
            color: #94a3b8;
            line-height: 1.6;
            margin: 0 0 24px 0;
        }

        /* ── Primary button ── */
        div[data-testid="stButton"] > button {
            background-color: #1d6fce;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 13px 32px;
            font-size: 0.98rem;
            font-weight: 600;
            cursor: pointer;
            letter-spacing: 0.3px;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #1558a8;
            color: #ffffff;
        }

        /* ── Divider ── */
        .divider {
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 8px 0 16px 0;
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 0.78rem;
            padding: 28px 0 8px 0;
            border-top: 1px solid #e2e8f0;
            margin-top: 52px;
        }
        /* Hide only the Deploy button/toolbar */
        [data-testid="stToolbar"] {
        display: none !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(
        "<div class='sidebar-logo'>🤖 MachineGuardAI</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Navigation — Home is active on the landing page
    st.markdown("**NAVIGATION**")
    st.markdown(
        """
        <a class="sidebar-nav-item active">🏠 &nbsp; Home</a>
        <a class="sidebar-nav-item">⚡ &nbsp; Predict Machine</a>
        <a class="sidebar-nav-item">ℹ️ &nbsp; About</a>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # System status
    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        """
        <p style="margin:6px 0; font-size:0.88rem;">
            <span class="sidebar-status-dot" style="background:#22c55e;"></span>System Online
        </p>
        <p style="margin:6px 0; font-size:0.88rem;">
            <span class="sidebar-status-dot" style="background:#3b82f6;"></span>Model Ready
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(
        "<span style='font-size:0.74rem; color:#475569;'>v1.0.0 · MachineGuardAI</span>",
        unsafe_allow_html=True,
    )

# ── Hero Section ─────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">🤖 AI-Powered Predictive Maintenance</div>
        <h1 class="hero-title">
            Prevent Downtime<br><span>Before It Happens</span>
        </h1>
        <p class="hero-desc">
            MachineGuardAI analyses real-time industrial sensor data to detect
            early signs of equipment failure — giving your team the foresight to
            act before a breakdown occurs, reduce unplanned downtime, and maximise
            asset lifespan.
        </p>
        <span class="hero-badge">🔬 Machine Learning</span>
        <span class="hero-badge">📡 Sensor Analytics</span>
        <span class="hero-badge">⚙️ Industrial IoT</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Feature Cards Row ─────────────────────────────────────────
st.markdown(
    '<p class="section-heading">Platform Capabilities</p>',
    unsafe_allow_html=True,
)

fc1, fc2, fc3, fc4 = st.columns(4, gap="medium")

features = [
    (
        "🔍",
        "Early Failure Detection",
        "Identify abnormal machine behaviour hours or days before a physical breakdown, enabling targeted preventive action.",
    ),
    (
        "🧠",
        "AI Prediction",
        "A trained ML classification model processes multi-sensor streams to deliver instant failure-type predictions with high accuracy.",
    ),
    (
        "🔧",
        "Maintenance Recommendation",
        "Automatically generate prioritised maintenance actions based on the predicted failure mode and current machine health score.",
    ),
    (
        "📡",
        "Industrial Sensor Monitoring",
        "Continuously ingest temperature, vibration, torque, RPM, and pressure readings from connected industrial equipment.",
    ),
]

for col, (icon, title, desc) in zip([fc1, fc2, fc3, fc4], features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Welcome / How It Works Section ───────────────────────────
st.markdown(
    '<p class="section-heading">How It Works</p>',
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    st.markdown(
        """
        <div class="info-card">
            <h3>⚙️ Four Steps to Smarter Maintenance</h3>
            <p>
                1. <strong>Collect</strong> — Ingest sensor readings (temperature, vibration,
                pressure, RPM, torque, and more) from connected machinery.<br><br>
                2. <strong>Analyse</strong> — Feed readings into a trained ML classification
                model that identifies abnormal operating patterns.<br><br>
                3. <strong>Predict</strong> — Receive an instant risk assessment and
                failure-type classification for each machine.<br><br>
                4. <strong>Act</strong> — Use the generated maintenance recommendations to
                schedule targeted repairs before failures cascade.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            <h3>🚨 Detectable Failure Types</h3>
            <p>
                • Heat Dissipation Failure<br>
                • Power Failure<br>
                • Overstrain Failure<br>
                • Tool Wear Failure<br>
                • Random / Unknown Failures
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div class="info-card">
            <h3>✅ Key Benefits</h3>
            <p>
                🔧 <strong>Reduce downtime</strong> by up to 50 % with early fault
                detection.<br><br>
                💰 <strong>Cut maintenance costs</strong> by replacing reactive repairs
                with planned interventions.<br><br>
                📈 <strong>Increase OEE</strong> — Overall Equipment Effectiveness —
                across your production lines.<br><br>
                🛡️ <strong>Improve safety</strong> by flagging high-risk equipment states
                before they endanger personnel.<br><br>
                📊 <strong>Data-driven decisions</strong> backed by explainable AI
                insights, not gut feel.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Call-to-Action — Start Prediction ────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

cta_col, _ = st.columns([2, 3])
with cta_col:
    st.markdown(
        """
        <div class="cta-card">
            <h3>🚀 Ready to Run a Prediction?</h3>
            <p>
                Enter your machine's current sensor readings and let MachineGuardAI
                assess its health status in real time. No hardware integration required
                for manual entry mode.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Primary action button — prediction logic unchanged
    if st.button("🚀 Predict Machine Health", use_container_width=True):
        st.switch_page("pages/Predict.py")

# ── Footer ────────────────────────────────────────────────────
st.markdown(
    """
    <div class="footer">
        MachineGuardAI &nbsp;·&nbsp; AI-Powered Predictive Maintenance &nbsp;·&nbsp;
        Built with Streamlit &nbsp;|&nbsp; © 2025
    </div>
    """,
    unsafe_allow_html=True,
)
