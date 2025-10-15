import { useState, useMemo } from 'preact/hooks';
import type { Proveedor, Item, Totales } from './types';

export function useInvoice() {
  // Estado del proveedor
  const [proveedor, setProveedor] = useState<Proveedor>({
    rut: '',
    nombre: '',
    correo: '',
    giro: '',
    fechaEmision: '',
    formaPago: 'Contado', // 👈 valor inicial válido
  });

  // Estado de ítems
  const [items, setItems] = useState<Item[]>([
    { id: 1, descripcion: '', cantidad: 1, um: 'UN', precio: 0, porcImpuesto: 0, porcDescuento: 0, total: 0 },
  ]);

  // Totales calculados
  const totales: Totales = useMemo(() => {
    const subtotal = items.reduce((acc, r) => acc + r.cantidad * r.precio, 0);
    const impuestos = items.reduce((acc, r) => acc + (r.precio * r.cantidad * r.porcImpuesto) / 100, 0);
    const descuentos = items.reduce((acc, r) => acc + (r.precio * r.cantidad * r.porcDescuento) / 100, 0);
    return {
      subtotal,
      impuestos,
      descuentos,
      total: subtotal + impuestos - descuentos,
    };
  }, [items]);

  // Funciones auxiliares
  const addRow = () =>
    setItems([
      ...items,
      { id: items.length + 1, descripcion: '', cantidad: 1, um: 'UN', precio: 0, porcImpuesto: 0, porcDescuento: 0, total: 0 },
    ]);

  const removeRow = (id: number) => setItems(items.filter((r) => r.id !== id));

  const updateRow = (id: number, newRow: Partial<Item>) =>
    setItems(items.map((r) => (r.id === id ? { ...r, ...newRow } : r)));

  const payload = { proveedor, items, totales };

  return {
    proveedor,
    setProveedor,
    items,
    setItems,
    totales,
    addRow,
    removeRow,
    updateRow,
    payload,
  };
}
