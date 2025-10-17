# 🧩 Mañas de este proyecto

1. Todos los "componentes.py" del backend se encuentran en la carpeta de routers, por lo tanto al llamarlo desde frontend algunas rutas se repiten o son extrañas, como esta:
```bash
https://just-creation-production-cae2.up.railway.app/ventas/ventas/por-fecha?fecha=2023-01-01
```
Cuando normalmente debería ser:
```bash
http://127.0.0.1:8000/ventas/por-fecha?fecha=2023-01-01
```
2. La sección de "factura.astro" funciona de manera irregular, solamente es un único archivo que esta encargado de exportar el formulario a PDF, de manera extraña al añadirle un layout común como "AdminLayout.astro" el componente de "html2pdf.js" no funciona correctamente, carga infinitamente
---
```bash
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣋⣉⡛⠻⢉⣤⣤⣬⣉⠛⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⠙⠀⠀⢹⡇⠀⠀⢠⣿⡟⢨⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⢁⣾⣿⣶⣶⣤⡌⠛⠁⠔⠦⠤⠴⢒⣿⣿⣷⡌⢻⣿⣿⣿⣿
⣿⣿⡄⢻⣿⣿⣿⣿⣿⣶⡆⢸⣿⣿⣿⣿⣿⣿⠂⣾⣿⣿⣿⡇⢸⠃⣼⣿
⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⡇⠈⣴⣶⣦⡈⢻⠃⣼⣿⣿⣿⣿⣿⢠⣿⣿⣿
⣿⣿⣿⣿⣧⠘⢿⣿⣿⣿⣿⡄⠸⡿⠛⠛⢠⣿⣿⣿⣿⣿⠏⣰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣤⣉⠛⢿⣿⣿⠿⡿⠿⠿⠛⢋⣤⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠛⢃⣄⠒⢂⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```
