from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import get_db


# ==========================================================
# ESTADO: OFICIAL
# ==========================================================


# ==========================================================
# Grupo de rutas: PROVEEDORES
# ==========================================================
router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


# ==========================================================
# GET /proveedores
# Lista todos los proveedores
# ==========================================================
@router.get(
    "/",
    summary="Listar todos los proveedores",
    response_description="Lista completa de proveedores registrados",
    status_code=status.HTTP_200_OK,
)
def get_proveedores(db: Session = Depends(get_db)):
    """
    Retorna una lista con todos los proveedores registrados.

    ### Retorna:
    - **200 OK**: Lista de proveedores.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        proveedores = db.query(models.Proveedor).all()
        return proveedores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proveedores: {e}")


# ==========================================================
# GET /proveedores/{id_proveedor}
# Obtiene un proveedor específico por su ID
# ==========================================================
@router.get(
    "/{id_proveedor}",
    summary="Obtener proveedor por ID",
    response_description="Datos de un proveedor específico",
    status_code=status.HTTP_200_OK,
)
def get_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    """
    Retorna los datos de un proveedor según su ID.

    ### Parámetros:
    - **id_proveedor (int)**: ID único del proveedor.

    ### Retorna:
    - **200 OK**: Datos del proveedor.
    - **404 Not Found**: Si el proveedor no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar proveedor: {e}")


# ==========================================================
# POST /proveedores
# Crea un nuevo proveedor
# ==========================================================
@router.post(
    "/",
    summary="Crear nuevo proveedor",
    response_description="Proveedor creado correctamente",
    status_code=status.HTTP_201_CREATED,
)
def create_proveedor(
    id_empleado: int,
    correo: str,
    telefono: str,
    direccion: str,
    nombre_empresa: str,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proveedor en la base de datos.

    ### Parámetros:
    - **id_empleado (int)**: ID del empleado que registra al proveedor.
    - **correo (str)**: Correo electrónico del proveedor.
    - **telefono (str)**: Número de contacto.
    - **direccion (str)**: Dirección del proveedor.
    - **nombre_empresa (str)**: Nombre de la empresa proveedora.

    ### Retorna:
    - **201 Created**: Si el proveedor se crea correctamente.
    - **400 Bad Request**: Si los datos son inválidos o faltan.
    - **500 Internal Server Error**: Si ocurre un error en la base de datos.
    """
    try:
        if not all([id_empleado, correo, telefono, direccion, nombre_empresa]):
            raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear proveedor: {e}")


# ==========================================================
# PUT /proveedores/{id_proveedor}
# Actualiza los datos de un proveedor existente
# ==========================================================
@router.put(
    "/{id_proveedor}",
    summary="Actualizar proveedor existente",
    response_description="Proveedor actualizado correctamente",
    status_code=status.HTTP_200_OK,
)
def update_proveedor(
    id_proveedor: int,
    correo: str,
    telefono: str,
    direccion: str,
    nombre_empresa: str,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un proveedor existente.

    ### Parámetros:
    - **id_proveedor (int)**: ID del proveedor a modificar.
    - **correo (str)**, **telefono (str)**, **direccion (str)**, **nombre_empresa (str)**.

    ### Retorna:
    - **200 OK**: Si se actualiza correctamente.
    - **404 Not Found**: Si el proveedor no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar proveedor: {e}")


# ==========================================================
# DELETE /proveedores/{id_proveedor}
# Elimina un proveedor existente
# ==========================================================
@router.delete(
    "/{id_proveedor}",
    summary="Eliminar proveedor por ID",
    response_description="Proveedor eliminado correctamente",
    status_code=status.HTTP_200_OK,
)
def delete_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    """
    Elimina un proveedor de la base de datos según su ID.

    ### Parámetros:
    - **id_proveedor (int)**: ID único del proveedor.

    ### Retorna:
    - **200 OK**: Si se elimina correctamente.
    - **404 Not Found**: Si el proveedor no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == id_proveedor).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

        db.delete(proveedor)
        db.commit()
        return {"msg": "Proveedor eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar proveedor: {e}")
