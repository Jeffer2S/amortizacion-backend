from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class CreditType(Base):
    __tablename__ = "credit_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)  # consumo, hipotecario, educacion, microcredito, productivo
    nominal_rate = Column(Float, nullable=False)     # tasa nominal anual en %
    max_term_months = Column(Integer, nullable=True)
    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)

    institution = relationship("Institution")
    indirect_charges = relationship("IndirectCharge", back_populates="credit_type", cascade="all, delete-orphan")
    amortization_schedules = relationship("AmortizationSchedule", back_populates="credit_type")
