import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.institution import Institution
from app.schemas.institution import InstitutionCreate, InstitutionUpdate, InstitutionOut
from app.services.auth import get_current_user, require_admin
from app.config import settings

router = APIRouter(prefix="/api/institution", tags=["institution"])


@router.get("/", response_model=InstitutionOut)
def get_institution(db: Session = Depends(get_db)):
    """Retorna la configuración de la institución (primer registro)."""
    institution = db.query(Institution).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Institución no configurada")
    return institution


@router.post("/", response_model=InstitutionOut, status_code=201)
def create_institution(data: InstitutionCreate, db: Session = Depends(get_db),
                       _=Depends(require_admin)):
    institution = Institution(**data.model_dump())
    db.add(institution)
    db.commit()
    db.refresh(institution)
    return institution


@router.put("/", response_model=InstitutionOut)
def update_institution(data: InstitutionUpdate, db: Session = Depends(get_db),
                       _=Depends(require_admin)):
    institution = db.query(Institution).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Institución no configurada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(institution, key, value)
    db.commit()
    db.refresh(institution)
    return institution


@router.post("/logo", response_model=InstitutionOut)
async def upload_logo(file: UploadFile = File(...), db: Session = Depends(get_db),
                      _=Depends(require_admin)):
    institution = db.query(Institution).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Institución no configurada")

    upload_dir = os.path.join(settings.upload_dir, "logos")
    os.makedirs(upload_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".svg"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no soportado")

    logo_path = os.path.join(upload_dir, f"institution_logo{ext}")
    content = await file.read()
    with open(logo_path, "wb") as f:
        f.write(content)

    institution.logo_path = logo_path
    db.commit()
    db.refresh(institution)
    return institution
