import sqlite3

createEmpleado = """CREATE TABLE IF NOT EXISTS Empleado(
            id_empleado INTEGER PRIMARY KEY,
            id_inventario INTEGER,
            nombre TEXT,
            rut TEXT,
            telefono TEXT,
            correo TEXT,
            direccion TEXT,
            fecha_de_ingreso TEXT,
            FOREIGN KEY(id_inventario) REFERENCES Inventario(id_inventario))"""

createInventario = """CREATE TABLE IF NOT EXISTS Inventario(
            id_inventario INTEGER PRIMARY KEY,
            id_producto INTEGER,
            stock INTEGER,
            fecha_ultima_entrada TEXT,
            proveedor TEXT,
            ubicación TEXT,
            precio_venta INTEGER,
            precio_costo INTEGER)"""

createAdministrador = """CREATE TABLE IF NOT EXISTS Administrador(
            id_empleado INTEGER PRIMARY KEY,
            usuario TEXT,
            contraseña TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Empleado(id_empleado))"""

createProveedor = """CREATE TABLE IF NOT EXISTS Proveedor(
            id_proveedor INTEGER PRIMARY KEY,
            id_empleado INTEGER,
            correo TEXT,
            representante TEXT,
            telefono TEXT,
            direccion TEXT,
            nombre_empresa TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Administrador(id_empleado))"""

createCajero = """CREATE TABLE IF NOT EXISTS Cajero(
            id_empleado INTEGER PRIMARY KEY,
            usuario TEXT,
            contraseña TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Empleado(id_empleado))"""

createCliente = """CREATE TABLE IF NOT EXISTS Cliente(
            rut TEXT PRIMARY KEY,
            id_empleado INTEGER,
            nombre_completo TEXT,
            direccion TEXT,
            celular TEXT,
            correo TEXT,
            fecha_de_nacimiento TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Cajero(id_empleado))"""

createVenta = """CREATE TABLE IF NOT EXISTS Venta(
            id_venta INTEGER PRIMARY KEY,
            id_empleado INTEGER,
            fecha_venta TEXT,
            total_venta INTEGER,
            id_cliente INTEGER,
            metodo_de_pago TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Cajero(id_empleado))"""

createReporte = """CREATE TABLE IF NOT EXISTS Reporte(
            id_reporte INTEGER PRIMARY KEY,
            id_venta INTEGER,
            fecha_reporte TEXT,
            tipo_reporte TEXT,
            fecha_inicio TEXT,
            fecha_final TEXT,
            total_compras INTEGER,
            total_ventas INTEGER,
            inventario_final INTEGER,
            FOREIGN KEY(id_venta) REFERENCES Venta(id_venta))"""

createProducto = """CREATE TABLE IF NOT EXISTS Producto(
            id_producto INTEGER PRIMARY KEY,
            rut TEXT,
            nombre TEXT,
            descripcion TEXT,
            precio INTEGER,
            stock INTEGER,
            fecha_ingreso TEXT,
            categoria TEXT,
            marca TEXT,
            proveedor TEXT,
            sku TEXT,
            FOREIGN KEY(rut) REFERENCES Cliente(rut))"""

def crearBD():
    cursor.execute(createEmpleado)
    cursor.execute(createInventario)
    cursor.execute(createAdministrador)
    cursor.execute(createProveedor)
    cursor.execute(createCajero)
    cursor.execute(createCliente)
    cursor.execute(createVenta)
    cursor.execute(createReporte)
    cursor.execute(createProducto)

conn = sqlite3.connect('mercado.db')
cursor = conn.cursor()
crearBD()

#with open("dump_sqlite_inserts_fix_all.sql", "r", encoding="utf-8") as dump:
    #sql_script = dump.read()
#cursor.executescript(sql_script)

cursor.execute("SELECT * FROM Inventario")
for row in cursor.fetchall():
    print(row)
conn.close()