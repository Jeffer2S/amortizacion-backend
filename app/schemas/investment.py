from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ──────── InvestmentType ────────
class InvestmentTypeBase(BaseModel):
    name: str
    min_term_days: int = 30
    max_term_days: int = 720
    annual_rate: float
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    payment_mode: str = "al_vencimiento"
    is_active: bool = True
    institution_id: Optional[int] = None


class InvestmentTypeCreate(InvestmentTypeBase):
    pass


class InvestmentTypeUpdate(InvestmentTypeBase):
    pass


class InvestmentTypeOut(InvestmentTypeBase):
    id: int

    class Config:
        from_attributes = True


# ──────── Simulation ────────
class InvestmentSimulateRequest(BaseModel):
    investment_type_id: int
    amount: float
    term_days: int


class InvestmentSimulateResponse(BaseModel):
    investment_type_name: str
    amount: float
    term_days: float
    annual_rate: float
    gross_interest: float
    ir_retention: float
    net_interest: float
    total_at_maturity: float
    simulation_id: Optional[int] = None


# ──────── Application ────────
class InvestmentApplicationCreate(BaseModel):
    investment_type_id: int
    amount: float
    term_days: int
    personal_data: Optional[dict] = None


class InvestmentApplicationOut(BaseModel):
    id: int
    investment_type_id: int
    amount: float
    term_days: int
    status: str
    biometric_status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KYCDocumentOut(BaseModel):
    id: int
    application_id: int
    doc_type: str
    file_path: str
    original_filename: Optional[str] = None

    class Config:
        from_attributes = True
