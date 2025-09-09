from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef home():\n    return {'msg': 'Hola desde FastAPI'}
