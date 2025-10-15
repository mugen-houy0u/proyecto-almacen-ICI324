from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text
import models
from helper import column_exists
from database import get_db

# Grupo de rutas de "Ventas"
router = APIRouter(prefix="/ventas", tags=["Ventas"])

# SELECT simple: lista todas las ventas
@router.get("/")
def get_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()

# SELECT con JOIN (Venta ⟂ Empleado) + filtro por rol=cajero
@router.get("/ventas/cajeros")
def get_ventas_cajeros(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Venta.id_venta,
            models.Venta.fecha_venta,
            models.Venta.total_venta,
            models.Empleado.nombre.label("cajero")
        )
        .join(models.Empleado, models.Venta.id_empleado == models.Empleado.id_empleado)
        .filter(models.Empleado.rol == "cajero")
        .all()
    )
    return [
        {"id_venta": r.id_venta, "fecha_venta": r.fecha_venta, "total_venta": r.total_venta, "cajero": r.cajero}
        for r in resultados
    ]

# SELECT con JOIN múltiple (Empleado ⟂ Venta ⟂ Cliente)
@router.get("/ventas/detalle")
def ventas_detalle(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Empleado.nombre.label("empleado"),
            models.Venta.id_venta,
            models.Cliente.nombre_completo.label("cliente")
        )
        .join(models.Venta, models.Empleado.id_empleado == models.Venta.id_empleado)
        .join(models.Cliente, models.Venta.rut_cliente == models.Cliente.rut_cliente)
        .all()
    )
    return [
        {"empleado": r.empleado, "id_venta": r.id_venta, "cliente": r.cliente}
        for r in resultados
    ]

# SELECT con JOIN (Venta ⟂ Cliente ⟂ Empleado)
@router.get("/ventas-clientes-empleados")
def get_ventas_clientes_empleados(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Venta.id_venta,
            models.Cliente.nombre_completo.label("cliente"),
            models.Empleado.nombre.label("empleado"),
            models.Venta.total_venta
        )
        .join(models.Cliente, models.Venta.rut_cliente == models.Cliente.rut_cliente)
        .join(models.Empleado, models.Venta.id_empleado == models.Empleado.id_empleado)
        .all()
    )
    return [
        {"id_venta": r.id_venta, "cliente": r.cliente, "empleado": r.empleado, "total_venta": r.total_venta}
        for r in resultados
    ]

# INSERT: crea una venta (usa el ORM)
@router.post("/ventas")
def create_venta(
    rut_cliente: str, total_venta: int, id_empleado: int,
    fecha_venta: str, metodo_de_pago: str, db: Session = Depends(get_db)
):
    nueva_venta = models.Venta(
        id_empleado=id_empleado,
        rut_cliente=rut_cliente,
        total_venta=total_venta,
        fecha_venta=fecha_venta,
        metodo_de_pago=metodo_de_pago,
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return {"message": "Venta creada correctamente", "venta": nueva_venta}

# DELETE: elimina una venta y sus reportes asociados (limpieza manual)
@router.delete("/ventas/{id_venta}")
def delete_venta(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id_venta == id_venta).first()
    if not venta:
        return {"error": "Venta no encontrada"}
    
    # Borrado explícito de los reportes de esa venta
    reportes = db.query(models.Reporte).filter(models.Reporte.id_venta == id_venta).all()
    for reporte in reportes:
        db.delete(reporte)

    db.delete(venta)
    db.commit()
    return {"message": f"Venta con ID {id_venta} y sus reportes asociados eliminados correctamente"}

# ALTER: agrega columna 'descuento' a Venta si no existe
@router.post("/alter/venta-descuento")
def alter_add_descuento_venta(db: Session = Depends(get_db)):
    if not column_exists(db, "Venta", "descuento"):
        db.execute(sql_text("ALTER TABLE Venta ADD COLUMN descuento INTEGER DEFAULT 0"))
        db.commit()
        return {"message": "Columna 'descuento' agregada a Venta"}
    return {"message": "La columna ya existe"}
