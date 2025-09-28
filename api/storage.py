import sqlite3, os, json, datetime
from typing import List, Dict, Any

DB_PATH = os.getenv("DB_PATH", "/app/data/calls.db")

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS calls ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "call_id TEXT,"
            "carrier TEXT,"
            "mc TEXT,"
            "load_id TEXT,"
            "offer_chain TEXT,"
            "final_price REAL,"
            "outcome TEXT,"
            "sentiment TEXT,"
            "created_at TEXT"
            ")"
        )
        c.commit()

def log_call(payload: Dict[str, Any]):
    with _conn() as c:
        c.execute(
            "INSERT INTO calls(call_id, carrier, mc, load_id, offer_chain, final_price, outcome, sentiment, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                payload.get("call_id"),
                payload.get("carrier"),
                payload.get("mc"),
                payload.get("load_id"),
                json.dumps(payload.get("offer_chain", [])),
                payload.get("final_price"),
                payload.get("outcome"),
                payload.get("sentiment", "neutral"),
                payload.get("created_at") or datetime.datetime.utcnow().isoformat()
            )
        )
        c.commit()

def metrics():
    with _conn() as c:
        cur = c.cursor()
        cur.execute("SELECT COUNT(*) FROM calls")
        total = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM calls WHERE outcome='booked'")
        booked = cur.fetchone()[0] or 0
        cur.execute("SELECT AVG(final_price) FROM calls WHERE final_price IS NOT NULL")
        avg_price = cur.fetchone()[0]
        cur.execute("SELECT outcome, COUNT(*) FROM calls GROUP BY outcome")
        outcome_breakdown = {row[0]: row[1] for row in cur.fetchall()}
        cur.execute("SELECT sentiment, COUNT(*) FROM calls GROUP BY sentiment")
        sentiment_breakdown = {row[0]: row[1] for row in cur.fetchall()}
        return {
            "total_calls": total,
            "booked": booked,
            "booked_rate": (booked / total) if total else 0.0,
            "avg_final_price": avg_price,
            "outcomes": outcome_breakdown,
            "sentiments": sentiment_breakdown
        }

def list_calls(limit:int=50):
    with _conn() as c:
        c.row_factory = sqlite3.Row
        cur = c.cursor()
        cur.execute("SELECT * FROM calls ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cur.fetchall()]
        return rows
