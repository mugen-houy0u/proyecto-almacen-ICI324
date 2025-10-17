import { h } from 'preact';
import { useState } from 'preact/hooks';

// Componente principal que ahora maneja el filtrado de ventas por fecha
export default function ReportesManager() {
  // Estado para el filtro por fecha. Se inicializa con la fecha de hoy.
  const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]);
  const [reporteData, setReporteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFiltrarPorFecha = async (e) => {
    e.preventDefault();
    if (!fecha) {
      setError('Por favor, selecciona una fecha.');
      return;
    }
    setLoading(true);
    setError('');
    setReporteData(null);

    try {
      const url = `http://127.0.0.1:8000/ventas/ventas/por-fecha?fecha=${fecha}`;
      console.log("URL solicitada desde el frontend:", url);

      const response = await fetch(url);
      
      if (response.status === 404) {
        setError(`No se encontraron ventas para la fecha ${fecha}.`);
        setReporteData({ ventas: [] });
      } else if (!response.ok) {
        throw new Error(`Error al obtener las ventas: ${response.statusText}`);
      } else {
        const data = await response.json();
        setReporteData(data);
      }
    } catch (err) {
      console.error(err);
      setError('No se pudo obtener el reporte. Revisa la conexión con el backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="w-full max-w-5xl mx-auto p-8 bg-white/30 backdrop-blur-md border border-white/40 rounded-2xl shadow-xl">
      {/* Formulario para seleccionar la fecha */}
      <form onSubmit={handleFiltrarPorFecha} class="flex flex-col sm:flex-row items-center gap-4 mb-8">
        <div class="w-full sm:w-auto sm:flex-grow">
          <label for="fecha_reporte" class="sr-only">Seleccionar Fecha</label>
          {/* 👇 CORREGIDO: Se vuelve a usar el input de tipo "date" para el calendario */}
          <input
            id="fecha_reporte"
            type="date"
            value={fecha}
            onInput={(e) => setFecha(e.currentTarget.value)}
            class="w-full px-4 py-3 bg-white/80 text-black rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-black"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          class="w-full sm:w-auto px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition shadow-md disabled:bg-gray-400"
        >
          {loading ? 'Buscando...' : 'Mostrar Ventas del Día'}
        </button>
      </form>

      {/* Sección de resultados */}
      <div class="mt-8">
        {error && <p class="text-center text-red-800 bg-red-200 p-3 rounded-lg">{error}</p>}
        {reporteData && <TablaResultados data={reporteData} />}
      </div>
    </div>
  );
}

// Componente para renderizar la tabla de resultados
function TablaResultados({ data }) {
  const { ventas, total_dia } = data;
  if (!ventas || (ventas.length === 0 && total_dia === null)) return null;
  return (
    <div class="overflow-x-auto bg-white/80 rounded-xl shadow-md">
      <table class="min-w-full text-left">
        <thead class="bg-gray-200">
          <tr>
            <th class="p-3 font-semibold text-gray-700">ID Venta</th>
            <th class="p-3 font-semibold text-gray-700">RUT Cliente</th>
            <th class="p-3 font-semibold text-gray-700">ID Empleado</th>
            <th class="p-3 font-semibold text-gray-700">Método de Pago</th>
            <th class="p-3 font-semibold text-gray-700 text-right">Monto Total</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          {ventas.map(venta => (
            <tr key={venta.id_venta}>
              <td class="p-3">{venta.id_venta}</td>
              <td class="p-3">{venta.rut_cliente}</td>
              <td class="p-3 text-center">{venta.id_empleado}</td>
              <td class="p-3">{venta.metodo_de_pago}</td>
              <td class="p-3 text-right">{formatCurrency(venta.total_venta)}</td>
            </tr>
          ))}
        </tbody>
        <tfoot class="bg-gray-200">
            <tr>
                <td colspan="4" class="p-3 text-right font-bold text-lg text-gray-800">Total del Día:</td>
                <td class="p-3 text-right font-bold text-lg text-gray-800">{formatCurrency(total_dia)}</td>
            </tr>
        </tfoot>
      </table>
    </div>
  );
}

// Función de utilidad para formatear moneda
function formatCurrency(value) {
  if (value === null || value === undefined) return '$0';
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(value);
}