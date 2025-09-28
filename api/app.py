import os, datetime
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from .models import NegotiateRequest, CallLog
from .fmcsaclient import verify_mc
from .loads import search_loads
from .negotiate import negotiate
from . import storage

API_KEY = os.getenv("API_KEY", "dev-key")

app = FastAPI(title="HappyRobot Carrier Inbound API", version="0.1.0")

@app.on_event("startup")
def startup():
    storage.init_db()

def auth(x_api_key: Optional[str]):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/verify-carrier")
def verify_carrier(mc: str, x_api_key: Optional[str] = Header(None)):
    auth(x_api_key)
    res = verify_mc(mc)
    return JSONResponse(res.dict())

@app.get("/loads")
def loads(origin: Optional[str] = None,
          destination: Optional[str] = None,
          equipment_type: Optional[str] = None,
          limit: int = Query(3, ge=1, le=20),
          x_api_key: Optional[str] = Header(None)):
    auth(x_api_key)
    res = search_loads(origin, destination, equipment_type, limit)
    return {"results": [r.dict() for r in res]}

@app.post("/negotiate")
def negotiate_endpoint(req: NegotiateRequest, x_api_key: Optional[str] = Header(None)):
    auth(x_api_key)
    res = negotiate(req)
    return res

@app.post("/log-call")
def log_call_endpoint(payload: CallLog, x_api_key: Optional[str] = Header(None)):
    auth(x_api_key)
    data = payload.dict()
    if not data.get("created_at"):
        data["created_at"] = datetime.datetime.utcnow().isoformat()
    storage.log_call(data)
    return {"ok": True}

@app.get("/metrics")
def metrics(x_api_key: Optional[str] = Header(None)):
    auth(x_api_key)
    return storage.metrics()

@app.get("/calls")
def calls(limit:int=50, x_api_key: Optional[str] = Header(None)):
    auth(x_api_key)
    return {"calls": storage.list_calls(limit)}
