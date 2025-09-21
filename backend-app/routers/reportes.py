from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

# Grupo de rutas para Reportes.
router = APIRouter(prefix="/reportes", tags=["Reportes"])

# SELECT simple: listar todos los reportes
@router.get("/")
def get_reportes(db: Session = Depends(get_db)):
    return db.query(models.Reporte).all()