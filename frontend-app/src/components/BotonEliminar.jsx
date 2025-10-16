import { h } from 'preact';
import { useState } from 'preact/hooks';

// Este componente solo necesita el ID del operador para funcionar
export default function BotonEliminar({ operadorId }) {
  const [eliminando, setEliminando] = useState(false);

  const handleEliminar = async () => {
    // 1. Pedimos confirmación al usuario
    if (!confirm("¿Estás seguro de que deseas eliminar a este operador?")) {
      return;
    }

    setEliminando(true);

    try {
      // 2. Hacemos la llamada DELETE al backend
      const res = await fetch(`http://127.0.0.1:8000/empleados/${operadorId}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        // 3. Si se elimina con éxito, recargamos la página para ver la lista actualizada
        alert("Operador eliminado con éxito.");
        window.location.reload(); // Recarga la página
      } else {
        const errorData = await res.json();
        throw new Error(errorData.detail || "No se pudo eliminar el operador.");
      }
    } catch (error) {
      console.error(error);
      alert(`Error al eliminar: ${error.message}`);
    } finally {
      setEliminando(false);
    }
  };

  return (
    <button
      onClick={handleEliminar}
      disabled={eliminando}
      type="button"
      class={`px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition text-sm font-medium ${eliminando ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {eliminando ? 'Eliminando...' : 'Eliminar'}
    </button>
  );
}