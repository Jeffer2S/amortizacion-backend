from pydantic import BaseModel
from typing import Optional


# ──────── Institution ────────
class InstitutionBase(BaseModel):
    name: str
    slogan: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    ruc: Optional[str] = None
    description: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(InstitutionBase):
    pass


class InstitutionOut(InstitutionBase):
    id: int
    logo_path: Optional[str] = None

    class Config:
        from_attributes = True
