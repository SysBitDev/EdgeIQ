from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...schemas.event import EventIn
from ...models.event import Event
from ...db import SessionLocal, Base, engine

router = APIRouter(tags=["events"])

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/events")
def create_events(items: List[EventIn], db: Session = Depends(get_db)):
    evs = [Event(**i.model_dump()) for i in items]
    db.add_all(evs)
    db.commit()
    return {"stored": len(evs)}


@router.get("/events/count")
def count_events(db: Session = Depends(get_db)):
    return {"count": db.query(Event).count()}
