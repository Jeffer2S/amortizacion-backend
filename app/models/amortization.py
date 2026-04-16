from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AmortizationSchedule(Base):
    __tablename__ = "amortization_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    credit_type_id = Column(Integer, ForeignKey("credit_types.id"), nullable=False)
    amount = Column(Float, nullable=False)           # monto del préstamo
    term_months = Column(Integer, nullable=False)    # plazo en meses
    nominal_rate = Column(Float, nullable=False)     # tasa nominal anual en % al momento del cálculo
    system = Column(String(20), nullable=False)      # "frances" | "aleman"
    schedule_data = Column(JSON, nullable=False)     # tabla de pagos serializada
    total_interest = Column(Float, nullable=False)
    total_charges = Column(Float, nullable=False)
    total_payment = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="amortization_schedules")
    credit_type = relationship("CreditType", back_populates="amortization_schedules")
