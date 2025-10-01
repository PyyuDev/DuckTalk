import json
import wave
from piper import PiperConfig, PiperVoice

# Cargar configuración y modelo una sola vez
with open("/home/cristian/Desktop/testDuck/Backend/models/voice/model.onnx.json", "r", encoding="utf-8") as f:
    config_dict = json.load(f)
config = PiperConfig.from_dict(config_dict)
voice = PiperVoice.load(
    "/home/cristian/Desktop/testDuck/Backend/models/voice/model.onnx",
    "/home/cristian/Desktop/testDuck/Backend/models/voice/model.onnx.json",
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







