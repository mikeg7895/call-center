from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..config.database import Base

class Advisor(Base):
    __tablename__ = "advisors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    in_call = Column(Boolean, default=False)
    position_queue = Column(Integer, nullable=True)

    calls = relationship("Call", back_populates="advisor")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    document = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    reason = Column(String, nullable=False)

    calls = relationship("Call", back_populates="client")