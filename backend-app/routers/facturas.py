from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import get_db

# ==========================================================
# ESTADO: OFICIAL
# ==========================================================


# ==========================================================
# Grupo de rutas: FACTURAS
# ==========================================================
router = APIRouter(prefix="/facturas", tags=["Facturas"])


# ==========================================================
# GET /facturas
# Lista todas las facturas emitidas
# ==========================================================
@router.get(
    "/",
    summary="Listar todas las facturas emitidas",
    response_description="Lista completa de facturas registradas",
    status_code=status.HTTP_200_OK,
)
def get_facturas(db: Session = Depends(get_db)):
    """
    Retorna una lista con todas las facturas registradas.

    ### Retorna:
    - **200 OK**: Lista de facturas.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        facturas = db.query(models.Factura).all()
        return facturas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener facturas: {e}")


# ==========================================================
# GET /facturas/{id_factura}
# Obtiene el detalle completo de una factura por ID
# ==========================================================
@router.get(
    "/{id_factura}",
    summary="Obtener factura por ID",
    response_description="Datos completos de una factura",
    status_code=status.HTTP_200_OK,
)
def get_factura(id_factura: int, db: Session = Depends(get_db)):
    """
    Retorna los datos de una factura según su ID.

    ### Parámetros:
    - **id_factura (int)**: Identificador único de la factura.

    ### Retorna:
    - **200 OK**: Datos de la factura.
    - **404 Not Found**: Si la factura no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        factura = db.query(models.Factura).filter(models.Factura.id_factura == id_factura).first()
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar factura: {e}")



# ==========================================================
# POST /facturas
# Crea una nueva factura
# ==========================================================
@router.post(
    "/",
    summary="Crear nueva factura",
    response_description="Factura creada correctamente",
    status_code=status.HTTP_201_CREATED,
)
def create_factura(
    rut: str,
    id_proveedor: int,
    nombre_razon_social: str,
    correo: str,
    giro: int,
    fecha_emision: str,
    forma_de_pago: str,
    db: Session = Depends(get_db),
):
    """
    Crea una nueva factura en la base de datos.

    ### Parámetros:
    - **rut (str)**: Rut asociado de la factura.
    - **id_proveedor (int)**: ID del proveedor asociado.
    - **nombre_razon_social (str)**: Nombre o razón social.
    - **correo (str)**: Correo del proveedor.
    - **giro (int)**: Tipo de giro.
    - **fecha_emision (str)**: Fecha de emisión de la factura.
    - **forma_de_pago (str)**: Método o condición de pago.

    ### Retorna:
    - **201 Created**: Factura creada correctamente.
    - **400 Bad Request**: Si los campos obligatorios faltan o ya existe el RUT.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        if not all([rut, id_proveedor, nombre_razon_social, correo, giro, fecha_emision, forma_de_pago]):
            raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

        existente = db.query(models.Factura).filter(models.Factura.rut == rut).first()
        if existente:
            raise HTTPException(status_code=400, detail="La factura ya existe")

        nueva_factura = models.Factura(
            rut=rut,
            id_proveedor=id_proveedor,
            nombre_razon_social=nombre_razon_social,
            correo=correo,
            giro=giro,
            fecha_emision=fecha_emision,
            forma_de_pago=forma_de_pago,
        )

        db.add(nueva_factura)
        db.commit()
        db.refresh(nueva_factura)

        return {"msg": "Factura creada correctamente", "factura": nueva_factura}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear factura: {e}")

# ==========================================================
# PUT /facturas/{id_factura}
# Actualiza los datos de una factura
# ==========================================================
@router.put(
    "/{id_factura}",
    summary="Actualizar factura existente",
    response_description="Factura actualizada correctamente",
    status_code=status.HTTP_200_OK,
)
def update_factura(
    id_factura: int,
    id_proveedor: int,
    nombre_razon_social: str,
    correo: str,
    giro: int,
    fecha_emision: str,
    forma_de_pago: str,
    db: Session = Depends(get_db),
):
    """
    Actualiza los datos de una factura existente.

    ### Parámetros:
    - **id_factura (int)**: ID de la factura a modificar.
    - Los demás campos se pueden actualizar.

    ### Retorna:
    - **200 OK**: Factura actualizada correctamente.
    - **404 Not Found**: Si la factura no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        factura = db.query(models.Factura).filter(models.Factura.id_factura == id_factura).first()
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")

        factura.id_proveedor = id_proveedor
        factura.nombre_razon_social = nombre_razon_social
        factura.correo = correo
        factura.giro = giro
        factura.fecha_emision = fecha_emision
        factura.forma_de_pago = forma_de_pago

        db.commit()
        db.refresh(factura)

        return {"msg": "Factura actualizada correctamente", "facturaActualizada": factura}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar factura: {e}")


# ==========================================================
# DELETE /facturas/{id_factura}
# Elimina una factura por su ID
# ==========================================================
@router.delete(
    "/{id_factura}",
    summary="Eliminar factura por ID",
    response_description="Factura eliminada correctamente",
    status_code=status.HTTP_200_OK,
)
def delete_factura(id_factura: int, db: Session = Depends(get_db)):
    """
    Elimina una factura de la base de datos según su ID.

    ### Parámetros:
    - **id_factura (int)**: Identificador único de la factura.

    ### Retorna:
    - **200 OK**: Factura eliminada correctamente.
    - **404 Not Found**: Si la factura no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        factura = db.query(models.Factura).filter(models.Factura.id_factura == id_factura).first()
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")

        db.delete(factura)
        db.commit()
        return {"msg": "Factura eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar factura: {e}")
