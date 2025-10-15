from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text
import models
from helper import column_exists
from database import get_db

# Grupo de rutas de Clientes
router = APIRouter(prefix="/clientes", tags=["CLientes"])

# SELECT simple: listar todos los clientes
@router.get("/")
def get_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()

# SELECT con JOIN (Cliente ⟂ Venta): compras por cliente

@router.get("/clientes/compras")
def clientes_compras(db: Session = Depends(get_db)):
    resultados = (
        db.query(models.Cliente.nombre_completo, models.Venta.id_venta, models.Venta.total_venta)
        .join(models.Venta, models.Cliente.rut_cliente == models.Venta.rut_cliente)
        .all()
    )
    return [
        {"cliente": r.nombre_completo, "id_venta": r.id_venta, "total_venta": r.total_venta}
        for r in resultados
    ]

# SELECT con JOIN (Cliente ⟂ Venta): métodos de pago por cliente
@router.get("/clientes/metodo-pago")
def clientes_metodo_pago(db: Session = Depends(get_db)):
    resultados = (
        db.query(models.Cliente.nombre_completo, models.Venta.metodo_de_pago)
        .join(models.Venta, models.Cliente.rut_cliente == models.Venta.rut_cliente)
        .all()
    )
    return [{"cliente": r.nombre_completo, "metodo_pago": r.metodo_de_pago} for r in resultados]

# ALTER: agrega columna puntos_fidelidad a Cliente (si no existe)
@router.post("/alter/cliente-puntos")
def alter_add_puntos_cliente(db: Session = Depends(get_db)):
    if not column_exists(db, "Cliente", "puntos_fidelidad"):
        db.execute(sql_text("ALTER TABLE Cliente ADD COLUMN puntos_fidelidad INTEGER DEFAULT 0"))
        db.commit()
        return {"message": "Columna 'puntos_fidelidad' agregada a Cliente"}
    return {"message": "La columna ya existe"}
