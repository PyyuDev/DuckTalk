# escucha_vosk.py
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time

model = Model("vosk-model-small-es-0.42")  # Asegurate de tener esta carpeta
rec = KaldiRecognizer(model, 16000)

def escuchar_voz(timeout_silencio=3):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()

    print("🎤 Habla. El sistema detectará silencio para terminar...\n")
    ultima_voz = time.time()
    texto_final = ""

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)

            if rec.AcceptWaveform(data):
                resultado = json.loads(rec.Result())
                texto = resultado.get("text", "").strip()
                if texto:
                    print("📝 Texto:", texto)
                    texto_final += " " + texto
                    ultima_voz = time.time()
            else:
                parcial = json.loads(rec.PartialResult()).get("partial", "").strip()
                if parcial:
                    ultima_voz = time.time()

            if time.time() - ultima_voz > timeout_silencio:
                print("\n🛑 Silencio detectado. Fin de la grabación.")
                break
    except KeyboardInterrupt:
        print("\n🛑 Interrumpido por el usuario.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    return texto_final.strip()
