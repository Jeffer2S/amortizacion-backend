from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.credit_type import CreditType
from app.models.amortization import AmortizationSchedule
from app.schemas.amortization import AmortizationRequest, AmortizationResponse, AmortizationRow
from app.services.amortization import (
    calcular_tabla_francesa, calcular_tabla_alemana
)
from app.services.auth import get_current_user
from app.models.user import User
from app.models.institution import Institution
from app.utils.pdf_generator import generar_pdf_amortizacion

router = APIRouter(prefix="/api/amortization", tags=["amortization"])


def _build_response(
    ct: CreditType,
    data: AmortizationRequest,
    tabla: List[dict],
    schedule_id: int = None,
) -> AmortizationResponse:
    total_capital = round(sum(r["capital"] for r in tabla), 2)
    total_interest = round(sum(r["interest"] for r in tabla), 2)

    charge_names = list(tabla[0]["indirect_charges"].keys()) if tabla else []
    total_charges_details = {
        name: round(sum(r["indirect_charges"].get(name, 0.0) for r in tabla), 2)
        for name in charge_names
    }
    total_charges = round(sum(sum(r["indirect_charges"].values()) for r in tabla), 2)
    total_payment = round(sum(r["total_payment"] for r in tabla), 2)

    return AmortizationResponse(
        credit_type_name=ct.name,
        system=data.system,
        amount=data.amount,
        term_months=data.term_months,
        nominal_rate=ct.nominal_rate,
        monthly_rate=round(ct.nominal_rate / 12, 6),
        schedule=[AmortizationRow(**r) for r in tabla],
        charge_names=charge_names,
        total_capital=total_capital,
        total_interest=total_interest,
        total_charges=total_charges,
        total_charges_details=total_charges_details,
        total_payment=total_payment,
        schedule_id=schedule_id,
    )


@router.post("/calculate", response_model=AmortizationResponse)
def calculate_amortization(
    data: AmortizationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ct = db.query(CreditType).filter(CreditType.id == data.credit_type_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Tipo de crédito no encontrado")

    if data.system == "frances":
        tabla = calcular_tabla_francesa(data.amount, ct.nominal_rate, data.term_months, list(ct.indirect_charges))
    elif data.system == "aleman":
        tabla = calcular_tabla_alemana(data.amount, ct.nominal_rate, data.term_months, list(ct.indirect_charges))
    else:
        raise HTTPException(status_code=400, detail="Sistema inválido. Use 'frances' o 'aleman'")

    total_capital = round(sum(r["capital"] for r in tabla), 2)
    total_interest = round(sum(r["interest"] for r in tabla), 2)
    total_charges = round(sum(sum(r["indirect_charges"].values()) for r in tabla), 2)
    total_payment = round(sum(r["total_payment"] for r in tabla), 2)

    # Persistir en BD
    schedule = AmortizationSchedule(
        user_id=current_user.id,
        credit_type_id=ct.id,
        amount=data.amount,
        term_months=data.term_months,
        nominal_rate=ct.nominal_rate,
        system=data.system,
        schedule_data=tabla,
        total_interest=total_interest,
        total_charges=total_charges,
        total_payment=total_payment,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return _build_response(ct, data, tabla, schedule.id)


@router.post("/calculate/preview", response_model=AmortizationResponse)
def preview_amortization(
    data: AmortizationRequest,
    db: Session = Depends(get_db),
):
    """Cálculo sin autenticación ni persistencia — para vista previa pública."""
    ct = db.query(CreditType).filter(CreditType.id == data.credit_type_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Tipo de crédito no encontrado")

    if data.system == "frances":
        tabla = calcular_tabla_francesa(data.amount, ct.nominal_rate, data.term_months, list(ct.indirect_charges))
    elif data.system == "aleman":
        tabla = calcular_tabla_alemana(data.amount, ct.nominal_rate, data.term_months, list(ct.indirect_charges))
    else:
        raise HTTPException(status_code=400, detail="Sistema inválido. Use 'frances' o 'aleman'")

    return _build_response(ct, data, tabla)


@router.post("/pdf/{schedule_id}")
def download_pdf(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Genera y devuelve el PDF de una tabla de amortización guardada."""
    schedule = db.query(AmortizationSchedule).filter(
        AmortizationSchedule.id == schedule_id,
        AmortizationSchedule.user_id == current_user.id,
    ).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Tabla no encontrada")

    ct = schedule.credit_type
    institution = db.query(Institution).first()

    pdf_bytes = generar_pdf_amortizacion(
        schedule=schedule.schedule_data,
        institution_name=institution.name if institution else "Institución Financiera",
        institution_logo=institution.logo_path if institution else None,
        credit_type_name=ct.name,
        amount=schedule.amount,
        term_months=schedule.term_months,
        nominal_rate=schedule.nominal_rate,
        system=schedule.system,
        client_name=current_user.name,
        total_capital=schedule.amount,
        total_interest=schedule.total_interest,
        charge_names=list(schedule.schedule_data[0]["indirect_charges"].keys()) if schedule.schedule_data and type(schedule.schedule_data[0].get("indirect_charges")) is dict else [],
        total_charges_details={name: round(sum(r["indirect_charges"].get(name, 0.0) for r in schedule.schedule_data), 2) for name in (list(schedule.schedule_data[0]["indirect_charges"].keys()) if schedule.schedule_data and type(schedule.schedule_data[0].get("indirect_charges")) is dict else [])},
        total_payment=schedule.total_payment,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=amortizacion_{schedule_id}.pdf"},
    )


@router.get("/history", response_model=List[AmortizationResponse])
def my_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = db.query(AmortizationSchedule).filter(
        AmortizationSchedule.user_id == current_user.id
    ).order_by(AmortizationSchedule.created_at.desc()).limit(20).all()

    results = []
    for s in records:
        ct = s.credit_type
        req = AmortizationRequest(
            credit_type_id=ct.id, amount=s.amount,
            term_months=s.term_months, system=s.system
        )
        results.append(_build_response(ct, req, s.schedule_data, s.id))
    return results
