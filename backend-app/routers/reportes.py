from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db
from sqlalchemy import func, desc


# Grupo de rutas para Reportes.
router = APIRouter(prefix="/reportes", tags=["Reportes"])

# SELECT simple: listar todos los reportes
@router.get("/")
def get_reportes(db: Session = Depends(get_db)):
    return db.query(models.Reporte).all()

# ==========================================================
# POST /reportes
# Crea y almacena un nuevo reporte general
# ==========================================================
@router.post(
    "/",
    summary="Generar y guardar un nuevo reporte general",
    response_description="Reporte creado correctamente",
    status_code=status.HTTP_201_CREATED,
)
def crear_reporte(
    id_venta: int,
    fecha_inicio: str,
    fecha_final: str,
    tipo_reporte: str,
    total_ventas: int,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo registro de reporte en la base de datos.

    ### Parámetros:
    - **id_venta (int)**: ID de la venta asociada.
    - **fecha_inicio (str)**: Fecha inicial del rango del reporte.
    - **fecha_final (str)**: Fecha final del rango del reporte.
    - **tipo_reporte (str)**: Tipo de reporte generado (por ejemplo, 'ventas', 'compras').
    - **total_ventas (int)**: Total de ventas dentro del rango.

    ### Retorna:
    - **201 Created**: Si el reporte se crea correctamente.
    - **400 Bad Request**: Si faltan datos requeridos.
    - **500 Internal Server Error**: Si ocurre un error durante la creación.
    """
    try:
        if not all([id_venta, fecha_inicio, fecha_final, tipo_reporte, total_ventas]):
            raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

        nuevo_reporte = models.Reporte(
            id_venta=id_venta,
            fecha_inicio=fecha_inicio,
            fecha_final=fecha_final,
            tipo_reporte=tipo_reporte,
            total_ventas=total_ventas,
        )

        db.add(nuevo_reporte)
        db.commit()
        db.refresh(nuevo_reporte)

        return {"msg": "Reporte creado correctamente", "reporte": nuevo_reporte}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el reporte: {e}")
    
