from api.ibm_predict import predict_failure
import streamlit as st
st.set_page_config(
    page_title="MachineGuardAI | Predict",
    page_icon="🤖",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>

[data-testid="stToolbar"]{
    display:none;
}

.block-container{
    padding-top:2rem;
}

.main-card{
    background:white;
    border-radius:18px;
    padding:30px;
    box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.predict-btn button{
    background:#1E40AF !important;
    color:white !important;
    border:none;
    border-radius:12px;
    height:55px;
    font-size:18px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

st.title("🔍 Predict Machine Health")
st.write(
    "Enter the machine parameters below to predict equipment failures using MachineGuardAI."
)

st.markdown("<div class='main-card'>", unsafe_allow_html=True)

product_id = st.text_input("Product ID", placeholder="L47181")

col1, col2 = st.columns(2)

with col1:
    air_temp = st.number_input(
        "Air Temperature [K]",
        value=298.0,
        format="%.2f"
    )

    rotational_speed = st.number_input(
        "Rotational Speed [rpm]",
        value=1500
    )

    tool_wear = st.number_input(
        "Tool Wear [min]",
        value=100
    )

with col2:
    process_temp = st.number_input(
        "Process Temperature [K]",
        value=308.0,
        format="%.2f"
    )

    torque = st.number_input(
        "Torque [Nm]",
        value=40.0,
        format="%.2f"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='predict-btn'>", unsafe_allow_html=True)

predict = st.button("🔍 Predict Failure", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if predict:

    with st.spinner("Analyzing machine data..."):

        try:

            result = predict_failure(
                product_id,
                air_temp,
                process_temp,
                rotational_speed,
                torque,
                tool_wear,
            )

            # ── Unpack structured result ──────────────────────────────
            prediction     = result["prediction"]
            confidence     = result["confidence"]
            source         = result["source"]
            rec            = result["recommendation"]
            severity       = rec["severity"]
            urgency        = rec["urgency"]
            icon           = rec["icon"]
            description    = rec["description"]
            actions        = rec["actions"]

            st.markdown("---")

            # ── Source badge ──────────────────────────────────────────
            if source == "IBM Watsonx AI":
                st.markdown(
                    "<span style='background:#1E40AF;color:white;padding:4px 14px;"
                    "border-radius:20px;font-size:0.82rem;font-weight:600;'>"
                    "&#x2601;&#xFE0F; IBM Watsonx AI</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<span style='background:#374151;color:#e5e7eb;padding:4px 14px;"
                    "border-radius:20px;font-size:0.82rem;font-weight:600;'>"
                    "&#x1F4BB; Local Random Forest Fallback</span>",
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Prediction result box ─────────────────────────────────
            if severity == "None":
                st.success(f"{icon}  **{prediction}**  —  Machine is operating normally.")
            elif severity == "Medium":
                st.warning(f"{icon}  **{prediction}**")
            else:
                # High or Critical
                st.error(f"{icon}  **{prediction}**")

            # ── Confidence bar ────────────────────────────────────────
            st.markdown(f"**Confidence:** {confidence:.1f}%")
            st.progress(int(confidence))

            st.markdown("---")

            # ── Recommendation panel ──────────────────────────────────
            st.markdown("### Maintenance Recommendation")

            sev_colours = {
                "None":     "#16a34a",
                "Medium":   "#d97706",
                "High":     "#dc2626",
                "Critical": "#7c3aed",
                "Unknown":  "#6b7280",
            }
            sev_colour = sev_colours.get(severity, "#6b7280")

            st.markdown(
                f"<div style='border-left:4px solid {sev_colour};"
                f"padding:14px 18px;background:#f9fafb;"
                f"border-radius:0 8px 8px 0;margin-bottom:12px;'>"
                f"<strong style='color:{sev_colour};'>Severity: {severity}</strong>"
                f"&nbsp;&nbsp;|&nbsp;&nbsp;"
                f"<strong>Urgency:</strong> {urgency}"
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(f"_{description}_")

            st.markdown("**Recommended Actions:**")
            for i, action in enumerate(actions, start=1):
                st.markdown(f"{i}. {action}")

        except Exception as e:

            st.error(f"Prediction failed: {e}")
