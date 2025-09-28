````markdown
# Inbound Sales AI Agent

This project is a demo of an **AI-powered voice agent** for inbound carrier sales in logistics.  
The agent can answer a carrier’s call, check their details, search available loads, negotiate prices, and record the outcome in a dashboard.

---

## What’s Inside
- **FastAPI backend** – carrier verification, load search, negotiation, call logging.  
- **Streamlit dashboard** – live dashboard showing key call stats.  
- **Dockerfile** – to run everything in a container.  
- **Ngrok support** – to expose the local API for external integrations.  

---

## Getting Started (Local)

### 1. Setup environment
You can use either **conda** or **venv**:  

```bash
# Conda
conda create -n inbound-agent python=3.11 -y
conda activate inbound-agent

# Or venv
python -m venv .venv
source .venv/bin/activate
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
export API_KEY=dev-key
export DB_PATH="$(pwd)/data/calls.db"
uvicorn api.app:app --reload --port 8080
```

Check it’s alive:

```bash
curl http://localhost:8080/health
```

---

## Example API Calls

```bash
# Verify carrier
curl -H "X-API-Key: dev-key" "http://localhost:8080/verify-carrier?mc=123456"

# Search loads
curl -H "X-API-Key: dev-key" "http://localhost:8080/loads?origin=Los%20Angeles&destination=Sacramento&equipment_type=Reefer"

# Negotiate
curl -H "X-API-Key: dev-key" -H "Content-Type: application/json" \
-d '{"loadboard_rate":1600,"offer":1300,"rounds_done":1}' \
http://localhost:8080/negotiate

# Log a call
curl -H "X-API-Key: dev-key" -H "Content-Type: application/json" \
-d '{
  "call_id": "demo-1",
  "carrier": "Demo Carrier",
  "mc": "123456",
  "load_id": "L-1003",
  "offer_chain": [1200, 1400, 1500],
  "final_price": 1500,
  "outcome": "booked",
  "sentiment": "positive"
}' \
http://localhost:8080/log-call
```

---

## Dashboard

```bash
export API_BASE=http://localhost:8080
export API_KEY=dev-key
streamlit run dashboard/app.py
```

The dashboard shows:

* Number of calls
* Booked percentage
* Outcomes (booked, rejected, no_loads, ineligible)
* Sentiment (positive, neutral, negative)

---

## Connect to a Workflow Platform

You can integrate this API with any workflow/voice platform (e.g. Twilio, SignalWire, or an AI agent orchestration tool).

Typical setup:

1. Start ngrok:

   ```bash
   ngrok http 8080
   ```

   Copy the HTTPS URL (e.g. `https://abcd1234.ngrok-free.app`).

2. In your platform, create an **Inbound Call workflow**.

3. Attach these tools (Webhooks) with your ngrok URL + header `X-API-Key: dev-key`:

   * `GET /verify-carrier?mc={mc}`
   * `GET /loads?...`
   * `POST /negotiate`
   * `POST /log-call`

4. Add a simple agent prompt:

   ```
   You are an inbound carrier sales agent.
   Ask for MC → Verify Carrier.
   If valid → ask for lane & equipment → Search Loads.
   Pitch a load and negotiate.
   Log outcome as booked or rejected.
   ```

---

## Run with Docker

```bash
docker build -t inbound-sales-ai-agent .
docker run -p 8080:8080 -e API_KEY=dev-key inbound-sales-ai-agent
```

---

## Next Steps

* Connect to the real FMCSA API (instead of the mock).
* Deploy the API to a cloud service like Render or Railway (so no ngrok needed).
* Store data in a production-ready database.
* Add authentication and monitoring for production use.

```