from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

# Grupo de rutas para Lotes
router = APIRouter(prefix="/lotes", tags=["Lotes"])

# SELECT simple: lista todos los registros de la tabla Lote
@router.get("/")
def get_lotes(db: Session = Depends(get_db)):
    return db.query(models.Lote).all()