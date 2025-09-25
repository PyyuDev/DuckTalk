import json
import wave
import simpleaudio  # para reproducir audio
from piper import PiperConfig, PiperVoice

# Cargar configuración y modelo una sola vez
with open("./voice/model4.onnx.json", "r", encoding="utf-8") as f:
    config_dict = json.load(f)
config = PiperConfig.from_dict(config_dict)
voice = PiperVoice.load("./voice/model4.onnx")

def hablar_como_pato(texto: str):
    """Genera un archivo de audio con la voz del pato y lo reproduce."""
    with wave.open("salida.wav", "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(config.sample_rate)
        voice.synthesize_wav(texto, wav_file)

    # Reproducir el audio
    wave_obj = simpleaudio.WaveObject.from_wave_file("salida.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

    print("🗣️ El pato habló.")






