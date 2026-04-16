from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime


class AmortizationRequest(BaseModel):
    credit_type_id: int
    amount: float
    term_months: int
    system: str = "frances"   # "frances" | "aleman"


class AmortizationRow(BaseModel):
    period: int
    initial_balance: float
    capital: float
    interest: float
    indirect_charges: dict[str, float]
    total_payment: float
    final_balance: float


class AmortizationResponse(BaseModel):
    credit_type_name: str
    system: str
    amount: float
    term_months: int
    nominal_rate: float
    monthly_rate: float
    schedule: List[AmortizationRow]
    charge_names: List[str]
    total_capital: float
    total_interest: float
    total_charges: float
    total_charges_details: dict[str, float]
    total_payment: float
    schedule_id: Optional[int] = None
