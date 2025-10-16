from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text
import models
from helper import column_exists
from database import get_db
from sqlalchemy import desc, asc
from sqlalchemy import func

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
from sqlalchemy import desc, asc

# GET: lista las ventas ordenadas por fecha (más recientes primero)
@router.get("/ventas/ordenadas")
def get_ventas_ordenadas(db: Session = Depends(get_db), orden: str = "desc"):
    """
    Lista todas las ventas ordenadas por fecha.
    Parámetro opcional:
      - orden=desc → más recientes primero (por defecto)
      - orden=asc  → más antiguas primero
    """
    try:
        if orden.lower() == "asc":
            resultados = db.query(models.Venta).order_by(asc(models.Venta.fecha_venta)).all()
        else:
            resultados = db.query(models.Venta).order_by(desc(models.Venta.fecha_venta)).all()

        if not resultados:
            raise HTTPException(status_code=404, detail="No hay ventas registradas.")

        return [
            {
                "id_venta": v.id_venta,
                "rut_cliente": v.rut_cliente,
                "id_empleado": v.id_empleado,
                "fecha_venta": v.fecha_venta,
                "total_venta": v.total_venta,
                "metodo_de_pago": v.metodo_de_pago
            }
            for v in resultados
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ordenar las ventas: {e}")



@router.get("/ventas/por-fecha")
def get_ventas_por_fecha(fecha: str, db: Session = Depends(get_db)):
    """
    Devuelve todas las ventas que coinciden exactamente con la fecha indicada (tipo string).
    Además incluye la suma total de las ventas de ese día (sin repetirla en cada registro).
    Ejemplo: /ventas/por-fecha?fecha=2025-10-16
    """
    try:
        # Buscar las ventas por coincidencia exacta de texto
        ventas = db.query(models.Venta).filter(models.Venta.fecha_venta == fecha).all()

        if not ventas:
            raise HTTPException(status_code=404, detail=f"No se encontraron ventas para la fecha {fecha}.")

        # Calcular la suma total de ese día
        total_dia = (
            db.query(func.sum(models.Venta.total_venta))
            .filter(models.Venta.fecha_venta == fecha)
            .scalar()
        )

        # Formatear respuesta (sin total_dia dentro de cada venta)
        reporte = [
            {
                "id_venta": v.id_venta,
                "rut_cliente": v.rut_cliente,
                "id_empleado": v.id_empleado,
                "fecha_venta": v.fecha_venta,
                "total_venta": v.total_venta,
                "metodo_de_pago": v.metodo_de_pago
            }
            for v in ventas
        ]

        return {
            "message": f"Ventas del {fecha}",
            "total_dia": total_dia,
            "ventas": reporte
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ventas por fecha: {e}")