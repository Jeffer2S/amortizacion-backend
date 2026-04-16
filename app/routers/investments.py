import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.investment_type import InvestmentType
from app.models.investment import InvestmentSimulation, InvestmentApplication, KYCDocument
from app.schemas.investment import (
    InvestmentTypeCreate, InvestmentTypeUpdate, InvestmentTypeOut,
    InvestmentSimulateRequest, InvestmentSimulateResponse,
    InvestmentApplicationCreate, InvestmentApplicationOut, KYCDocumentOut
)
from app.services.investment import calcular_inversion, calcular_tabla_comparativa
from app.services.auth import get_current_user, require_admin
from app.models.user import User
from app.models.institution import Institution
from app.config import settings
from app.utils.pdf_generator import generar_pdf_inversion

router = APIRouter(prefix="/api/investments", tags=["investments"])


# ──────── Investment Types (Admin) ────────

@router.get("/types", response_model=List[InvestmentTypeOut])
def list_investment_types(db: Session = Depends(get_db)):
    return db.query(InvestmentType).filter(InvestmentType.is_active == True).all()


@router.post("/types", response_model=InvestmentTypeOut, status_code=201)
def create_investment_type(data: InvestmentTypeCreate, db: Session = Depends(get_db),
                           _=Depends(require_admin)):
    it = InvestmentType(**data.model_dump())
    db.add(it)
    db.commit()
    db.refresh(it)
    return it


@router.put("/types/{type_id}", response_model=InvestmentTypeOut)
def update_investment_type(type_id: int, data: InvestmentTypeUpdate,
                           db: Session = Depends(get_db), _=Depends(require_admin)):
    it = db.query(InvestmentType).filter(InvestmentType.id == type_id).first()
    if not it:
        raise HTTPException(status_code=404, detail="Tipo de inversión no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(it, key, value)
    db.commit()
    db.refresh(it)
    return it


@router.delete("/types/{type_id}", status_code=204)
def delete_investment_type(type_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    it = db.query(InvestmentType).filter(InvestmentType.id == type_id).first()
    if not it:
        raise HTTPException(status_code=404, detail="Tipo de inversión no encontrado")
    it.is_active = False
    db.commit()


# ──────── Simulation (Client) ────────

@router.post("/simulate", response_model=InvestmentSimulateResponse)
def simulate_investment(
    data: InvestmentSimulateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    it = db.query(InvestmentType).filter(InvestmentType.id == data.investment_type_id).first()
    if not it:
        raise HTTPException(status_code=404, detail="Tipo de inversión no encontrado")

    result = calcular_inversion(data.amount, it.annual_rate, data.term_days)

    sim = InvestmentSimulation(
        user_id=current_user.id,
        investment_type_id=it.id,
        amount=data.amount,
        term_days=data.term_days,
        annual_rate=it.annual_rate,
        gross_interest=result["gross_interest"],
        ir_retention=result["ir_retention"],
        net_interest=result["net_interest"],
        total_at_maturity=result["total_at_maturity"],
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)

    return InvestmentSimulateResponse(
        investment_type_name=it.name,
        amount=data.amount,
        term_days=data.term_days,
        annual_rate=it.annual_rate,
        gross_interest=result["gross_interest"],
        ir_retention=result["ir_retention"],
        net_interest=result["net_interest"],
        total_at_maturity=result["total_at_maturity"],
        simulation_id=sim.id,
    )


@router.post("/simulate/preview", response_model=InvestmentSimulateResponse)
def preview_investment(data: InvestmentSimulateRequest, db: Session = Depends(get_db)):
    """Vista previa sin auth."""
    it = db.query(InvestmentType).filter(InvestmentType.id == data.investment_type_id).first()
    if not it:
        raise HTTPException(status_code=404, detail="Tipo de inversión no encontrado")
    result = calcular_inversion(data.amount, it.annual_rate, data.term_days)
    return InvestmentSimulateResponse(investment_type_name=it.name, **result)


@router.get("/simulate/comparative/{type_id}")
def comparative_table(type_id: int, amount: float, db: Session = Depends(get_db)):
    it = db.query(InvestmentType).filter(InvestmentType.id == type_id).first()
    if not it:
        raise HTTPException(status_code=404, detail="Tipo de inversión no encontrado")
    return calcular_tabla_comparativa(amount, it.annual_rate)


# ──────── Online Application (Client) ────────

@router.post("/apply", response_model=InvestmentApplicationOut, status_code=201)
def create_application(
    data: InvestmentApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    it = db.query(InvestmentType).filter(InvestmentType.id == data.investment_type_id).first()
    if not it:
        raise HTTPException(status_code=404, detail="Tipo de inversión no encontrado")

    app = InvestmentApplication(
        user_id=current_user.id,
        investment_type_id=data.investment_type_id,
        amount=data.amount,
        term_days=data.term_days,
        personal_data=data.personal_data,
        status="pendiente",
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.get("/applications", response_model=List[InvestmentApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(InvestmentApplication).filter(
        InvestmentApplication.user_id == current_user.id
    ).order_by(InvestmentApplication.created_at.desc()).all()


@router.get("/applications/all", response_model=List[InvestmentApplicationOut])
def all_applications(db: Session = Depends(get_db), _=Depends(require_admin)):
    return db.query(InvestmentApplication).order_by(
        InvestmentApplication.created_at.desc()
    ).all()


@router.put("/applications/{app_id}/status")
def update_application_status(
    app_id: int, status: str, db: Session = Depends(get_db), _=Depends(require_admin)
):
    app = db.query(InvestmentApplication).filter(InvestmentApplication.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    app.status = status
    db.commit()
    return {"message": "Estado actualizado"}


# ──────── Document Upload ────────

@router.post("/applications/{app_id}/documents", response_model=KYCDocumentOut, status_code=201)
async def upload_document(
    app_id: int,
    doc_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = db.query(InvestmentApplication).filter(
        InvestmentApplication.id == app_id,
        InvestmentApplication.user_id == current_user.id,
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    upload_dir = os.path.join(settings.upload_dir, "kyc", str(app_id))
    os.makedirs(upload_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1].lower()
    safe_name = f"{doc_type}{ext}"
    file_path = os.path.join(upload_dir, safe_name)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Si ya existe un doc del mismo tipo, actualiza
    existing = db.query(KYCDocument).filter(
        KYCDocument.application_id == app_id,
        KYCDocument.doc_type == doc_type,
    ).first()
    if existing:
        existing.file_path = file_path
        existing.original_filename = file.filename
        db.commit()
        db.refresh(existing)
        return existing

    doc = KYCDocument(
        application_id=app_id,
        doc_type=doc_type,
        file_path=file_path,
        original_filename=file.filename,
    )
    db.add(doc)

    # Si todos los docs están subidos, actualizar estado
    docs = db.query(KYCDocument).filter(KYCDocument.application_id == app_id).all()
    if len(docs) >= 3:
        app.status = "documentos_enviados"
    db.commit()
    db.refresh(doc)
    return doc


@router.post("/applications/{app_id}/biometric")
async def save_biometric(
    app_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Guarda la selfie de validación biométrica y actualiza el estado."""
    app = db.query(InvestmentApplication).filter(
        InvestmentApplication.id == app_id,
        InvestmentApplication.user_id == current_user.id,
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    upload_dir = os.path.join(settings.upload_dir, "kyc", str(app_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, "selfie.jpg")

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Registrar como KYC doc
    existing = db.query(KYCDocument).filter(
        KYCDocument.application_id == app_id,
        KYCDocument.doc_type == "selfie",
    ).first()
    if not existing:
        doc = KYCDocument(application_id=app_id, doc_type="selfie",
                          file_path=file_path, original_filename="selfie.jpg")
        db.add(doc)

    app.biometric_status = "verificado"
    app.status = "biometria_verificada"
    db.commit()

    return {"message": "Validación biométrica completada", "status": "verificado"}


# ──────── PDF ────────

@router.post("/simulate/pdf/{sim_id}")
def download_investment_pdf(
    sim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sim = db.query(InvestmentSimulation).filter(
        InvestmentSimulation.id == sim_id,
        InvestmentSimulation.user_id == current_user.id,
    ).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")

    institution = db.query(Institution).first()
    it = sim.investment_type

    pdf_bytes = generar_pdf_inversion(
        institution_name=institution.name if institution else "Institución Financiera",
        institution_logo=institution.logo_path if institution else None,
        investment_type_name=it.name,
        client_name=current_user.name,
        amount=sim.amount,
        term_days=sim.term_days,
        annual_rate=sim.annual_rate,
        gross_interest=sim.gross_interest,
        ir_retention=sim.ir_retention,
        net_interest=sim.net_interest,
        total_at_maturity=sim.total_at_maturity,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=inversion_{sim_id}.pdf"},
    )
