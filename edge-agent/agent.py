import hashlib
import hmac
import json
import os
import time
import uuid

import psutil
import requests

API = os.getenv("API_URL", "http://localhost:8000/api/v1/events")
TENANT = os.getenv("TENANT", "demo")
AGENT_ID = os.getenv("AGENT_ID", str(uuid.uuid4()))
SECRET = os.getenv("SECRET", "dev-secret")
BATCH = 10
INTERVAL = 5


def sign(payload: bytes) -> str:
    return hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()


buf = []
while True:
    point = {
        "tenant_id": TENANT,
        "agent_id": AGENT_ID,
        "metric": "cpu",
        "value": psutil.cpu_percent(),
        "ts": int(time.time()),
    }
    buf.append(point)
    if len(buf) >= BATCH:
        data = json.dumps(buf).encode()
        try:
            r = requests.post(
                API,
                data=data,
                headers={"Content-Type": "application/json", "X-Signature": sign(data)},
                timeout=5,
            )
            print("sent:", r.status_code, r.text)
        except Exception as e:
            print("send error:", e)
        buf.clear()
    time.sleep(INTERVAL)
