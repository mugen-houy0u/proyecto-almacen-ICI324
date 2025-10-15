import { h } from 'preact';
import { useState } from 'preact/hooks';

export default function AgregarOperadorForm() {
  // Estados para cada campo del formulario
  const [nombre, setNombre] = useState('');
  const [rut, setRut] = useState('');
  const [telefono, setTelefono] = useState('');
  const [correo, setCorreo] = useState('');
  const [direccion, setDireccion] = useState('');
  const [fechaIngreso, setFechaIngreso] = useState('');
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  
  // Estado para manejar mensajes de respuesta (éxito o error)
  const [mensaje, setMensaje] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje('Enviando...');

    // URL del endpoint para crear cajeros en tu backend
    const url = 'http://127.0.0.1:8000/empleados/cajero';

    // Construimos los datos del formulario para la API
    const params = new URLSearchParams({
      nombre: nombre,
      rut_empleado: rut,
      telefono: telefono,
      correo: correo,
      direccion: direccion,
      fecha_de_ingreso: fechaIngreso,
      usuario: usuario,
      contrasena: contrasena,
    });

    try {
      const response = await fetch(`${url}?${params.toString()}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setMensaje(data.message || 'Operador agregado con éxito.');
        // Opcional: limpiar el formulario
        setNombre(''); setRut(''); setTelefono(''); setCorreo(''); setDireccion(''); setFechaIngreso(''); setUsuario(''); setContrasena('');
      } else {
        const errorData = await response.json();
        setMensaje(`Error: ${errorData.detail || 'No se pudo agregar el operador.'}`);
      }
    } catch (error) {
      setMensaje('Error de conexión con el servidor.');
      console.error('Error al agregar operador:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} class="w-full max-w-2xl mx-auto bg-white/80 p-8 rounded-xl shadow-lg space-y-4">
      {/* Fila para Nombre y RUT */}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="nombre" class="block text-sm font-medium text-gray-700">Nombre Completo</label>
          <input type="text" id="nombre" value={nombre} onInput={(e) => setNombre(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
        </div>
        <div>
          <label for="rut" class="block text-sm font-medium text-gray-700">RUT</label>
          <input type="text" id="rut" value={rut} onInput={(e) => setRut(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
        </div>
      </div>

      {/* Fila para Teléfono y Correo */}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="telefono" class="block text-sm font-medium text-gray-700">Teléfono</label>
          <input type="tel" id="telefono" value={telefono} onInput={(e) => setTelefono(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
        </div>
        <div>
          <label for="correo" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
          <input type="email" id="correo" value={correo} onInput={(e) => setCorreo(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
        </div>
      </div>
      
      {/* Fila para Dirección y Fecha de Ingreso */}
      <div>
        <label for="direccion" class="block text-sm font-medium text-gray-700">Dirección</label>
        <input type="text" id="direccion" value={direccion} onInput={(e) => setDireccion(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
      </div>
      <div>
        <label for="fechaIngreso" class="block text-sm font-medium text-gray-700">Fecha de Ingreso</label>
        <input type="date" id="fechaIngreso" value={fechaIngreso} onInput={(e) => setFechaIngreso(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
      </div>

      {/* Fila para Usuario y Contraseña */}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="usuario" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
          <input type="text" id="usuario" value={usuario} onInput={(e) => setUsuario(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
        </div>
        <div>
          <label for="contrasena" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input type="password" id="contrasena" value={contrasena} onInput={(e) => setContrasena(e.currentTarget.value)} required class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-black" />
        </div>
      </div>

      {/* Botón de envío y mensaje de estado */}
      <div class="pt-4 flex items-center justify-between">
        <button type="submit" class="px-6 py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition shadow-md">
          Agregar Operador
        </button>
        {mensaje && <p class="text-sm font-medium text-gray-800">{mensaje}</p>}
      </div>
    </form>
  );
}