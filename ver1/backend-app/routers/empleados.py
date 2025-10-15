from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

# Rutas de Empleados
router = APIRouter(prefix="/empleados", tags=["Empleados"])

# SELECT simple: lista todos los empleados
@router.get("/")
def get_empleados(db: Session = Depends(get_db)):
    return db.query(models.Empleado).all()

# 👇 AÑADE ESTA NUEVA FUNCIÓN 👇
# SELECT por ID: obtiene un solo empleado
@router.get("/{id_empleado}")
def get_empleado_por_id(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        # Si no se encuentra, devuelve un error 404 claro
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

# DELETE: elimina un empleado por ID
# CORRECCIÓN: La ruta no debe repetirse, FastAPI es inteligente
@router.delete("/{id_empleado}")
def delete_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    db.delete(empleado)
    db.commit()
    return {"message": f"Empleado con ID {id_empleado} eliminado correctamente"}

# UPDATE: actualiza teléfono y correo de un empleado
# CORRECCIÓN: La ruta no debe repetirse
@router.put("/{id_empleado}")
def update_empleado(id_empleado: int, telefono: str, correo: str, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    empleado.telefono = telefono
    empleado.correo = correo
    db.commit()
    db.refresh(empleado)
    return {"message": "Empleado actualizado correctamente", "empleado": empleado}

# INSERT: crea un empleado con rol 'cajero'
@router.post("/cajero")
def create_cajero(nombre: str, rut_empleado: str, telefono: str, correo: str, direccion:str, fecha_de_ingreso:str, usuario:str,contrasena:str, db: Session = Depends(get_db)):
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
    return {"message": "Cajero creado correctamente", "cajero": nuevo_cajero}
