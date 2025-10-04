# 🧩 Estructura del Frontend

Este proyecto utiliza **Astro + Preact + TailwindCSS** para la construcción del frontend.  
A continuación se muestra la organización general de los archivos dentro del directorio `src/`.

---

## 📁 Estructura de carpetas

```bash
src/
├── layouts/
│   ├── AdminLayout.astro
│   ├── OperadorLayout.astro
│   └── AuthLayout.astro          # (opcional) diseño para la vista de login
│
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   ├── SidebarAdmin.astro
│   ├── SidebarOperador.astro
│   ├── LoginForm.astro
│   └── forms/                    # subcarpeta opcional para formularios
│       ├── ProveedorForm.astro
│       └── OperadorForm.astro
│
└── pages/
    ├── index.astro               # redirección o portada inicial
    ├── login.astro               # vista de inicio de sesión
    │
    ├── admin/                    # secciones del rol administrador
    │   ├── index.astro           # página principal de administrador
    │   ├── proveedores.astro     # registro y gestión de proveedores
    │   ├── operadores.astro      # añadir / editar operadores
    │   └── roles.astro           # asignación de roles
    │
    └── operador/                 # secciones del rol operador
        ├── index.astro           # página principal del operador
        ├── ventas.astro
        ├── productos.astro
        ├── precios.astro
        ├── stock.astro
        └── reportes.astro

