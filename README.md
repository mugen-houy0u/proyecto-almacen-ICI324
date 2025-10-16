# 📦 Proyecto de Gestión para Almacén **"El Vecino"**

Este es un proyecto **full-stack** que consiste en una plataforma web para la gestión de un almacén.  
La aplicación está diseñada para **modernizar y digitalizar los procesos clave** del negocio, como el control de inventario, la gestión de empleados y la generación de reportes.

---

## 🧩 Arquitectura del Proyecto

La solución se compone de dos partes principales:

- **Backend:** Construido con **FastAPI**, encargado de la lógica de negocio y la comunicación con la base de datos.  
- **Frontend:** Desarrollado con **Astro** y **Preact**, encargado de la interfaz visual y la interacción con el usuario.

---

## 🚀 Tecnologías Utilizadas

### 🖥️ Frontend
- **Astro:** Framework principal enfocado en el rendimiento al generar HTML estático y cargar JS solo donde es necesario.  
- **Preact:** Alternativa ligera a React, usada para componentes interactivos (islas de Astro).  
- **Tailwind CSS:** Framework CSS “utility-first” para un diseño rápido, moderno y consistente.  

### ⚙️ Backend
- **FastAPI:** Framework de alto rendimiento para construir APIs en Python.  
- **Python 3:** Lenguaje principal del backend.  
- **SQLAlchemy:** ORM para manejar la base de datos de forma segura y eficiente.  
- **SQLite:** Base de datos ligera para el almacenamiento de información.  
- **Uvicorn:** Servidor ASGI para ejecutar la aplicación FastAPI.  

---

## ✨ Funcionalidades Principales

El sistema cuenta con dos roles principales con permisos distintos:

### 👨‍💼 Administrador
- **Gestión de Operadores (Empleados):**
  - Visualizar lista completa de empleados.  
  - Agregar nuevos empleados.  
  - Editar información existente.  
  - Eliminar empleados.  
  - Ver detalles completos de cada empleado.  

- **Gestión de Proveedores:** *(Funcionalidad en desarrollo)*  
- **Generación de Reportes:** *(Funcionalidad en desarrollo)*  

### 👷 Operario / Cajero
- *(Vistas futuras a desarrollar)*  

---

## 🛠️ Instalación y Puesta en Marcha

Para ejecutar este proyecto localmente, debes abrir **dos terminales**:  
una para el backend y otra para el frontend.

---

### 1️⃣ Configuración del Backend (API)

#### ✅ Requisitos
- Python 3.x instalado

#### 🧭 Pasos

```bash
# Navega a la carpeta del backend
cd ruta/a/tu/backend-app

# Crea un entorno virtual (solo la primera vez)
python -m venv venv

# Activa el entorno virtual
# En Windows (Git Bash)
source venv/Scripts/activate
# En macOS/Linux
source venv/bin/activate

# Instala las dependencias
pip install fastapi "uvicorn[standard]" sqlalchemy

# Inicia el servidor del backend
uvicorn main:app --reload
