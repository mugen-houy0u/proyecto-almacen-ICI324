// src/components/EditarOperadorForm.jsx
import { useState, useEffect } from "preact/hooks";

export default function EditarOperadorForm({ id }) {
  const [formData, setFormData] = useState({
    rut: "",
    nombre: "",
    rol: "",
  });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  /* ---------- carga inicial ---------- */
  useEffect(() => {
    async function fetchOperador() {
      try {
        const res = await fetch(`http://localhost:4321/api/operadores/${id}`);
        if (!res.ok) throw new Error("Error al cargar operador");
        const data = await res.json();
        setFormData({
          rut: data.rut || "",
          nombre: data.nombre || "",
          rol: data.rol || "",
        });
      } catch (err) {
        console.error(err);
        setMessage("No se pudo cargar el operador.");
      } finally {
        setLoading(false);
      }
    }
    fetchOperador();
  }, [id]);

  /* ---------- handlers ---------- */
  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage("");
    try {
      const res = await fetch(`http://localhost:3000/api/operadores/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("Error al guardar cambios");
      setMessage("Operador actualizado correctamente ✅");
    } catch (err) {
      console.error(err);
      setMessage("❌ Error al actualizar operador.");
    }
  }

  /* ---------- render ---------- */
  if (loading)
    return (
      <div class="flex items-center justify-center min-h-screen bg-[url('/bg.jpg')] bg-cover">
        <p class="text-white text-lg">Cargando datos...</p>
      </div>
    );

  return (
    <div class="flex items-center justify-center min-h-screen bg-[url('/bg.jpg')] bg-cover">
      {/* ¡Contenedor grande ELIMINADO! */}
      <form
        onSubmit={handleSubmit}
        class="flex flex-col gap-4 w-80 p-6 rounded-xl shadow-xl bg-white/20 backdrop-blur-lg border border-white/30"
      >
        <h2 class="text-2xl font-bold text-center text-black mb-2">
          Editar Operador
        </h2>

        <div>
          <label class="block text-sm font-medium text-gray-900">RUT</label>
          <input
            name="rut"
            value={formData.rut}
            onChange={handleChange}
            class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-900">Nombre</label>
          <input
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-900">Rol</label>
          <select
            name="rol"
            value={formData.rol}
            onChange={handleChange}
            class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            required
          >
            <option value="" disabled>Seleccionar rol</option>
            <option value="administrador">Administrador</option>
            <option value="operador">Operador</option>
            <option value="supervisor">Supervisor</option>
          </select>
        </div>

        <button
          type="submit"
          class="w-full bg-black text-white font-semibold py-2 rounded-lg hover:bg-gray-800 transition"
        >
          Guardar cambios
        </button>

        {message && (
          <p class="text-center text-sm text-black mt-2">{message}</p>
        )}
      </form>
    </div>
  );
}