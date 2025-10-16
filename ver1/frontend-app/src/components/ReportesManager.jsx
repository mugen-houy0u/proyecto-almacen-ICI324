// src/components/ReportesManager.jsx
import { h } from 'preact';
import { useState } from 'preact/hooks';

// Componente principal que maneja la lógica de los reportes
export default function ReportesManager() {
  const [tipoReporte, setTipoReporte] = useState('ventas-por-empleado');
  const [reporteData, setReporteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Función que se ejecuta al enviar el formulario
  const handleGenerarReporte = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setReporteData(null);

    try {
      const response = await fetch(`http://127.0.0.1:8000/reportes/${tipoReporte}`);
      if (!response.ok) {
        throw new Error(`Error al obtener el reporte: ${response.statusText}`);
      }
      const data = await response.json();
      
      // 👇 ¡AÑADIDO PARA DEPURACIÓN! 👇
      // Esto te mostrará en la consola del navegador la estructura de datos real.
      console.log('Datos recibidos del backend:', data);

      setReporteData(data);
    } catch (err) {
      console.error(err);
      setError('No se pudo generar el reporte. Revisa la conexión con el backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="w-full max-w-5xl mx-auto p-8 bg-white/30 backdrop-blur-md border border-white/40 rounded-2xl shadow-xl">
      {/* Formulario para seleccionar el tipo de reporte */}
      <form onSubmit={handleGenerarReporte} class="flex flex-col sm:flex-row items-center gap-4 mb-8">
        <div class="w-full sm:w-auto sm:flex-grow">
          <label for="tipo_reporte" class="sr-only">Tipo de Reporte</label>
          <select
            id="tipo_reporte"
            value={tipoReporte}
            onChange={(e) => setTipoReporte(e.currentTarget.value)}
            class="w-full px-4 py-3 bg-white/80 text-black rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-black"
          >
            <option value="ventas-por-empleado">Ventas por Empleado</option>
            <option value="ventas-por-cliente">Ventas por Cliente</option>
            <option value="ventas-por-producto">Ventas por Producto</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          class="w-full sm:w-auto px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition shadow-md disabled:bg-gray-400"
        >
          {loading ? 'Generando...' : 'Generar Reporte'}
        </button>
      </form>

      {/* Sección de resultados */}
      <div>
        {error && <p class="text-center text-red-800 bg-red-200 p-3 rounded-lg">{error}</p>}
        {reporteData && <TablaResultados tipo={tipoReporte} data={reporteData} />}
      </div>
    </div>
  );
}

// Componente para renderizar la tabla de resultados dinámicamente
function TablaResultados({ tipo, data }) {
  if (!data || data.length === 0) {
    return <p class="text-center text-white">No hay datos para mostrar en este reporte.</p>;
  }

  // Define las cabeceras y las celdas según el tipo de reporte
  let headers = [];
  let rows = [];

  switch (tipo) {
    case 'ventas-por-empleado':
      headers = ['Empleado', 'Cantidad de Ventas', 'Monto Total Vendido'];
      rows = data.map(item => (
        <tr key={item.id_empleado}>
          <td class="p-3">{item.nombre_empleado}</td>
          <td class="p-3 text-center">{item.cantidad_ventas}</td>
          <td class="p-3 text-right">{formatCurrency(item.monto_total_vendido)}</td>
        </tr>
      ));
      break;
    case 'ventas-por-cliente':
      headers = ['Cliente', 'RUT', 'Cantidad de Compras', 'Monto Total Gastado'];
      rows = data.map(item => (
        <tr key={item.rut_cliente}>
          <td class="p-3">{item.nombre_cliente}</td>
          <td class="p-3">{item.rut_cliente}</td>
          <td class="p-3 text-center">{item.cantidad_compras}</td>
          <td class="p-3 text-right">{formatCurrency(item.monto_total_gastado)}</td>
        </tr>
      ));
      break;
    case 'ventas-por-producto':
      headers = ['Producto (SKU)', 'Cantidad Vendida', 'Monto Total Generado'];
      rows = data.map(item => (
        <tr key={item.sku}>
          <td class="p-3">{item.nombre_producto} ({item.sku})</td>
          <td class="p-3 text-center">{item.cantidad_total_vendida}</td>
          <td class="p-3 text-right">{formatCurrency(item.monto_total_generado)}</td>
        </tr>
      ));
      break;
    default:
      return null;
  }

  return (
    <div class="overflow-x-auto bg-white/80 rounded-xl shadow-md">
      <table class="min-w-full text-left">
        <thead class="bg-gray-200">
          <tr>
            {headers.map(header => <th key={header} class="p-3 font-semibold text-gray-700">{header}</th>)}
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          {rows}
        </tbody>
      </table>
    </div>
  );
}

// Función de utilidad para formatear a CLP
function formatCurrency(value) {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
  }).format(value);
}