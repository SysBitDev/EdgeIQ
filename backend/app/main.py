from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api.v1 import health, events

app = FastAPI(title="EdgeIQ Ingest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
