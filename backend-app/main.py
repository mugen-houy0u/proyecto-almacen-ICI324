from fastapi import FastAPI
from database import engine, Base
import models
from routers import empleados, clientes, lotes, proveedores, productos, reportes, ventas  

# -Crear tablas en SQLite si no existen aún -

Base.metadata.create_all(bind=engine)

# -Instancia principal de la aplicación FastAPI -

app = FastAPI()


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

# ======= DESPLIEGUE EN RAILWAY =======
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway asigna el puerto automáticamente
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)