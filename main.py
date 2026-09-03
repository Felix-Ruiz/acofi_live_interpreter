import os
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_REGION = os.getenv("AZURE_REGION", "")
APP_PASSWORD = os.getenv("APP_PASSWORD", "acofi2026") 

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    session_cookie = request.cookies.get("acofi_session")
    
    if session_cookie == APP_PASSWORD:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        html_content = html_content.replace("INYECCION_AZURE_KEY", AZURE_SPEECH_KEY)
        html_content = html_content.replace("INYECCION_AZURE_REGION", AZURE_REGION)
        return html_content
    else:
        with open("login.html", "r", encoding="utf-8") as f:
            return f.read()

@app.post("/login")
async def login(response: Response, password: str = Form(...)):
    if password == APP_PASSWORD:
        res = RedirectResponse(url="/", status_code=303)
        res.set_cookie(key="acofi_session", value=password, max_age=2592000, httponly=True)
        return res
    else:
        with open("login.html", "r", encoding="utf-8") as f:
            content = f.read().replace('id="error-msg" style="display: none;"', 'id="error-msg" style="display: block;"')
            return HTMLResponse(content)

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("manifest.json")

@app.get("/sw.js")
async def get_sw():
    return FileResponse("sw.js")

@app.get("/icon-192.png")
async def get_icon_192():
    return FileResponse("icon-192.png")

@app.get("/icon-512.png")
async def get_icon_512():
    return FileResponse("icon-512.png")