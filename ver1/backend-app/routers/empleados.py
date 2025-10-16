from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import get_db



# ==========================================================
# ESTADO: OFICIAL
# ==========================================================

# ==========================================================
# Grupo de rutas: EMPLEADOS
# ==========================================================
router = APIRouter(prefix="/empleados", tags=["Empleados"])


# ==========================================================
# GET /empleados
# Lista todos los empleados
# ==========================================================
@router.get(
    "/",
    summary="Listar todos los empleados",
    response_description="Lista completa de empleados registrados",
    status_code=status.HTTP_200_OK,
)
def get_empleados(db: Session = Depends(get_db)):
    """
    Retorna una lista con todos los empleados registrados.

    ### Retorna:
    - **200 OK**: Lista de empleados.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        empleados = db.query(models.Empleado).all()
        return empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener empleados: {e}")


# ==========================================================
# GET /empleados/{id_empleado}
# Obtiene un empleado específico por su ID
# ==========================================================
@router.get(
    "/{id_empleado}",
    summary="Obtener empleado por ID",
    response_description="Datos de un empleado específico",
    status_code=status.HTTP_200_OK,
)
def get_empleado(id_empleado: int, db: Session = Depends(get_db)):
    """
    Retorna los datos de un empleado según su ID.

    ### Parámetros:
    - **id_empleado (int)**: ID único del empleado.

    ### Retorna:
    - **200 OK**: Datos del empleado.
    - **404 Not Found**: Si el empleado no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar empleado: {e}")


# ==========================================================
# POST /empleados/cajero
# Crea un nuevo empleado con rol 'cajero'
# ==========================================================
@router.post(
    "/cajero",
    summary="Crear nuevo empleado con rol cajero",
    response_description="Empleado tipo cajero creado correctamente",
    status_code=status.HTTP_201_CREATED,
)
def create_cajero(
    nombre: str,
    rut_empleado: str,
    telefono: str,
    correo: str,
    direccion: str,
    fecha_de_ingreso: str,
    usuario: str,
    contrasena: str,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo empleado con el rol fijo 'cajero'.

    ### Parámetros:
    - **nombre (str)**: Nombre completo del empleado.
    - **rut_empleado (str)**: RUT o documento del empleado.
    - **telefono (str)**: Número de contacto.
    - **correo (str)**: Correo electrónico.
    - **direccion (str)**: Dirección del empleado.
    - **fecha_de_ingreso (str)**: Fecha de ingreso al trabajo.
    - **usuario (str)**: Nombre de usuario para el login.
    - **contrasena (str)**: Contraseña del empleado.

    ### Retorna:
    - **201 Created**: Si se crea correctamente.
    - **400 Bad Request**: Si faltan campos o son inválidos.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        if not all([nombre, rut_empleado, telefono, correo, direccion, fecha_de_ingreso, usuario, contrasena]):
            raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

        nuevo_cajero = models.Empleado(
            nombre=nombre,
            rut_empleado=rut_empleado,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            fecha_de_ingreso=fecha_de_ingreso,
            usuario=usuario,
            contrasena=contrasena,
            rol="cajero"
        )

        db.add(nuevo_cajero)
        db.commit()
        db.refresh(nuevo_cajero)

        return {"msg": "Cajero creado correctamente", "cajero": nuevo_cajero}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cajero: {e}")


# ==========================================================
# PUT /empleados/{id_empleado}
# Actualiza teléfono y correo de un empleado
# ==========================================================
@router.put(
    "/{id_empleado}",
    summary="Actualizar datos de un empleado",
    response_description="Empleado actualizado correctamente",
    status_code=status.HTTP_200_OK,
)
def update_empleado(
    id_empleado: int,
    telefono: str,
    correo: str,
    db: Session = Depends(get_db)
):
    """
    Actualiza el teléfono y correo de un empleado existente.

    ### Parámetros:
    - **id_empleado (int)**: ID del empleado.
    - **telefono (str)**: Nuevo número telefónico.
    - **correo (str)**: Nuevo correo electrónico.

    ### Retorna:
    - **200 OK**: Si se actualiza correctamente.
    - **404 Not Found**: Si el empleado no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        empleado.telefono = telefono
        empleado.correo = correo

        db.commit()
        db.refresh(empleado)
        return {"msg": "Empleado actualizado correctamente", "empleado": empleado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar empleado: {e}")


# ==========================================================
# DELETE /empleados/{id_empleado}
# Elimina un empleado existente por su ID
# ==========================================================
@router.delete(
    "/{id_empleado}",
    summary="Eliminar empleado por ID",
    response_description="Empleado eliminado correctamente",
    status_code=status.HTTP_200_OK,
)
def delete_empleado(id_empleado: int, db: Session = Depends(get_db)):
    """
    Elimina un empleado según su ID.

    ### Parámetros:
    - **id_empleado (int)**: ID único del empleado.

    ### Retorna:
    - **200 OK**: Si se elimina correctamente.
    - **404 Not Found**: Si el empleado no existe.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        db.delete(empleado)
        db.commit()
        return {"msg": f"Empleado con ID {id_empleado} eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar empleado: {e}")


# ==========================================================
# POST /empleados/login
# Verifica credenciales de acceso
# ==========================================================
@router.post(
    "/login",
    summary="Inicio de sesión de empleado",
    response_description="Autenticación correcta",
    status_code=status.HTTP_200_OK,
)
def login(usuario: str, contrasena: str, db: Session = Depends(get_db)):
    """
    Verifica si el usuario y contraseña existen en la tabla Empleado.

    ### Parámetros:
    - **usuario (str)**: Nombre de usuario del empleado.
    - **contrasena (str)**: Contraseña del empleado.

    ### Retorna:
    - **200 OK**: Si las credenciales son correctas.
    - **401 Unauthorized**: Si las credenciales son incorrectas.
    - **500 Internal Server Error**: Si ocurre un error inesperado.
    """
    try:
        empleado = (
            db.query(models.Empleado)
            .filter(models.Empleado.usuario == usuario, models.Empleado.contrasena == contrasena)
            .first()
        )

        if not empleado:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        return {
            "msg": "Inicio de sesión exitoso",
            "empleado": {
                "id_empleado": empleado.id_empleado,
                "nombre": empleado.nombre,
                "rol": empleado.rol,
                "correo": empleado.correo,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante el inicio de sesión: {e}")
