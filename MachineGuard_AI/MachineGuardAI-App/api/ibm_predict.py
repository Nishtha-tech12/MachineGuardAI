import os
import time
import requests
import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# ── Load .env (no-op if variables are already in the environment) ─────
load_dotenv()

# ── Validated environment variable loader ─────────────────────────────
def _require_env(name: str) -> str:
    """
    Return a stripped env var value or raise EnvironmentError with a
    clear, actionable message — never silently pass None or empty string.
    """
    raw = os.getenv(name)

    if raw is None:
        raise EnvironmentError(
            f"[MachineGuardAI] '{name}' is not set.\n"
            f"  -> Add '{name}=<value>' to your .env file and restart the app."
        )

    value = raw.strip()

    if not value:
        raise EnvironmentError(
            f"[MachineGuardAI] '{name}' is set but empty after stripping whitespace.\n"
            f"  -> Check your .env file for a missing value on the '{name}=' line."
        )

    # Catch the common mistake of leaving the placeholder text in place
    if value.startswith("<") and value.endswith(">"):
        raise EnvironmentError(
            f"[MachineGuardAI] '{name}' still contains a placeholder value: {value!r}\n"
            f"  -> Replace it with your actual value in .env."
        )

    return value


# ── Module-level config ───────────────────────────────────────────────
# IBM credentials are optional: if missing, every call silently uses the
# local model.  A missing .env is not a crash — it is a fallback trigger.
_IBM_API_KEY  = os.getenv("IBM_API_KEY",  "").strip()
_IBM_ENDPOINT = os.getenv("IBM_ENDPOINT", "").strip()
_IBM_IAM_URL  = os.getenv(
    "IBM_IAM_URL",
    "https://iam.cloud.ibm.com/identity/token"
).strip()

# True only when both credentials are present AND the endpoint is public
_IBM_CONFIGURED = bool(
    _IBM_API_KEY
    and _IBM_ENDPOINT
    and not _IBM_ENDPOINT.startswith("<")
    and "private." not in _IBM_ENDPOINT
)

# ── In-process IAM token cache ────────────────────────────────────────
# IBM IAM tokens are valid for 3600 s.  We pre-refresh 5 min before expiry
# so the token is always fresh without a round-trip on every prediction call.
_TOKEN_CACHE: dict = {"token": None, "expires_at": 0.0}
_REFRESH_BUFFER_SECS = 300

# ── Local model artefacts (lazy-loaded on first fallback use) ─────────
_BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODEL_PATH = os.path.join(_BASE_DIR, "models", "predictive_model.joblib")
_ENC_PATH   = os.path.join(_BASE_DIR, "models", "label_encoder.joblib")
_local_model   = None
_local_encoder = None

# HTTP status codes that are IBM quota / service errors — fall back silently
_FALLBACK_HTTP_CODES = {402, 405, 429, 500, 502, 503, 504}


# ── Internal helpers ──────────────────────────────────────────────────

def get_access_token() -> str:
    """
    Return a valid IBM IAM bearer token, using the in-process cache.

    Raises RuntimeError with an actionable message on auth failure,
    including the IBM error body so the cause is immediately visible.
    """
    now = time.time()

    # Return cached token if still fresh
    if _TOKEN_CACHE["token"] and now < _TOKEN_CACHE["expires_at"] - _REFRESH_BUFFER_SECS:
        return _TOKEN_CACHE["token"]

    # Fetch a new token
    try:
        response = requests.post(
            _IBM_IAM_URL,
            data={
                "apikey": _IBM_API_KEY,
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code
        body   = exc.response.text

        hint = ""
        if status == 400:
            hint = (
                "\n  Possible causes:"
                "\n    1. IBM_API_KEY is wrong, expired, or was deleted."
                "\n    2. IBM_API_KEY has invisible whitespace — re-copy carefully."
                f"\n    3. IBM_IAM_URL is wrong (currently: {_IBM_IAM_URL!r})."
            )
        elif status == 401:
            hint = "\n  The API key was rejected — it may have been revoked."

        raise RuntimeError(
            f"[MachineGuardAI] IBM IAM authentication failed with HTTP {status}.{hint}"
            f"\n  IBM response body: {body}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"[MachineGuardAI] Could not reach IBM IAM endpoint ({_IBM_IAM_URL!r}): {exc}"
        ) from exc

    data = response.json()
    _TOKEN_CACHE["token"]      = data["access_token"]
    _TOKEN_CACHE["expires_at"] = now + data.get("expires_in", 3600)

    return _TOKEN_CACHE["token"]


def _load_local_model():
    """Lazy-load the local joblib artefacts (once per process)."""
    global _local_model, _local_encoder

    if _local_model is None:
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(
                f"[MachineGuardAI] Local model not found at {_MODEL_PATH}.\n"
                "  Run train_local_model.py first to generate it."
            )
        if not os.path.exists(_ENC_PATH):
            raise FileNotFoundError(
                f"[MachineGuardAI] Label encoder not found at {_ENC_PATH}.\n"
                "  Run train_local_model.py first to generate it."
            )
        _local_model   = joblib.load(_MODEL_PATH)
        _local_encoder = joblib.load(_ENC_PATH)


def _predict_local(
    product_id: str,
    air_temp: float,
    process_temp: float,
    rotational_speed: int,
    torque: float,
    tool_wear: int,
) -> tuple[str, float]:
    """
    Run inference against the local Random Forest.

    Returns
    -------
    (failure_type, confidence_pct)
        failure_type   : str   — e.g. "Heat Dissipation Failure"
        confidence_pct : float — 0.0 to 100.0
    """
    _load_local_model()

    # Encode Product ID prefix the same way train_local_model.py did
    prefix = str(product_id).strip()[0].upper() if product_id else "L"
    try:
        prefix_enc = int(_local_encoder.transform([prefix])[0])
    except ValueError:
        # Unknown prefix — default to the most common class index
        prefix_enc = int(_local_encoder.transform([_local_encoder.classes_[0]])[0])

    X = pd.DataFrame([[
        prefix_enc,
        float(air_temp),
        float(process_temp),
        int(rotational_speed),
        float(torque),
        int(tool_wear),
    ]], columns=[
        "Product_Prefix_Enc",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
    ])

    failure_type   = str(_local_model.predict(X)[0])
    proba_row      = _local_model.predict_proba(X)[0]
    confidence_pct = float(np.max(proba_row) * 100)

    return failure_type, confidence_pct


def _predict_ibm(
    product_id: str,
    air_temp: float,
    process_temp: float,
    rotational_speed: int,
    torque: float,
    tool_wear: int,
) -> tuple[str, float]:
    """
    Send a single-row scoring request to IBM Watson ML.

    Returns
    -------
    (failure_type, confidence_pct)

    Raises
    ------
    _IBMFallbackError  — on quota / service errors that should trigger fallback
    RuntimeError       — on hard auth errors that should surface to the user
    """
    token = get_access_token()

    payload = {
        "input_data": [
            {
                "fields": [
                    "Product ID",
                    "Air temperature [K]",
                    "Process temperature [K]",
                    "Rotational speed [rpm]",
                    "Torque [Nm]",
                    "Tool wear [min]",
                ],
                "values": [[
                    str(product_id),
                    float(air_temp),
                    float(process_temp),
                    int(rotational_speed),
                    float(torque),
                    int(tool_wear),
                ]],
            }
        ]
    }

    try:
        response = requests.post(
            _IBM_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as exc:
        if exc.response.status_code in _FALLBACK_HTTP_CODES:
            raise _IBMFallbackError(exc.response.status_code) from exc
        # Hard error (e.g. 401 bad token) — let it surface
        raise RuntimeError(
            f"[MachineGuardAI] Watson ML prediction failed with HTTP "
            f"{exc.response.status_code}.\n"
            f"  IBM response body: {exc.response.text}"
        ) from exc

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
        raise _IBMFallbackError("network") from exc

    # Parse IBM response — shape: predictions[0].values[0] = [label, [probs...]]
    data   = response.json()
    values = data["predictions"][0]["values"][0]   # [label, [p0, p1, ...]]
    failure_type   = str(values[0])
    confidence_pct = float(max(values[1]) * 100)

    return failure_type, confidence_pct


class _IBMFallbackError(Exception):
    """Internal sentinel: IBM call failed with a recoverable error."""


# ── Public API ────────────────────────────────────────────────────────

def predict_failure(
    product_id: str,
    air_temp: float,
    process_temp: float,
    rotational_speed: int,
    torque: float,
    tool_wear: int,
) -> dict:
    """
    Predict machine failure type.

    Attempts IBM Watsonx AI Online Deployment first.
    Silently falls back to the local Random Forest on:
      - HTTP 402 (instance_quota_exceeded)
      - HTTP 405 (method not allowed)
      - HTTP 429 / 500 / 502 / 503 / 504 (service errors)
      - Request timeout (> 30 s)
      - Network / connection error
      - IBM credentials not configured in .env

    Parameters
    ----------
    product_id        : Machine product identifier, e.g. "L47181"
    air_temp          : Air temperature in Kelvin
    process_temp      : Process temperature in Kelvin
    rotational_speed  : Spindle speed in RPM
    torque            : Applied torque in Nm
    tool_wear         : Cumulative tool wear in minutes

    Returns
    -------
    dict:
        {
          "prediction":     str,    # e.g. "Heat Dissipation Failure"
          "confidence":     float,  # 0.0 – 100.0
          "source":         str,    # "IBM Watsonx AI" | "Local Random Forest Fallback"
          "recommendation": dict    # from recommendations.get_recommendation()
        }

    Raises
    ------
    RuntimeError  — only on hard, non-recoverable errors (bad API key, model
                    file missing, etc.) that the UI should surface to the user.
    """
    # Import here to avoid a circular import if recommendations ever imports
    # something from this module.
    from recommendations import get_recommendation

    failure_type: str
    confidence:   float
    source:       str

    # ── 1. Try IBM first ─────────────────────────────────────────────
    if _IBM_CONFIGURED:
        try:
            failure_type, confidence = _predict_ibm(
                product_id, air_temp, process_temp,
                rotational_speed, torque, tool_wear,
            )
            source = "IBM Watsonx AI"
        except _IBMFallbackError:
            # Quota exhausted, service down, timeout — fall through silently
            failure_type, confidence = _predict_local(
                product_id, air_temp, process_temp,
                rotational_speed, torque, tool_wear,
            )
            source = "Local Random Forest Fallback"
    else:
        # ── 2. No IBM credentials — go straight to local model ───────
        failure_type, confidence = _predict_local(
            product_id, air_temp, process_temp,
            rotational_speed, torque, tool_wear,
        )
        source = "Local Random Forest Fallback"

    return {
        "prediction":     failure_type,
        "confidence":     round(confidence, 2),
        "source":         source,
        "recommendation": get_recommendation(failure_type),
    }
