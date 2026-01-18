from fastapi import FastAPI
from app.schemas import TransactionRequest
from app.rules_engine import rule_score
from app.ml_model import ml_score
import redis

app = FastAPI()

r = redis.Redis(host="redis", port=6379)

@app.get("/")
def home():
    return {"message": "SentinelStream Running"}

@app.post("/transaction")
def process(tx: TransactionRequest):
    user = tx.user_id
    device = tx.device_id

    # Rule-based risk
    rule = rule_score(tx.amount)

    # Device-based risk
    if device.startswith("X"):
        device_risk = 0.7
    else:
        device_risk = 0.2

    # ML-based risk
    ml = ml_score(tx.amount)

    # Final risk
    risk = (rule + ml + device_risk) / 3

    # Decision
    if risk > 0.8:
        status = "DECLINED"
    elif risk > 0.5:
        status = "FLAGGED"
    else:
        status = "APPROVED"

    return {
        "user_id": user,
        "device_id": device,
        "amount": tx.amount,
        "risk": round(risk, 2),
        "status": status
    }
