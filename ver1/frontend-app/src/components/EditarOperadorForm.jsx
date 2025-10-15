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
  const [errorDetail, setErrorDetail] = useState("");

  // ---------- carga inicial ----------
  useEffect(() => {
    let alive = true;
    async function fetchEmpleado() {
      try {
        const res = await fetch(`/api/empleados/${id}`);
        if (!res.ok) {
          const txt = await res.text();
          throw new Error(`GET /api/empleados/${id} → ${res.status} ${txt}`);
        }
        const data = await res.json();
        if (!alive) return;
        setFormData({
          rut: data.rut ?? "",
          nombre: data.nombre ?? "",
          // normaliza rol (por si backend valida Literals con mayúscula)
          rol: data.rol ?? "",
        });
      } catch (err) {
        console.error(err);
        setMessage("❌ No se pudo cargar el empleado.");
        setErrorDetail(String(err?.message ?? err));
      } finally {
        if (alive) setLoading(false);
      }
    }
    fetchEmpleado();
    return () => {
      alive = false;
    };
  }, [id]);

  // ---------- handlers ----------
  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage("");
    setErrorDetail("");

    try {
      // IMPORTANTE: incluir id en el body
      const res = await fetch(`/api/empleados/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: Number(id),
          // Si tu backend valida Literals exactos, usa capitalización:
          // administrador → Administrador, operador → Operador, supervisor → Supervisor
          ...formData,
          rol: capitalizaRol(formData.rol),
        }),
      });

      if (!res.ok) {
        // intenta leer JSON de error para ver el detalle REAL
        let detail = "";
        try {
          const errJson = await res.json();
          detail =
            errJson?.detail ||
            errJson?.error?.message ||
            JSON.stringify(errJson);
        } catch {
          detail = await res.text();
        }
        throw new Error(`PUT /api/empleados/${id} → ${res.status} ${detail}`);
      }

      // opcionalmente podrías usar el JSON devuelto para refrescar la UI
      await res.json().catch(() => null);
      setMessage("✅ Empleado actualizado correctamente");
    } catch (err) {
      console.error(err);
      setMessage("❌ Error al actualizar empleado.");
      setErrorDetail(String(err?.message ?? err));
    }
  }

  function capitalizaRol(rol) {
    if (!rol) return "";
    const map = {
      administrador: "Administrador",
      operador: "Operador",
      supervisor: "Supervisor",
    };
    // si ya viene capitalizado, respétalo; si viene en minúsculas, mapea
    return map[rol.toLowerCase()] ?? rol;
  }

  // ---------- render ----------
  if (loading)
    return (
      <div class="flex items-center justify-center min-h-screen bg-[url('/bg.jpg')] bg-cover">
        <p class="text-white text-lg">Cargando datos...</p>
      </div>
    );

  return (
    <div class="flex items-center justify-center min-h-screen bg-[url('/bg.jpg')] bg-cover">
      <form
        onSubmit={handleSubmit}
        class="flex flex-col gap-4 w-80 p-6 rounded-xl shadow-xl bg-white/20 backdrop-blur-lg border border-white/30"
      >
        <h2 class="text-2xl font-bold text-center text-black mb-2">
          Editar Empleado
        </h2>

        <div>
          <label class="block text-sm font-medium text-gray-900">RUT</label>
          <input
            name="rut"
            value={formData.rut}
            onInput={handleChange}
            class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-900">Nombre</label>
          <input
            name="nombre"
            value={formData.nombre}
            onInput={handleChange}
            class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-900">Rol</label>
          <select
            name="rol"
            value={formData.rol}
            onInput={handleChange}
            class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            required
          >
            <option value="" disabled>Seleccionar rol</option>
            {/* usa valores capitalizados para evitar choque con Literals */}
            <option value="Administrador">Administrador</option>
            <option value="Operador">Operador</option>
            <option value="Supervisor">Supervisor</option>
          </select>
        </div>

        <button
          type="submit"
          class="w-full bg-black text-white font-semibold py-2 rounded-lg hover:bg-gray-800 transition"
        >
          Guardar cambios
        </button>

        {message && <p class="text-center text-sm text-black mt-2">{message}</p>}
        {errorDetail && (
          <pre class="text-xs text-red-700 bg-white/70 p-2 rounded mt-1 whitespace-pre-wrap">
            {errorDetail}
          </pre>
        )}
      </form>
    </div>
  );
}

