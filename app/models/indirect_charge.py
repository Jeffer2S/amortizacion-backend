from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class IndirectCharge(Base):
    __tablename__ = "indirect_charges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    # Tipos: seguro_desgravamen, aporte_solca, comision_administrativa, donacion, otro
    charge_type = Column(String(100), nullable=False, default="otro")
    value = Column(Float, nullable=False)            # valor numérico
    is_percentage = Column(Boolean, default=True)    # True=% del monto, False=valor fijo USD
    is_monthly = Column(Boolean, default=True)       # True=cobra cada mes, False=una sola vez
    is_active = Column(Boolean, default=True)
    credit_type_id = Column(Integer, ForeignKey("credit_types.id"), nullable=False)

    credit_type = relationship("CreditType", back_populates="indirect_charges")
