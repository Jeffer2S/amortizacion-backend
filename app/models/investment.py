from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class InvestmentSimulation(Base):
    __tablename__ = "investment_simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    investment_type_id = Column(Integer, ForeignKey("investment_types.id"), nullable=False)
    amount = Column(Float, nullable=False)
    term_days = Column(Integer, nullable=False)
    annual_rate = Column(Float, nullable=False)          # tasa al momento del cálculo
    gross_interest = Column(Float, nullable=False)
    ir_retention = Column(Float, nullable=False)        # retención impuesto a la renta
    net_interest = Column(Float, nullable=False)
    total_at_maturity = Column(Float, nullable=False)   # capital + interés neto
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="investment_simulations")
    investment_type = relationship("InvestmentType", back_populates="simulations")


class InvestmentApplication(Base):
    __tablename__ = "investment_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    investment_type_id = Column(Integer, ForeignKey("investment_types.id"), nullable=False)
    amount = Column(Float, nullable=False)
    term_days = Column(Integer, nullable=False)
    # Estado: pendiente | documentos_enviados | biometria_verificada | aprobado | rechazado
    status = Column(String(50), nullable=False, default="pendiente")
    biometric_status = Column(String(30), nullable=False, default="pendiente")  # pendiente | verificado
    personal_data = Column(JSON, nullable=True)         # datos adicionales del formulario
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="investment_applications")
    investment_type = relationship("InvestmentType", back_populates="applications")
    documents = relationship("KYCDocument", back_populates="application", cascade="all, delete-orphan")


class KYCDocument(Base):
    __tablename__ = "kyc_documents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("investment_applications.id"), nullable=False)
    doc_type = Column(String(100), nullable=False)  # cedula_frontal, cedula_posterior, papeleta, planilla, selfie
    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("InvestmentApplication", back_populates="documents")
