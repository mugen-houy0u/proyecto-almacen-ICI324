Organización de frontend
src/
├── layouts/
│   ├── AdminLayout.astro
│   ├── OperadorLayout.astro
│   └── AuthLayout.astro          # opcional: para login
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   ├── SidebarAdmin.astro
│   ├── SidebarOperador.astro
│   ├── LoginForm.astro
│   └── forms/                    # subcarpeta opcional para formularios
│       ├── ProveedorForm.astro
│       └── OperadorForm.astro
└── pages/
    ├── index.astro               # redirección al login
    ├── login.astro
    ├── admin/
    │   ├── index.astro           # página de inicio admin
    │   ├── proveedores.astro     # registrar proveedores
    │   ├── operadores.astro      # añadir/editar operadores
    │   └── roles.astro           # editar roles de operadores
    └── operador/
        ├── index.astro           # inicio operador
        ├── ventas.astro
        ├── productos.astro
        ├── precios.astro
        ├── stock.astro
        └── reportes.astro

