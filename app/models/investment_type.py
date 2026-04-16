from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class InvestmentType(Base):
    __tablename__ = "investment_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)           # ej. "Depósito a Plazo Fijo"
    min_term_days = Column(Integer, nullable=False, default=30)
    max_term_days = Column(Integer, nullable=False, default=720)
    annual_rate = Column(Float, nullable=False)          # tasa anual en %
    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)
    payment_mode = Column(String(50), nullable=False, default="al_vencimiento")  # "al_vencimiento" | "mensual"
    is_active = Column(Boolean, default=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)

    institution = relationship("Institution")
    simulations = relationship("InvestmentSimulation", back_populates="investment_type")
    applications = relationship("InvestmentApplication", back_populates="investment_type")
