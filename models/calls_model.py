from app.config.database import Base
from app.models.base_model import Advisor, Client
from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class ProcessInitiated(Base):
    __tablename__ = "processes_initiated"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    started = Column(Boolean, default=False)


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    advisor_id = Column(Integer, ForeignKey("advisors.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    advisor = relationship("Advisor", back_populates="calls")
    client = relationship("Client", back_populates="calls")
    ssid = Column(String, nullable=False)
    status = Column(String, nullable=True)