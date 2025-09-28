from pydantic import BaseModel, field_validator
from typing import Optional, List, Literal, Dict


class VerifyCarrierResponse(BaseModel):
    eligible: bool
    mc: str
    carrier_name: Optional[str] = None
    safety_rating: Optional[str] = None
    details: Optional[Dict] = None


class Load(BaseModel):
    load_id: str
    origin: str
    destination: str
    pickup_datetime: str
    delivery_datetime: str
    equipment_type: str
    loadboard_rate: float
    notes: str
    weight: int
    commodity_type: str
    num_of_pieces: int
    miles: int
    dimensions: str


class NegotiateRequest(BaseModel):
    loadboard_rate: float
    offer: float
    rounds_done: int = 0

    @field_validator("loadboard_rate", "offer", mode="before")
    def cast_to_float(cls, v):
        try:
            return float(v)
        except Exception:
            raise ValueError("loadboard_rate and offer must be numeric")

    @field_validator("rounds_done", mode="before")
    def cast_to_int(cls, v):
        try:
            return int(v)
        except Exception:
            raise ValueError("rounds_done must be an integer")


class NegotiateResponse(BaseModel):
    decision: Literal["accept", "counter", "reject"]
    price: float


class CallLog(BaseModel):
    call_id: Optional[str] = None
    carrier: Optional[str] = None
    mc: Optional[str] = None
    load_id: Optional[str] = None
    offer_chain: List[float] = []
    final_price: Optional[float] = None
    outcome: Literal["booked", "rejected", "ineligible", "no_loads", "abandoned"]
    sentiment: Literal["positive", "neutral", "negative"] = "neutral"
    created_at: Optional[str] = None

    @field_validator("offer_chain", mode="before")
    def cast_offer_chain(cls, v):
        if isinstance(v, list):
            try:
                return [float(x) for x in v]
            except Exception:
                raise ValueError("offer_chain values must be numeric")
        return v
