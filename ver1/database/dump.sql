BEGIN TRANSACTION;

INSERT INTO Empleado (nombre, rut_empleado, telefono, correo, direccion, fecha_de_ingreso, rol, usuario, contrasena) VALUES
('Juan Pérez', '11.111.111-1', '912345678', 'juan.perez@empresa.com', 'Calle Falsa 123', '2022-01-01', 'cajero', 'jperez', '1234'),
('María López', '22.222.222-2', '923456789', 'maria.lopez@empresa.com', 'Avenida Siempre Viva 456', '2022-02-01', 'cajero', 'mlopez', '1234'),
('Carlos Gómez', '33.333.333-3', '934567890', 'carlos.gomez@empresa.com', 'Boulevard Central 789', '2021-05-01', 'administrador', 'cgomez', 'admin123');

INSERT INTO Proveedor (id_empleado, correo, telefono, direccion, nombre_empresa) VALUES
(3, 'contacto@proveedor1.com', '987654321', 'Calle Uno 111', 'Proveedor Uno'),
(3, 'contacto@proveedor2.com', '976543210', 'Calle Dos 222', 'Proveedor Dos'),
(3, 'contacto@proveedor3.com', '965432109', 'Calle Tres 333', 'Proveedor Tres'),
(3, 'contacto@proveedor4.com', '954321098', 'Calle Cuatro 444', 'Proveedor Cuatro'),
(3, 'contacto@proveedor5.com', '943210987', 'Calle Cinco 555', 'Proveedor Cinco');

INSERT INTO Producto (sku, nombre, descripcion, precio, stock, categoria, marca, proveedor) VALUES
(1001, 'Producto A', 'Descripcion A', 1000, 50, 'Categoria1', 'Marca1', 'Proveedor Uno'),
(1002, 'Producto B', 'Descripcion B', 2000, 50, 'Categoria1', 'Marca1', 'Proveedor Uno'),
(1003, 'Producto C', 'Descripcion C', 1500, 50, 'Categoria2', 'Marca2', 'Proveedor Dos'),
(1004, 'Producto D', 'Descripcion D', 2500, 50, 'Categoria2', 'Marca2', 'Proveedor Dos'),
(1005, 'Producto E', 'Descripcion E', 3000, 50, 'Categoria3', 'Marca3', 'Proveedor Tres'),
(1006, 'Producto F', 'Descripcion F', 3500, 50, 'Categoria3', 'Marca3', 'Proveedor Tres'),
(1007, 'Producto G', 'Descripcion G', 4000, 50, 'Categoria4', 'Marca4', 'Proveedor Cuatro'),
(1008, 'Producto H', 'Descripcion H', 4500, 50, 'Categoria4', 'Marca4', 'Proveedor Cuatro'),
(1009, 'Producto I', 'Descripcion I', 5000, 50, 'Categoria5', 'Marca5', 'Proveedor Cinco'),
(1010, 'Producto J', 'Descripcion J', 5500, 50, 'Categoria5', 'Marca5', 'Proveedor Cinco');

INSERT INTO Lote (id_empleado, sku) VALUES
(3, 1001),(3, 1002),(3, 1003),(3, 1004),(3, 1005),
(3, 1006),(3, 1007),(3, 1008),(3, 1009),(3, 1010);

INSERT INTO Cliente (rut_cliente, nombre_completo, direccion, celular, correo, fecha_de_nacimiento) VALUES
('1-9', 'Cliente Uno', 'Direccion 1', '900000001', 'cliente1@mail.com', '1990-01-01'),
('2-7', 'Cliente Dos', 'Direccion 2', '900000002', 'cliente2@mail.com', '1991-02-02'),
('3-5', 'Cliente Tres', 'Direccion 3', '900000003', 'cliente3@mail.com', '1992-03-03'),
('4-3', 'Cliente Cuatro', 'Direccion 4', '900000004', 'cliente4@mail.com', '1993-04-04'),
('5-1', 'Cliente Cinco', 'Direccion 5', '900000005', 'cliente5@mail.com', '1994-05-05'),
('6-9', 'Cliente Seis', 'Direccion 6', '900000006', 'cliente6@mail.com', '1995-06-06'),
('7-7', 'Cliente Siete', 'Direccion 7', '900000007', 'cliente7@mail.com', '1996-07-07'),
('8-5', 'Cliente Ocho', 'Direccion 8', '900000008', 'cliente8@mail.com', '1997-08-08'),
('9-3', 'Cliente Nueve', 'Direccion 9', '900000009', 'cliente9@mail.com', '1998-09-09'),
('10-1', 'Cliente Diez', 'Direccion 10', '900000010', 'cliente10@mail.com', '1999-10-10');

INSERT INTO Venta (id_empleado, rut_cliente, total_venta, fecha_venta, metodo_de_pago) VALUES
(1, '1-9', 1000, '2023-01-01', 'efectivo'),
(2, '1-9', 2000, '2023-01-02', 'tarjeta'),
(1, '1-9', 3000, '2023-01-03', 'efectivo'),
(2, '1-9', 4000, '2023-01-04', 'tarjeta'),
(1, '1-9', 5000, '2023-01-05', 'efectivo'),

(2, '2-7', 1500, '2023-01-01', 'tarjeta'),
(1, '2-7', 2500, '2023-01-02', 'efectivo'),
(2, '2-7', 3500, '2023-01-03', 'tarjeta'),
(1, '2-7', 4500, '2023-01-04', 'efectivo'),
(2, '2-7', 5500, '2023-01-05', 'tarjeta'),

(1, '3-5', 2000, '2023-01-01', 'efectivo'),
(2, '3-5', 3000, '2023-01-02', 'tarjeta'),
(1, '3-5', 4000, '2023-01-03', 'efectivo'),
(2, '3-5', 5000, '2023-01-04', 'tarjeta'),
(1, '3-5', 6000, '2023-01-05', 'efectivo'),

(2, '4-3', 1000, '2023-01-01', 'tarjeta'),
(1, '4-3', 2000, '2023-01-02', 'efectivo'),
(2, '4-3', 3000, '2023-01-03', 'tarjeta'),
(1, '4-3', 4000, '2023-01-04', 'efectivo'),
(2, '4-3', 5000, '2023-01-05', 'tarjeta'),

(1, '5-1', 1500, '2023-01-01', 'efectivo'),
(2, '5-1', 2500, '2023-01-02', 'tarjeta'),
(1, '5-1', 3500, '2023-01-03', 'efectivo'),
(2, '5-1', 4500, '2023-01-04', 'tarjeta'),
(1, '5-1', 5500, '2023-01-05', 'efectivo'),

(2, '6-9', 2000, '2023-01-01', 'tarjeta'),
(1, '6-9', 3000, '2023-01-02', 'efectivo'),
(2, '6-9', 4000, '2023-01-03', 'tarjeta'),
(1, '6-9', 5000, '2023-01-04', 'efectivo'),
(2, '6-9', 6000, '2023-01-05', 'tarjeta'),

(1, '7-7', 1000, '2023-01-01', 'efectivo'),
(2, '7-7', 2000, '2023-01-02', 'tarjeta'),
(1, '7-7', 3000, '2023-01-03', 'efectivo'),
(2, '7-7', 4000, '2023-01-04', 'tarjeta'),
(1, '7-7', 5000, '2023-01-05', 'efectivo'),

(2, '8-5', 1500, '2023-01-01', 'tarjeta'),
(1, '8-5', 2500, '2023-01-02', 'efectivo'),
(2, '8-5', 3500, '2023-01-03', 'tarjeta'),
(1, '8-5', 4500, '2023-01-04', 'efectivo'),
(2, '8-5', 5500, '2023-01-05', 'tarjeta'),

(1, '9-3', 2000, '2023-01-01', 'efectivo'),
(2, '9-3', 3000, '2023-01-02', 'tarjeta'),
(1, '9-3', 4000, '2023-01-03', 'efectivo'),
(2, '9-3', 5000, '2023-01-04', 'tarjeta'),
(1, '9-3', 6000, '2023-01-05', 'efectivo'),

(2, '10-1', 1000, '2023-01-01', 'tarjeta'),
(1, '10-1', 2000, '2023-01-02', 'efectivo'),
(2, '10-1', 3000, '2023-01-03', 'tarjeta'),
(1, '10-1', 4000, '2023-01-04', 'efectivo'),
(2, '10-1', 5000, '2023-01-05', 'tarjeta');

COMMIT;