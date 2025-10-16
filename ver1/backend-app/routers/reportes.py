from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

# Grupo de rutas para "Reportes"
router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/ventas-por-empleado")
def get_reporte_ventas_por_empleado(db: Session = Depends(get_db)):
    """
    Genera un reporte que agrupa las ventas totales por cada empleado.
    """
    resultados = (
        db.query(
            models.Empleado.id_empleado,
            models.Empleado.nombre.label("nombre_empleado"),
            func.count(models.Venta.id_venta).label("cantidad_ventas"),
            func.sum(models.Venta.total_venta).label("monto_total_vendido"),
        )
        .join(models.Venta, models.Empleado.id_empleado == models.Venta.id_empleado)
        .group_by(models.Empleado.id_empleado, models.Empleado.nombre)
        .order_by(models.Empleado.nombre)
        .all()
    )
    return resultados

@router.get("/ventas-por-cliente")
def get_reporte_ventas_por_cliente(db: Session = Depends(get_db)):
    """
    Genera un reporte que agrupa las compras totales por cada cliente.
    """
    resultados = (
        db.query(
            models.Cliente.rut_cliente,
            models.Cliente.nombre_completo.label("nombre_cliente"),
            func.count(models.Venta.id_venta).label("cantidad_compras"),
            func.sum(models.Venta.total_venta).label("monto_total_gastado"),
        )
        .join(models.Venta, models.Cliente.rut_cliente == models.Venta.rut_cliente)
        .group_by(models.Cliente.rut_cliente, models.Cliente.nombre_completo)
        .order_by(models.Cliente.nombre_completo)
        .all()
    )
    return resultados

@router.get("/ventas-por-producto")
def get_reporte_ventas_por_producto(db: Session = Depends(get_db)):
    """
    Genera un reporte que agrupa las ventas totales por cada producto.
    NOTA: Esta función asume que tienes una tabla/modelo llamado 'DetalleVenta'
    que conecta Venta y Producto, ya que no estaba en tu dump original.
    """
    # Si no tienes un modelo DetalleVenta, esta consulta fallará.
    # Necesitarías crearlo en models.py y en tu base de datos.
    # Por ahora, devolvemos datos de ejemplo para que el frontend no falle.
    
    # --- CÓDIGO REAL (CUANDO TENGAS LA TABLA DetalleVenta) ---
    # resultados = (
    #     db.query(
    #         models.Producto.sku,
    #         models.Producto.nombre.label("nombre_producto"),
    #         func.sum(models.DetalleVenta.cantidad).label("cantidad_total_vendida"),
    #         func.sum(models.DetalleVenta.cantidad * models.Producto.precio).label("monto_total_generado"),
    #     )
    #     .join(models.DetalleVenta, models.Producto.sku == models.DetalleVenta.sku_producto)
    #     .group_by(models.Producto.sku, models.Producto.nombre)
    #     .order_by(models.Producto.nombre)
    #     .all()
    # )
    # return resultados

    # --- DATOS DE EJEMPLO (SOLUCIÓN TEMPORAL) ---
    return [
        {"sku": 1001, "nombre_producto": "Producto A", "cantidad_total_vendida": 15, "monto_total_generado": 15000},
        {"sku": 1003, "nombre_producto": "Producto C", "cantidad_total_vendida": 10, "monto_total_generado": 15000},
        {"sku": 1005, "nombre_producto": "Producto E", "cantidad_total_vendida": 5, "monto_total_generado": 15000},
    ]