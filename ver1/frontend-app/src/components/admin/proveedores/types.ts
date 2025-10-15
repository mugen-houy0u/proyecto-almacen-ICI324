// Tipos centralizados del módulo Proveedores

// ✅ Lista única de formas de pago válidas
export const FORMA_PAGO = ['Contado', 'Crédito', 'Transferencia'] as const;

// ✅ Tipo literal derivado del array anterior
export type FormaPago = typeof FORMA_PAGO[number];

// ✅ Estructura de proveedor
export type Proveedor = {
  rut: string;
  nombre: string;
  correo: string;
  giro?: string;
  fechaEmision: string;
  formaPago: FormaPago;
};

// ✅ Estructura de un ítem dentro de la factura
export type Item = {
  id: number;
  descripcion: string;
  cantidad: number;
  um: string;
  precio: number;
  porcImpuesto: number;
  porcDescuento: number;
  total: number;
};

// ✅ Totales calculados
export type Totales = {
  subtotal: number;
  impuestos: number;
  descuentos: number;
  total: number;
};
