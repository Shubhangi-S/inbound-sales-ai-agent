from .models import NegotiateRequest, NegotiateResponse

def negotiate(req: NegotiateRequest) -> NegotiateResponse:
    lb = float(req.loadboard_rate)
    offer = float(req.offer)
    rounds = int(req.rounds_done)

    if offer >= 0.90 * lb:
        return NegotiateResponse(decision="accept", price=offer)

    if rounds < 3:
        target = max(0.92 * lb, (offer + 0.95 * lb) / 2.0)
        return NegotiateResponse(decision="counter", price=round(target, 2))

    return NegotiateResponse(decision="reject", price=offer)
