import os, requests
from .models import VerifyCarrierResponse

FMCSA_BASE = os.getenv("FMCSA_BASE", "https://example-fmcsa-api")
FMCSA_API_KEY = os.getenv("FMCSA_API_KEY", "YOUR_KEY_HERE")

def verify_mc(mc: str) -> VerifyCarrierResponse:
    # Mock if no real key set
    if not FMCSA_API_KEY or FMCSA_API_KEY == "YOUR_KEY_HERE":
        eligible = mc.strip().isdigit() and len(mc.strip()) in (6,7)
        return VerifyCarrierResponse(eligible=eligible, mc=mc, carrier_name="Demo Carrier" if eligible else None, safety_rating="Satisfactory" if eligible else None)

    try:
        url = f"{FMCSA_BASE}/carriers/{mc}"
        headers = {"Authorization": f"Bearer {FMCSA_API_KEY}"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        eligible = bool(data.get("eligible", False))
        return VerifyCarrierResponse(
            eligible=eligible,
            mc=mc,
            carrier_name=data.get("name"),
            safety_rating=data.get("safety_rating"),
            details=data
        )
    except Exception as e:
        return VerifyCarrierResponse(eligible=False, mc=mc, details={"error": str(e)})
