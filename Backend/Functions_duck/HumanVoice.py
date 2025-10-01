# stt_vosk.py
from vosk import Model, KaldiRecognizer
import wave
import subprocess
import os
import json


VOSK_MODEL_PATH = os.path.join( "models", "vosk-model-small-es-0.42")
# Cargar modelo solo una vez
model = Model(VOSK_MODEL_PATH)

def convertir_audio_a_texto(ruta_archivo: str) -> str:
    # Convertir a WAV si no está en ese formato
    if not ruta_archivo.endswith(".wav"):
        wav_path = "temp_input.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", ruta_archivo,
            "-ar", "16000", "-ac", "1", wav_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        wav_path = ruta_archivo

    # Procesar WAV
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    texto_final = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            resultado = json.loads(rec.Result())
            texto_final += " " + resultado.get("text", "")
    resultado = json.loads(rec.FinalResult())
    texto_final += " " + resultado.get("text", "")

    wf.close()
    return texto_final.strip()




