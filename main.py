import os
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_REGION = os.getenv("AZURE_REGION", "")
# Nueva variable de entorno para la contraseña maestra (Cámbiala en Vercel)
APP_PASSWORD = os.getenv("APP_PASSWORD", "acofi2026") 

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    # Barrera de Seguridad Server-Side
    session_cookie = request.cookies.get("acofi_session")
    
    if session_cookie == APP_PASSWORD:
        # Autenticado: Entregamos el código protegido y las llaves
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        html_content = html_content.replace("INYECCION_AZURE_KEY", AZURE_SPEECH_KEY)
        html_content = html_content.replace("INYECCION_AZURE_REGION", AZURE_REGION)
        return html_content
    else:
        # No autenticado: Entregamos la pantalla de Login y el Pop-up de instalación
        with open("login.html", "r", encoding="utf-8") as f:
            return f.read()

@app.post("/login")
async def login(response: Response, password: str = Form(...)):
    if password == APP_PASSWORD:
        # Configurar cookie de seguridad encriptada (Dura 30 días)
        res = RedirectResponse(url="/", status_code=303)
        res.set_cookie(key="acofi_session", value=password, max_age=2592000, httponly=True)
        return res
    else:
        # Contraseña incorrecta
        with open("login.html", "r", encoding="utf-8") as f:
            content = f.read().replace('id="error-msg" style="display: none;"', 'id="error-msg" style="display: block;"')
            return HTMLResponse(content)

# Rutas vitales para habilitar la instalación como App (PWA)
@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("manifest.json")

@app.get("/sw.js")
async def get_sw():
    return FileResponse("sw.js")