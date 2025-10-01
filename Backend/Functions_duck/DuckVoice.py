import json
import wave
import os
from piper import PiperConfig, PiperVoice

MODEL_ONNX_PATH = os.path.join("models", "voice","model.onnx")

MODEL_JSON_PATH = os.path.join("models", "voice","model.onnx.json")

# Cargar configuración y modelo una sola vez
with open(MODEL_JSON_PATH, "r", encoding="utf-8") as f:
    config_dict = json.load(f)
config = PiperConfig.from_dict(config_dict)
voice = PiperVoice.load(
    MODEL_ONNX_PATH,
    MODEL_JSON_PATH,
    use_cuda=False
)

def hablar_como_pato(texto: str, archivo_salida="salida.wav"):
    """Genera un archivo de audio WAV con la voz del pato."""
    with wave.open(archivo_salida, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(config.sample_rate)
        voice.synthesize_wav(texto, wav_file)

    print(f"🗣️ Audio generado en '{archivo_salida}'")







