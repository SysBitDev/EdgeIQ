from pydantic import BaseModel, Field


class EventIn(BaseModel):
    tenant_id: str
    agent_id: str
    metric: str
    value: float
    ts: int = Field(..., description="unix ts")


class EventOut(EventIn):
    id: int
