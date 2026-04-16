from pydantic import BaseModel
from typing import Optional, List


# ──────── CreditType ────────
class IndirectChargeBase(BaseModel):
    name: str
    charge_type: str = "otro"
    value: float
    is_percentage: bool = True
    is_monthly: bool = True
    is_active: bool = True


class IndirectChargeCreate(IndirectChargeBase):
    credit_type_id: int


class IndirectChargeUpdate(IndirectChargeBase):
    pass


class IndirectChargeOut(IndirectChargeBase):
    id: int
    credit_type_id: int

    class Config:
        from_attributes = True


# ──────── CreditType ────────
class CreditTypeBase(BaseModel):
    name: str
    category: str
    nominal_rate: float
    max_term_months: Optional[int] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    is_active: bool = True
    institution_id: Optional[int] = None


class CreditTypeCreate(CreditTypeBase):
    pass


class CreditTypeUpdate(CreditTypeBase):
    pass


class CreditTypeOut(CreditTypeBase):
    id: int
    indirect_charges: List[IndirectChargeOut] = []

    class Config:
        from_attributes = True
