from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...db import get_db
from ...models.event import Event
from ...schemas.event import CountOut, EventIn
from .ws import broadcast_event

router = APIRouter(prefix="/api/v1", tags=["events"])


@router.get("/events/count", response_model=CountOut)
def events_count(db: Session = Depends(get_db)):
    cnt = db.scalar(select(func.count()).select_from(Event)) or 0
    return CountOut(count=cnt)


@router.post("/events", status_code=204)
def ingest_events(
    payload: List[EventIn],
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not payload:
        raise HTTPException(status_code=400, detail="empty payload")

    objects = [Event(**e.model_dump()) for e in payload]
    db.add_all(objects)
    db.commit()

    for obj in objects:
        background.add_task(
            broadcast_event,
            {
                "type": "event",
                "tenant_id": obj.tenant_id,
                "agent_id": obj.agent_id,
                "metric": obj.metric,
                "value": obj.value,
                "ts": obj.ts,
                "id": obj.id,
            },
        )
    return
