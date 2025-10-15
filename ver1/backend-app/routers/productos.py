from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
from database import get_db

# Rutas de Productos
router = APIRouter(prefix="/productos", tags=["Productos"])

# SELECT simple: lista todos los productos
@router.get("/")
def get_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

# UPDATE: actualizar stock de un producto por SKU
@router.put("/producto/{sku}")
def update_stock(sku: int, nuevo_stock: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.sku == sku).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado en inventario")

    producto.stock = nuevo_stock
    db.commit()
    db.refresh(producto)
    return {"message": "Stock actualizado correctamente", "inventario": producto}

# UPDATE: actualizar precio de un producto por SKU
@router.put("/producto/{sku}/precio")
def update_precio_producto(sku: int, nuevo_precio: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.sku == sku).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.precio = nuevo_precio
    db.commit()
    db.refresh(producto)
    return {"message": "Precio actualizado correctamente", "producto": producto}

# DROP lógico: vacía la tabla Producto (DELETE FROM)
@router.delete("/drop")
def drop_productos(db: Session = Depends(get_db)):
    try:
        db.query(models.Producto).delete()
        db.commit()
        return {"message": "Todos los productos han sido eliminados"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar productos: {str(e)}")


# INSERT: crea un producto nuevo (SKU es PK)
@router.post("/producto")
def create_producto(
    sku: int,
    nombre: str,
    descripcion: str,
    precio: int,
    stock: int,
    categoria: str,
    marca: str,
    proveedor: str,
    db: Session = Depends(get_db),
):

# Construye el objeto ORM para insertar
    nuevo = models.Producto(
        sku=sku,
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        categoria=categoria,
        marca=marca,
        proveedor=proveedor,
    )
    try:
        db.add(nuevo) # INSERT
        db.commit() # confirma escritura
        db.refresh(nuevo) # sincroniza el objeto con la BD
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El SKU ya existe.")
    return {"message": "Producto creado correctamente", "producto": nuevo}
