import type { Item, Proveedor, Totales } from './types';
import { money } from './money';
import type { Ref } from 'preact';

type Props = { proveedor?: Proveedor; items?: Item[]; totales?: Totales; elRef?: Ref<HTMLElement>; };

const EMPTY_PROV: Proveedor = { rut: '', nombre: '', correo: '', giro: '', fechaEmision: '', formaPago: 'Contado' };
const ZERO_TOTALS: Totales = { subtotal: 0, impuestos: 0, descuentos: 0, total: 0 };

export default function InvoicePreview({ proveedor = EMPTY_PROV, items = [], totales = ZERO_TOTALS, elRef }: Props) {
  return (
    <section ref={elRef} class="rounded-lg border border-gray-700 bg-gray-900 text-white p-4 shadow-lg">
      {/* Header */}
      <header class="flex items-center justify-between border-b border-gray-700 pb-3 mb-3">
        <div>
          <div class="text-xs text-gray-400">PRUEBA</div>
          <h2 class="text-xl font-semibold text-white">Factura</h2>
          <div class="text-xs text-gray-400">Emisor demo — www.demo.cl — +56 55 5555</div>
        </div>
        <div class="inline-flex items-center rounded-md border-2 border-red-500 px-3 py-1 text-sm font-bold text-red-500 uppercase tracking-wide">
          Factura electrónica
        </div>
      </header>

      {/* Datos proveedor */}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm mb-4">
        <div class="space-y-1">
          <div><span class="font-medium text-white">Señor(es):</span> {proveedor.nombre || '—'}</div>
          <div><span class="font-medium text-white">R.U.T.:</span> {proveedor.rut || '—'}</div>
          <div><span class="font-medium text-white">Giro:</span> {proveedor.giro || '—'}</div>
          <div><span class="font-medium text-white">Correo:</span> {proveedor.correo || '—'}</div>
        </div>
        <div class="space-y-1">
          <div><span class="font-medium text-white">Fecha emisión:</span> {proveedor.fechaEmision || '—'}</div>
          <div><span class="font-medium text-white">Forma de pago:</span> {proveedor.formaPago || '—'}</div>
        </div>
      </div>

      {/* Tabla de productos */}
      <div class="overflow-hidden rounded-lg border border-gray-700">
        <table class="min-w-full divide-y divide-gray-700">
          <thead class="bg-gray-800">
            <tr>
              {['N°', 'Descripción', 'Cantidad', 'U.M', 'Precio', '% Imp.', '% Desc.', 'Total'].map((h, i) => (
                <th
                  key={i}
                  class="px-4 py-2 text-left text-xs font-semibold uppercase tracking-wide text-white"
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-700 bg-gray-900">
            {items.map((r) => (
              <tr key={r.id}>
                <td class="px-4 py-2 font-mono">{r.id}</td>
                <td class="px-4 py-2">{r.descripcion || '—'}</td>
                <td class="px-4 py-2 font-mono">{r.cantidad}</td>
                <td class="px-4 py-2">{r.um}</td>
                <td class="px-4 py-2 font-mono">{money(r.precio)}</td>
                <td class="px-4 py-2 font-mono">{r.porcImpuesto}%</td>
                <td class="px-4 py-2 font-mono">{r.porcDescuento}%</td>
                <td class="px-4 py-2 text-right font-mono">{money(r.total)}</td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td colSpan={8} class="px-4 py-4 text-center text-gray-400 italic">
                  No hay productos en la factura.
                </td>
              </tr>
            )}
          </tbody>
          <tfoot class="bg-gray-800">
            {[
              ['Subtotal', money(totales.subtotal)],
              ['Impuestos', money(totales.impuestos)],
              ['Descuentos', `-${money(totales.descuentos).replace('$', '')}`],
              ['Total factura', money(totales.total)],
            ].map(([k, v]) => (
              <tr>
                <td
                  colSpan={7}
                  class="px-4 py-2 text-right font-medium text-white"
                >
                  {k}
                </td>
                <td class="px-4 py-2 text-right font-mono font-semibold text-white">
                  {v}
                </td>
              </tr>
            ))}
          </tfoot>
        </table>
      </div>

      {/* Pie */}
      <p class="mt-3 text-xs text-gray-400 italic">
        Documento de demostración (frontend). “Sello rojo” decorativo.
      </p>
    </section>
  );
}
