from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import events, health, ws
from .settings import settings

app = FastAPI(title="EdgeIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(events.router)
app.include_router(ws.router)
