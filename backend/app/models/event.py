from sqlalchemy import BigInteger, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    agent_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    metric: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
