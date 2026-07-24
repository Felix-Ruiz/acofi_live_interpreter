import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Esto lee explícitamente el archivo .env ubicado en tu carpeta local
load_dotenv()

app = FastAPI()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_REGION = os.getenv("AZURE_REGION", "")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
        
    html_content = html_content.replace("INYECCION_AZURE_KEY", AZURE_SPEECH_KEY)
    html_content = html_content.replace("INYECCION_AZURE_REGION", AZURE_REGION)
    
    return html_content