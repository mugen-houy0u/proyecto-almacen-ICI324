from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# =========================
#  ENTIDAD: Empleado
# =========================

class Empleado(Base):
    __tablename__ = "Empleado"

    id_empleado = Column(Integer, primary_key=True, autoincrement=True) # PK
    nombre = Column(String)
    rut_empleado = Column(String, unique=True) # Único por persona
    telefono = Column(String)
    correo = Column(String)
    direccion = Column(String)
    fecha_de_ingreso = Column(String)
    rol = Column(String)
    usuario = Column(String)
    contrasena = Column(String)

#  Relaciones (1 Empleado tiene muchos Proveedores/Ventas/Lotes)
    proveedores = relationship("Proveedor", back_populates="empleado")
    ventas = relationship("Venta", back_populates="empleado")
    lotes = relationship("Lote", back_populates="empleado")

# =========================
#  ENTIDAD: Proveedor
# =========================

class Proveedor(Base):
    __tablename__ = "Proveedor"

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)  # PK
    id_empleado = Column(Integer, ForeignKey("Empleado.id_empleado"))  # FK → Empleado
    correo = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    nombre_empresa = Column(String)

    empleado = relationship("Empleado", back_populates="proveedores")

# =========================
#  ENTIDAD: Cliente
# =========================

class Cliente(Base):
    __tablename__ = "Cliente"

    rut_cliente = Column(String, primary_key=True) # PK (usa el RUT como identificador)
    nombre_completo = Column(String)
    direccion = Column(String)
    celular = Column(String)
    correo = Column(String)
    fecha_de_nacimiento = Column(String)

    ventas = relationship("Venta", back_populates="cliente")


# =========================
#  ENTIDAD: Venta
# =========================

class Venta(Base):
    __tablename__ = "Venta"

    id_venta = Column(Integer, primary_key=True, autoincrement=True) # PK
    id_empleado = Column(Integer, ForeignKey("Empleado.id_empleado")) # FK → Empleado
    rut_cliente = Column(String, ForeignKey("Cliente.rut_cliente")) # FK → Cliente
    total_venta = Column(Integer)
    fecha_venta = Column(String)
    metodo_de_pago = Column(String)

    empleado = relationship("Empleado", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    reportes = relationship("Reporte", back_populates="venta") 


# =========================
#  ENTIDAD: Reporte
# =========================

class Reporte(Base):
    __tablename__ = "Reporte"

    id_reporte = Column(Integer, primary_key=True, autoincrement=True) # PK
    id_venta = Column(Integer, ForeignKey("Venta.id_venta")) # FK → Venta
    fecha_inicio = Column(String)
    fecha_final = Column(String)
    tipo_reporte = Column(String)
    total_ventas = Column(Integer)

    venta = relationship("Venta", back_populates="reportes")

# =========================
#  ENTIDAD: Producto
# =========================

class Producto(Base):
    __tablename__ = "Producto"

    sku = Column(Integer, primary_key=True) # PK (SKU)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Integer)
    stock = Column(Integer)
    categoria = Column(String)
    marca = Column(String)
    proveedor = Column(String)

    lotes = relationship("Lote", back_populates="producto")
    
# =========================
#  ENTIDAD: Lote 
# =========================

class Lote(Base):
    __tablename__ = "Lote"
    
# Clave primaria compuesta (no permite pares duplicados Empleado–Producto)
    id_empleado = Column(Integer, ForeignKey("Empleado.id_empleado"), primary_key=True)
    sku = Column(Integer, ForeignKey("Producto.sku"), primary_key=True)

    empleado = relationship("Empleado", back_populates="lotes")
    producto = relationship("Producto", back_populates="lotes")
