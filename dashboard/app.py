import os, requests, streamlit as st, pandas as pd
API_BASE = os.getenv("API_BASE", "http://localhost:8080")
API_KEY = os.getenv("API_KEY", "dev-key")

st.title("Carrier Inbound – Metrics Dashboard")

def api_get(path):
    r = requests.get(f"{API_BASE}{path}", headers={"X-API-Key": API_KEY}, timeout=10)
    r.raise_for_status()
    return r.json()

col1, col2, col3 = st.columns(3)
m = api_get("/metrics")
col1.metric("Total Calls", m.get("total_calls", 0))
col2.metric("Booked", m.get("booked", 0))
col3.metric("Booked Rate", f"{(m.get('booked_rate',0)*100):.1f}%")

st.subheader("Outcome Breakdown")
out_df = pd.DataFrame([(k,v) for k,v in (m.get("outcomes") or {}).items()], columns=["outcome","count"])
st.bar_chart(out_df.set_index("outcome"))

st.subheader("Sentiment Breakdown")
sent_df = pd.DataFrame([(k,v) for k,v in (m.get("sentiments") or {}).items()], columns=["sentiment","count"])
st.bar_chart(sent_df.set_index("sentiment"))

st.subheader("Recent Calls")
calls = api_get("/calls")["calls"]
if calls:
    df = pd.DataFrame(calls)
    st.dataframe(df)
else:
    st.info("No calls logged yet. Trigger a web call in HappyRobot to populate data.")
