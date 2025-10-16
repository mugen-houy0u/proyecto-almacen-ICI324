from fastapi import FastAPI
from database import engine, Base
import models
from routers import empleados, clientes, lotes, proveedores, productos, reportes, ventas, facturas
from fastapi.middleware.cors import CORSMiddleware 

# -Crear tablas en SQLite si no existen aún -

Base.metadata.create_all(bind=engine)

# -Instancia principal de la aplicación FastAPI -

app = FastAPI(title="El vecino-Backend")

# Lista de orígenes permitidos (dominios desde los cuales se pueden hacer solicitudes al backend)
origins = [
    "http://localhost:4321",  # Dirección y puerto donde corre Astro (modo desarrollo)
    "http://127.0.0.1:4321",  # Variante local alternativa para el mismo entorno
]

# Se agrega el middleware CORS a la aplicación FastAPI
# Esto habilita las políticas de intercambio de recursos entre dominios
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Define qué dominios pueden acceder al backend
    allow_credentials=True,        # Permite el uso de cookies, cabeceras de autenticación, etc.
    allow_methods=["*"],           # Autoriza todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Permite todos los tipos de cabeceras (headers) en las peticiones
)


# -Endpoint raíz para ver el estado del servicio-

@app.get("/")
def root():
    return {
        "title": "📦 Backend del Almacén del Vecino 🛒",
        "message": "Bienvenido al sistema que mueve nuestro almacén con FastAPI 🚀",
        "features": [
            "✅ Gestión de empleados",
            "✅ Control de inventario",
            "✅ Registro de clientes",
            "✅ Ventas y reportes en tiempo real"
        ],
        "status": "🟢 API corriendo sin problemas"
    }

# -Registro de routers (módulos de endpoints por recurso)-

app.include_router(empleados.router)
app.include_router(clientes.router)
app.include_router(lotes.router)
app.include_router(proveedores.router)
app.include_router(productos.router)
app.include_router(reportes.router)
app.include_router(ventas.router)
app.include_router(facturas.router)

# ======= DESPLIEGUE EN RAILWAY =======
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway asigna el puerto automáticamente
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)