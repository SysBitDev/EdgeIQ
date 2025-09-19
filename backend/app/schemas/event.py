from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class EventIn(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=64)
    agent_id: str = Field(min_length=1, max_length=128)
    metric: str = Field(min_length=1, max_length=64)
    value: float
    ts: int


class EventOut(EventIn):
    id: int


class CountOut(BaseModel):
    count: int


class HealthOut(BaseModel):
    ok: Literal[True]


class EventsPage(BaseModel):
    items: List[EventOut]
    total: int
    next_offset: Optional[int] = None
