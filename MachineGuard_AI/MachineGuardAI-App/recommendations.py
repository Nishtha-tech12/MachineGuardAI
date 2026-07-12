# ============================================================
# MachineGuardAI — Maintenance Recommendation Engine
# ============================================================
# Provides structured, actionable maintenance guidance for
# every Failure Type the model can predict.
#
# Usage:
#   from recommendations import get_recommendation
#   rec = get_recommendation("Heat Dissipation Failure")
#   # rec["severity"]      → "High"
#   # rec["actions"]       → list[str]
#   # rec["urgency"]       → "Immediate"
#   # rec["description"]   → str
# ============================================================

from __future__ import annotations

# ── Recommendation Catalogue ─────────────────────────────────
# Keys must exactly match the Failure Type strings produced by
# the trained model (see models/predictive_model.joblib).
_RECOMMENDATIONS: dict[str, dict] = {

    "No Failure": {
        "severity": "None",
        "urgency": "Routine",
        "icon": "✅",
        "description": (
            "The machine is operating within normal parameters. "
            "No immediate intervention is required."
        ),
        "actions": [
            "Continue scheduled preventive maintenance intervals.",
            "Log current sensor readings as a healthy baseline.",
            "Verify lubrication levels are within specification.",
            "Confirm next planned maintenance date is on record.",
        ],
    },

    "Heat Dissipation Failure": {
        "severity": "High",
        "urgency": "Immediate",
        "icon": "🌡️",
        "description": (
            "The temperature differential between air and process temperature "
            "has dropped critically low while the machine is running at high speed, "
            "indicating the cooling system is not dissipating heat effectively. "
            "Continued operation risks thermal runaway and permanent component damage."
        ),
        "actions": [
            "STOP machine immediately if air-to-process temperature delta is below 8.6 K.",
            "Inspect and clean all cooling fans, heat sinks, and ventilation ducts.",
            "Check coolant level, flow rate, and coolant pump for blockages or leaks.",
            "Verify thermal paste and heat-exchanger contact on critical components.",
            "Inspect ambient temperature — relocate machine if environment is too hot.",
            "Run a controlled test cycle after servicing; monitor temperature delta closely.",
        ],
    },

    "Power Failure": {
        "severity": "High",
        "urgency": "Immediate",
        "icon": "⚡",
        "description": (
            "Detected abnormal combination of torque and rotational speed indicating "
            "electrical power delivery to the drive system is unstable or insufficient. "
            "This can damage motors, drives, and connected mechanical components."
        ),
        "actions": [
            "Shut down the machine safely and lock out / tag out (LOTO) before inspection.",
            "Inspect motor windings for signs of overheating, burning, or insulation breakdown.",
            "Test supply voltage and current draw against the motor nameplate ratings.",
            "Check Variable Frequency Drive (VFD) or motor controller fault logs.",
            "Inspect all power cables, connectors, and fuses for damage or loose terminations.",
            "Measure torque-speed characteristic under no-load and compare to baseline.",
            "Replace motor or drive unit if electrical fault is confirmed.",
        ],
    },

    "Overstrain Failure": {
        "severity": "Critical",
        "urgency": "Stop Operation",
        "icon": "🔩",
        "description": (
            "The product of tool wear and torque exceeds the mechanical strain threshold "
            "for the current machine variant. Continued operation will cause mechanical "
            "fracture, spindle seizure, or structural damage to the machine frame."
        ),
        "actions": [
            "STOP the machine immediately — do not continue the current operation.",
            "Reduce feed rate and cutting depth before resuming any test runs.",
            "Replace the current tool insert or cutting head; inspect for micro-fractures.",
            "Review and reduce scheduled torque/load for this machine variant (L/M/H rating).",
            "Inspect spindle bearings, chuck, and drive shaft for deformation.",
            "Perform a full mechanical inspection of the gearbox and coupling.",
            "Update machining program with corrected load parameters before restart.",
        ],
    },

    "Tool Wear Failure": {
        "severity": "Medium",
        "urgency": "Scheduled - Within 24 hours",
        "icon": "🔧",
        "description": (
            "Cumulative tool wear has reached a level where cutting performance degrades, "
            "dimensional accuracy drops, and surface finish quality deteriorates. "
            "Left unaddressed, this leads to scrap parts and possible tool breakage."
        ),
        "actions": [
            "Replace the cutting tool, insert, or drill bit at the next opportunity.",
            "Inspect the tool holder and collet for wear or runout.",
            "Review tool life management records — adjust replacement interval if needed.",
            "Check machined part dimensions against tolerance spec to identify scrap.",
            "Inspect the spindle for vibration signatures indicating chatter from a worn tool.",
            "Update the tool wear counter in the machine's CNC control or CMMS.",
        ],
    },

    "Random Failures": {
        "severity": "Medium",
        "urgency": "Investigate Within 4 Hours",
        "icon": "⚠️",
        "description": (
            "An anomalous operating condition has been detected that does not match "
            "a specific known failure pattern. This may indicate a sensor fault, an "
            "intermittent electrical issue, or an emerging fault in an early stage."
        ),
        "actions": [
            "Review all sensor readings for outliers or implausible values.",
            "Check sensor calibration dates — recalibrate any sensor past its interval.",
            "Inspect wiring harness and sensor connectors for loose contacts or corrosion.",
            "Review the machine's recent maintenance and fault history log.",
            "Monitor the machine for 15–30 minutes under normal load; log any recurrence.",
            "Escalate to a maintenance engineer if the anomaly recurs within the shift.",
        ],
    },
}

# ── Public API ────────────────────────────────────────────────

def get_recommendation(failure_type: str) -> dict:
    """
    Return a structured maintenance recommendation dict for the given
    failure type string.

    Parameters
    ----------
    failure_type : str
        The failure type label as returned by the trained model, e.g.:
        "No Failure", "Heat Dissipation Failure", "Power Failure",
        "Overstrain Failure", "Tool Wear Failure", "Random Failures".

    Returns
    -------
    dict with keys:
        severity    : str  — "None" | "Medium" | "High" | "Critical"
        urgency     : str  — plain-English time-to-act label
        icon        : str  — single emoji for UI display
        description : str  — human-readable explanation of the failure mode
        actions     : list[str] — ordered maintenance action steps

    If the failure_type is unrecognised, a safe fallback is returned
    rather than raising an exception.
    """
    normalised = failure_type.strip()
    if normalised in _RECOMMENDATIONS:
        return _RECOMMENDATIONS[normalised]

    # Unknown / future class — return a safe fallback
    return {
        "severity": "Unknown",
        "urgency": "Investigate Immediately",
        "icon": "❓",
        "description": (
            f"Unrecognised failure type: {failure_type!r}. "
            "The model may have returned an unexpected label. "
            "Contact your maintenance engineer for manual inspection."
        ),
        "actions": [
            "Perform a full manual inspection of the machine.",
            "Check model version — retrain if the dataset has new failure categories.",
        ],
    }


def list_failure_types() -> list[str]:
    """Return all failure type keys the recommendation engine knows about."""
    return list(_RECOMMENDATIONS.keys())
