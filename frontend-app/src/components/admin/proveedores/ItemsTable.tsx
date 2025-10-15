import type { Item, Totales } from './types';
import { money } from './money';
import type { JSX } from 'preact';

type Props = {
  items: Item[];
  totales: Totales;
  onAdd: () => void;
  onClear: () => void;
  onRemove: (id: number) => void;
  onChange: (id: number, patch: Partial<Item>) => void;
};

export default function ItemsTable({
  items,
  totales,
  onAdd,
  onClear,
  onRemove,
  onChange,
}: Props) {
  const onNum =
    (id: number, key: keyof Item) =>
    (e: JSX.TargetedEvent<HTMLInputElement, Event>) => {
      const v = parseFloat((e.currentTarget as HTMLInputElement).value || '0');
      onChange(id, { [key]: v } as Partial<Item>);
    };

  const onStr =
    (id: number, key: keyof Item) =>
    (e: JSX.TargetedEvent<HTMLInputElement, Event>) => {
      const v = (e.currentTarget as HTMLInputElement).value;
      onChange(id, { [key]: v } as Partial<Item>);
    };

  return (
    <section class="rounded-lg border border-gray-700 bg-gray-900 text-white">
      <div class="flex flex-wrap items-center gap-3 p-4">
        <button
          class="inline-flex items-center rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white hover:bg-gray-700"
          onClick={onAdd}
        >
          + Agregar producto
        </button>
        <button
          class="inline-flex items-center rounded-md border border-red-600 bg-transparent px-3 py-2 text-sm text-red-400 hover:bg-red-500/20"
          onClick={onClear}
        >
          Vaciar
        </button>
        <span class="text-sm text-gray-300">
          Campos: N°, Descripción, Cantidad, U.M, Precio, %Imp, %Desc
        </span>
      </div>

      <div class="overflow-auto">
        <table class="min-w-full divide-y divide-gray-700">
          <thead class="bg-gray-800">
            <tr>
              {[
                'N°',
                'Descripción',
                'Cantidad',
                'U.M',
                'Precio',
                '% Imp.',
                '% Desc.',
                'Total',
                '',
              ].map((h, i) => (
                <th
                  key={i}
                  class={`px-4 py-2 text-left text-xs font-semibold uppercase tracking-wide text-white ${
                    i === 8 ? 'w-12' : ''
                  }`}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-700 bg-gray-900">
            {items.map((r) => (
              <tr key={r.id}>
                <td class="px-4 py-2">
                  <input
                    class="w-20 rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="number"
                    min={1}
                    value={r.id}
                    onInput={onNum(r.id, 'id')}
                  />
                </td>
                <td class="px-4 py-2">
                  <input
                    class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="text"
                    value={r.descripcion}
                    onInput={onStr(r.id, 'descripcion')}
                    placeholder="Descripción"
                  />
                </td>
                <td class="px-4 py-2">
                  <input
                    class="w-28 rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="number"
                    min={0}
                    step="0.01"
                    value={r.cantidad}
                    onInput={onNum(r.id, 'cantidad')}
                  />
                </td>
                <td class="px-4 py-2">
                  <input
                    class="w-20 rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="text"
                    value={r.um}
                    onInput={onStr(r.id, 'um')}
                  />
                </td>
                <td class="px-4 py-2">
                  <input
                    class="w-32 rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="number"
                    min={0}
                    step="0.01"
                    value={r.precio}
                    onInput={onNum(r.id, 'precio')}
                  />
                </td>
                <td class="px-4 py-2">
                  <input
                    class="w-28 rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="number"
                    min={0}
                    max={100}
                    step="0.01"
                    value={r.porcImpuesto}
                    onInput={onNum(r.id, 'porcImpuesto')}
                  />
                </td>
                <td class="px-4 py-2">
                  <input
                    class="w-28 rounded-md border border-gray-700 bg-gray-800 text-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    type="number"
                    min={0}
                    max={100}
                    step="0.01"
                    value={r.porcDescuento}
                    onInput={onNum(r.id, 'porcDescuento')}
                  />
                </td>
                <td class="px-4 py-2 text-right font-mono">
                  {money(r.total)}
                </td>
                <td class="px-4 py-2 text-right">
                  <button
                    class="rounded-md border border-red-600 px-2 py-1 text-sm text-red-400 hover:bg-red-500/20"
                    onClick={() => onRemove(r.id)}
                  >
                    ✕
                  </button>
                </td>
              </tr>
            ))}
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
                <td />
              </tr>
            ))}
          </tfoot>
        </table>
      </div>
    </section>
  );
}
