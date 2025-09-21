from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

# Grupo de rutas para Proveedores
router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

# SELECT simple: lista todos los proveedores
@router.get("/")
def get_proveedores(db: Session = Depends(get_db)):
    return db.query(models.Proveedor).all()