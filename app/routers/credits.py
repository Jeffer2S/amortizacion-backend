from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.credit_type import CreditType
from app.models.indirect_charge import IndirectCharge
from app.schemas.credit import (
    CreditTypeCreate, CreditTypeUpdate, CreditTypeOut,
    IndirectChargeCreate, IndirectChargeUpdate, IndirectChargeOut
)
from app.services.auth import require_admin, get_current_user

router = APIRouter(prefix="/api/credits", tags=["credits"])


# ──────── Credit Types ────────

@router.get("/types", response_model=List[CreditTypeOut])
def list_credit_types(db: Session = Depends(get_db)):
    return db.query(CreditType).filter(CreditType.is_active == True).all()


@router.get("/types/{credit_type_id}", response_model=CreditTypeOut)
def get_credit_type(credit_type_id: int, db: Session = Depends(get_db)):
    ct = db.query(CreditType).filter(CreditType.id == credit_type_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Tipo de crédito no encontrado")
    return ct


@router.post("/types", response_model=CreditTypeOut, status_code=201)
def create_credit_type(data: CreditTypeCreate, db: Session = Depends(get_db),
                       _=Depends(require_admin)):
    ct = CreditType(**data.model_dump())
    db.add(ct)
    db.commit()
    db.refresh(ct)
    return ct


@router.put("/types/{credit_type_id}", response_model=CreditTypeOut)
def update_credit_type(credit_type_id: int, data: CreditTypeUpdate,
                       db: Session = Depends(get_db), _=Depends(require_admin)):
    ct = db.query(CreditType).filter(CreditType.id == credit_type_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Tipo de crédito no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ct, key, value)
    db.commit()
    db.refresh(ct)
    return ct


@router.delete("/types/{credit_type_id}", status_code=204)
def delete_credit_type(credit_type_id: int, db: Session = Depends(get_db),
                       _=Depends(require_admin)):
    ct = db.query(CreditType).filter(CreditType.id == credit_type_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Tipo de crédito no encontrado")
    ct.is_active = False
    db.commit()


# ──────── Indirect Charges ────────

@router.get("/charges", response_model=List[IndirectChargeOut])
def list_charges(credit_type_id: int = None, db: Session = Depends(get_db)):
    q = db.query(IndirectCharge).filter(IndirectCharge.is_active == True)
    if credit_type_id:
        q = q.filter(IndirectCharge.credit_type_id == credit_type_id)
    return q.all()


@router.post("/charges", response_model=IndirectChargeOut, status_code=201)
def create_charge(data: IndirectChargeCreate, db: Session = Depends(get_db),
                  _=Depends(require_admin)):
    # Verificar que el tipo de crédito existe
    ct = db.query(CreditType).filter(CreditType.id == data.credit_type_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Tipo de crédito no encontrado")
    charge = IndirectCharge(**data.model_dump())
    db.add(charge)
    db.commit()
    db.refresh(charge)
    return charge


@router.put("/charges/{charge_id}", response_model=IndirectChargeOut)
def update_charge(charge_id: int, data: IndirectChargeUpdate,
                  db: Session = Depends(get_db), _=Depends(require_admin)):
    charge = db.query(IndirectCharge).filter(IndirectCharge.id == charge_id).first()
    if not charge:
        raise HTTPException(status_code=404, detail="Cobro no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(charge, key, value)
    db.commit()
    db.refresh(charge)
    return charge


@router.delete("/charges/{charge_id}", status_code=204)
def delete_charge(charge_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    charge = db.query(IndirectCharge).filter(IndirectCharge.id == charge_id).first()
    if not charge:
        raise HTTPException(status_code=404, detail="Cobro no encontrado")
    charge.is_active = False
    db.commit()
