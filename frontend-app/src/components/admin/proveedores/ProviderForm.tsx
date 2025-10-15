import type { Proveedor } from './types';
import { FORMA_PAGO, type FormaPago } from './types';

type Props = {
  value: Proveedor;
  onChange: (p: Proveedor) => void;
};

export default function ProviderForm({ value, onChange }: Props) {
  return (
    // ⬇️ Contenedor SIEMPRE oscuro
    <form class="rounded-lg border border-gray-700 bg-gray-900 text-white p-4">
      <h2 class="text-lg font-semibold mb-4">Datos del proveedor</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        {/* RUT */}
        <div>
          <label class="block text-sm font-medium text-white mb-1">RUT</label>
          <input
            type="text"
            value={value.rut}
            onInput={(e) =>
              onChange({ ...value, rut: (e.currentTarget as HTMLInputElement).value })
            }
            class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="76.667.791-6"
          />
        </div>

        {/* Nombre */}
        <div>
          <label class="block text-sm font-medium text-white mb-1">Nombre o Razón Social</label>
          <input
            type="text"
            value={value.nombre}
            onInput={(e) =>
              onChange({ ...value, nombre: (e.currentTarget as HTMLInputElement).value })
            }
            class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ej: WebFactura SPA"
          />
        </div>

        {/* Correo */}
        <div>
          <label class="block text-sm font-medium text-white mb-1">Correo electrónico</label>
          <input
            type="email"
            value={value.correo}
            onInput={(e) =>
              onChange({ ...value, correo: (e.currentTarget as HTMLInputElement).value })
            }
            class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="contacto@dominio.cl"
          />
        </div>

        {/* Giro */}
        <div>
          <label class="block text-sm font-medium text-white mb-1">Giro</label>
          <input
            type="text"
            value={value.giro}
            onInput={(e) =>
              onChange({ ...value, giro: (e.currentTarget as HTMLInputElement).value })
            }
            class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Comercio al por menor"
          />
        </div>

        {/* Fecha emisión */}
        <div>
          <label class="block text-sm font-medium text-white mb-1">Fecha de emisión</label>
          <input
            type="date"
            value={value.fechaEmision}
            onInput={(e) =>
              onChange({ ...value, fechaEmision: (e.currentTarget as HTMLInputElement).value })
            }
            class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Forma de pago */}
        <div>
          <label class="block text-sm font-medium text-white mb-1">Forma de pago</label>
          <select
            value={value.formaPago}
            onInput={(e) =>
              onChange({
                ...value,
                formaPago: (e.currentTarget as HTMLSelectElement).value as FormaPago,
              })
            }
            class="w-full rounded-md border border-gray-700 bg-gray-800 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {FORMA_PAGO.map((fp) => (
              <option class="bg-gray-800 text-white" value={fp}>{fp}</option>
            ))}
          </select>
        </div>
      </div>
    </form>
  );
}
