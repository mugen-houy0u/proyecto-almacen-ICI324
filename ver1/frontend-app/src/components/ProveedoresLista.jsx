// src/components/ProveedoresLista.jsx
import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';

// Componente principal que maneja la lógica de la lista de proveedores
export default function ProveedoresLista() {
  // --- ESTADOS ---
  const [proveedores, setProveedores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false); // Estado para mostrar/ocultar el formulario

  // Estado para los campos del nuevo proveedor
  const [newProviderData, setNewProviderData] = useState({
    nombre_empresa: '',
    correo: '',
    telefono: '',
    direccion: '',
  });

  // --- EFECTOS ---
  // Carga inicial de los proveedores desde el backend
  useEffect(() => {
    const fetchProveedores = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/proveedores/');
        if (!response.ok) {
          throw new Error('No se pudo obtener la lista de proveedores.');
        }
        const data = await response.json();
        setProveedores(data);
      } catch (err) {
        console.error(err);
        setError('Error al cargar los proveedores. Revisa la conexión con el backend.');
      } finally {
        setLoading(false);
      }
    };
    fetchProveedores();
  }, []);

  // --- MANEJADORES DE EVENTOS ---

  // Maneja la eliminación de un proveedor
  const handleEliminar = async (idProveedor) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar este proveedor?')) {
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/proveedores/${idProveedor}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Error al eliminar el proveedor.');
      }
      
      setProveedores(proveedores.filter(p => p.id_proveedor !== idProveedor));
      alert('Proveedor eliminado con éxito.');

    } catch (err) {
      console.error(err);
      alert('No se pudo eliminar el proveedor.');
    }
  };
  
  // Maneja los cambios en los inputs del formulario
  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setNewProviderData(prevData => ({ ...prevData, [name]: value }));
  };

  // Maneja el envío del formulario para agregar un nuevo proveedor
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    // ID del empleado administrador que registra. Según tu dump, es el 3.
    const idAdmin = 3; 

    // CORREGIDO: Construimos los parámetros para la URL, como lo espera el backend
    const params = new URLSearchParams({
        id_empleado: idAdmin,
        correo: newProviderData.correo,
        telefono: newProviderData.telefono,
        direccion: newProviderData.direccion,
        nombre_empresa: newProviderData.nombre_empresa
    });

    try {
      const response = await fetch(`http://127.0.0.1:8000/proveedores/?${params.toString()}`, {
        method: 'POST',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'No se pudo agregar el proveedor.');
      }
      
      const nuevoProveedorResponse = await response.json();
      
      // Actualiza la lista en el frontend con el nuevo proveedor
      setProveedores([...proveedores, nuevoProveedorResponse.proveedor]);
      setShowForm(false); // Oculta el formulario
      setNewProviderData({ nombre_empresa: '', correo: '', telefono: '', direccion: '' }); // Limpia el formulario
      alert(nuevoProveedorResponse.msg);

    } catch (err) {
      console.error(err);
      alert(`Error al agregar el proveedor: ${err.message}`);
    }
  };

  // --- RENDERIZADO ---
  if (loading) return <p class="text-white text-center">Cargando proveedores...</p>;
  if (error) return <p class="text-red-400 text-center">{error}</p>;

  return (
    <section class="w-full max-w-5xl mx-auto p-8 bg-white/30 backdrop-blur-md border border-white/40 rounded-2xl shadow-xl">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-bold text-white">Gestión de Proveedores</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          class="px-5 py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition shadow-md"
        >
          {showForm ? 'Cancelar' : 'Agregar Proveedor'}
        </button>
      </div>
      
      {showForm && (
        <div class="mb-8 p-6 bg-white/50 rounded-xl shadow-md transition-all duration-300">
          <form onSubmit={handleFormSubmit} class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <h3 class="md:col-span-2 text-xl font-semibold text-gray-800 mb-2">Nuevo Proveedor</h3>
            <input name="nombre_empresa" value={newProviderData.nombre_empresa} onInput={handleFormChange} placeholder="Nombre de la empresa" required class="p-2 rounded border" />
            <input name="correo" type="email" value={newProviderData.correo} onInput={handleFormChange} placeholder="Correo" required class="p-2 rounded border" />
            <input name="telefono" value={newProviderData.telefono} onInput={handleFormChange} placeholder="Teléfono" required class="p-2 rounded border" />
            <input name="direccion" value={newProviderData.direccion} onInput={handleFormChange} placeholder="Dirección" required class="p-2 rounded border" />
            <button type="submit" class="md:col-span-2 py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Guardar Proveedor</button>
          </form>
        </div>
      )}

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {proveedores.map(prov => (
          <div key={prov.id_proveedor} class="bg-white/80 rounded-xl p-4 flex flex-col items-center text-center shadow-md">
            <img src="/default-provider.png" alt={prov.nombre_empresa} class="w-24 h-24 object-cover rounded-full mb-3 border-2 border-white" />
            <h3 class="font-semibold text-lg text-gray-900">{prov.nombre_empresa}</h3>
            <p class="text-gray-700 text-sm">{prov.correo}</p>
            <p class="text-gray-500 text-xs">Tel: {prov.telefono}</p>
            <div class="flex flex-wrap justify-center items-center gap-2 mt-4">
              {/* CORREGIDO: Enlaces a futuras páginas dinámicas */}
              <a href={`/admin/proveedores/${prov.id_proveedor}/editar`} class="px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition text-sm font-medium">Modificar</a>
              <a href={`/admin/proveedores/${prov.id_proveedor}/detalles`} class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-medium">Detalles</a>
              <button onClick={() => handleEliminar(prov.id_proveedor)} class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition text-sm font-medium">Eliminar</button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
