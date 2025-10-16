import sqlite3

createEmpleado = """CREATE TABLE IF NOT EXISTS Empleado(
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            rut_empleado TEXT,
            telefono TEXT,
            correo TEXT,
            direccion TEXT,
            fecha_de_ingreso TEXT,
            rol TEXT,
            usuario TEXT,
            contrasena TEXT
            )"""

createProveedor = """CREATE TABLE IF NOT EXISTS Proveedor(
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER,
            correo TEXT,
            telefono TEXT,
            direccion TEXT,
            nombre_empresa TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Empleado(id_empleado))"""

createCliente = """CREATE TABLE IF NOT EXISTS Cliente(
            rut_cliente TEXT PRIMARY KEY,
            nombre_completo TEXT,
            direccion TEXT,
            celular TEXT,
            correo TEXT,
            fecha_de_nacimiento TEXT
            )"""

createVenta = """CREATE TABLE IF NOT EXISTS Venta(
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER,
            rut_cliente TEXT,
            total_venta INTEGER,
            fecha_venta TEXT,
            metodo_de_pago TEXT,
            FOREIGN KEY(id_empleado) REFERENCES Empleado(id_empleado),
            FOREIGN KEY(rut_cliente) REFERENCES Cliente(rut_cliente))"""

createReporte = """CREATE TABLE IF NOT EXISTS Reporte(
            id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER,
            fecha_inicio TEXT,
            fecha_final TEXT,
            tipo_reporte TEXT,
            total_ventas INTEGER,
            FOREIGN KEY(id_venta) REFERENCES Venta(id_venta))"""

createProducto = """CREATE TABLE IF NOT EXISTS Producto(
            sku INTEGER PRIMARY KEY,
            nombre TEXT,
            descripcion TEXT,
            precio INTEGER,
            stock INTEGER,
            categoria TEXT,
            marca TEXT,
            proveedor TEXT
            )"""

crearLote = """CREATE TABLE IF NOT EXISTS Lote(
            id_empleado INTEGER REFERENCES Empleado(id_empleado),
            sku INTEGER REFERENCES Producto(sku),
            PRIMARY KEY(id_empleado, sku))"""

crearFactura = """CREATE TABLE IF NOT EXISTS Factura(
                id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT,
                id_proveedor INTEGER,
                nombre_razon_social TEXT,
                correo TEXT,
                giro INTEGER,
                fecha_emision TEXT,
                forma_de_pago TEXT,
                FOREIGN KEY(id_proveedor) REFERENCES Proveedor(id_proveedor))"""

def crearBD():
    cursor.execute(createEmpleado)
    cursor.execute(createProveedor)
    cursor.execute(createCliente)
    cursor.execute(createVenta)
    cursor.execute(createReporte)
    cursor.execute(createProducto)
    cursor.execute(crearLote)
    cursor.execute(crearFactura)

conn = sqlite3.connect('mercado.db')
cursor = conn.cursor()
crearBD()

with open("dump.sql", "r", encoding="utf-8") as dump:
    sql_script = dump.read()
    
cursor.executescript(sql_script)