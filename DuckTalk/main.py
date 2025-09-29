from fastapi import FastAPI, UploadFile, File,BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from Duck_action.HumanVoice import convertir_audio_a_texto
from Duck_action.DuckIA import iniciar_sesion,enviar_mensaje
from Duck_action.DuckVoice import hablar_como_pato
import logging
import time
import os
import asyncio
from fastapi.staticfiles import StaticFiles
from pathlib import Path
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import os
import signal

driver_global = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

respuesta_inicial_global = None

@app.get("/iniciar")
async def iniciar(background_tasks: BackgroundTasks):
    global driver_global, respuesta_inicial_global

    if driver_global is None:
        try:
            print("🔄 Inicializando sesión con Gemini...")
            driver_global, respuesta_inicial_global = iniciar_sesion()
            print("✅ Sesión iniciada con respuesta:", respuesta_inicial_global)

            # Generar el audio en segundo plano
            hablar_como_pato(respuesta_inicial_global, "salida.wav")

        except Exception as e:
            logger.exception("Error al iniciar sesión con Gemini")
            return {"error": str(e)}
    else:
        print("⚠️ Driver ya estaba iniciado. Reusando...")

    return FileResponse("salida.wav", media_type="audio/wav")



@app.post("/conversar")
async def conversar(audio: UploadFile = File(...)):
    global driver_global

    if driver_global is None:
        return {"error": "Primero debés iniciar la conversación con /iniciar"}

    with open("temp_input.webm", "wb") as f:
        f.write(await audio.read())

    texto_usuario = convertir_audio_a_texto("temp_input.webm")
    print("🎤 Usuario dijo:", texto_usuario)

    respuesta, driver_global = enviar_mensaje(texto_usuario, driver=driver_global)

    hablar_como_pato(respuesta, "salida.wav")

    return FileResponse("salida.wav", media_type="audio/wav")


@app.get("/cerrar")
async def cerrar_sesion():
    global driver_global
    print('aca estoy cerrando')
    if driver_global:
        try:
            print("🔻 Cerrando driver con .quit()")
            # Intenta cerrar como siempre
            driver_global.quit()
        except Exception as e:
            print("⚠️ Error al cerrar con quit():", e)

        try:
            # Forzar cierre del proceso si sigue vivo
            pid = driver_global.service.process.pid
            print(f"🔪 Matando proceso del driver (pid: {pid})")
            os.kill(pid, signal.SIGTERM)
        except Exception as e:
            print("⚠️ No se pudo matar el proceso:", e)

        driver_global = None
        print("✅ Driver cerrado completamente")
        return {"mensaje": "Driver cerrado completamente"}

    return {"mensaje": "Driver ya estaba cerrado"}


