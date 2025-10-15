from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

# Grupo de rutas para Proveedores
router = APIRouter(prefix="/proveedores", tags=["Proveedores"])



# -----------------------------------
# GET /proveedores
# Lista todos los proveedores
# -----------------------------------
@router.get("/")
def get_proveedores(db: Session = Depends(get_db)):
    return db.query(models.Proveedor).all()

# -----------------------------------
# GET /proveedores/{id}
# Obtiene un proveedor específico por ID
# -----------------------------------
@router.get("/{id_proveedor}")
def get_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

# -----------------------------------
# POST /proveedores
# Crea un nuevo proveedor
# -----------------------------------
@router.post("/")
def create_proveedor(
    id_empleado: int,
    correo: str,
    telefono: str,
    direccion: str,
    nombre_empresa: str,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proveedor con todos sus datos.
    Equivalente a:
    INSERT INTO Proveedor (id_empleado, correo, telefono, direccion, nombre_empresa)
    VALUES (...)
    """
    nuevo_proveedor = models.Proveedor(
        id_empleado=id_empleado,
        correo=correo,
        telefono=telefono,
        direccion=direccion,
        nombre_empresa=nombre_empresa
    )

    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)

    return {"msg": "Proveedor creado correctamente", "proveedor": nuevo_proveedor}


# -----------------------------------
# PUT /proveedores/{id}
# Actualiza un proveedor existente
# -----------------------------------
@router.put("/{id_proveedor}")
def update_proveedor(
    id_proveedor: int,
    correo: str,
    telefono: str,
    direccion: str,
    nombre_empresa: str,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos principales de un proveedor existente.
    Permite modificar: correo, telefono, direccion, nombre_empresa
    """
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()

    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    proveedor.correo = correo
    proveedor.telefono = telefono
    proveedor.direccion = direccion
    proveedor.nombre_empresa = nombre_empresa

    db.commit()
    db.refresh(proveedor)

    return {"msg": "Proveedor actualizado correctamente", "proveedorActualizado": proveedor}

# -----------------------------------
# DELETE /proveedores/{id}
# Elimina un proveedor existente
# -----------------------------------
@router.delete("/{id_proveedor}")
def delete_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    db.delete(proveedor)
    db.commit()
    return {"msg": "Proveedor eliminado"}
