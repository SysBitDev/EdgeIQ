from sqlalchemy import BigInteger, Column, Integer, String, Float
from ..db import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(64), index=True, nullable=False)
    agent_id = Column(String(128), index=True, nullable=False)
    metric = Column(String(64), index=True, nullable=False)
    value = Column(Float, nullable=False)
    ts = Column(BigInteger, index=True, nullable=False)
