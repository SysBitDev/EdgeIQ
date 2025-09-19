from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...db import get_db
from ...models.event import Event
from ...schemas.event import CountOut, EventIn, EventOut, EventsPage
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


@router.get("/events/list", response_model=EventsPage)
def list_events(
    db: Session = Depends(get_db),
    metric: Optional[str] = None,
    tenant_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    limit: int = Query(5000, ge=1, le=20000),
    offset: int = Query(0, ge=0),
):
    # base query
    stmt = select(Event)
    if metric:
        stmt = stmt.where(Event.metric == metric)
    if tenant_id:
        stmt = stmt.where(Event.tenant_id == tenant_id)
    if agent_id:
        stmt = stmt.where(Event.agent_id == agent_id)
    if from_ts is not None:
        stmt = stmt.where(Event.ts >= from_ts)
    if to_ts is not None:
        stmt = stmt.where(Event.ts <= to_ts)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0

    # page
    rows = db.execute(stmt.order_by(Event.ts.asc()).offset(offset).limit(limit)).scalars().all()

    items = [
        EventOut(
            id=r.id,
            tenant_id=r.tenant_id,
            agent_id=r.agent_id,
            metric=r.metric,
            value=r.value,
            ts=r.ts,
        )
        for r in rows
    ]

    next_offset = offset + len(items) if (offset + len(items)) < total else None
    return EventsPage(items=items, total=total, next_offset=next_offset)
