from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="client")  # "admin" | "client"
    is_active = Column(Boolean, default=True)
    cedula = Column(String(20), nullable=True)
    phone = Column(String(50), nullable=True)

    amortization_schedules = relationship("AmortizationSchedule", back_populates="user")
    investment_simulations = relationship("InvestmentSimulation", back_populates="user")
    investment_applications = relationship("InvestmentApplication", back_populates="user")
