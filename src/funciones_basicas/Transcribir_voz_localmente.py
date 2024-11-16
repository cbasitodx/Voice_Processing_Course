#pip install vosk numpy scipy

import wave
import json
from vosk import Model, KaldiRecognizer
import numpy as np
from scipy.io.wavfile import write
import scipy.io.wavfile as wav

####################################################################################################################################
######### DESCARGAR Y DESCOMPRIME MODELO DE ESTE ENLACE: https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip ##########
####################################################################################################################################

# Convierte audio a 16,000 Hz para mejor compatibilidad
def convertir_frecuencia(archivo_audio, frecuencia_deseada=16000):
    frecuencia_original, data = wav.read(archivo_audio)
    if frecuencia_original != frecuencia_deseada:
        # Cambiar frecuencia de muestreo usando scipy
        data = np.interp(
            np.linspace(0, len(data), int(len(data) * frecuencia_deseada / frecuencia_original)),
            np.arange(len(data)),
            data
        ).astype(np.int16)
        nuevo_archivo = "audio_convertido.wav"
        write(nuevo_archivo, frecuencia_deseada, data)
        return nuevo_archivo
    return archivo_audio

# Función para transcribir el audio usando VOSK
def transcribir_voz_vosk(archivo_audio):
    archivo_audio = convertir_frecuencia(archivo_audio)

    # Cargar el modelo de VOSK para español
    # Asegúrate de especificar la ruta donde descargaste el modelo de español
    model = Model("./vosk-model-small-es-0.42")
    with wave.open(archivo_audio, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("El archivo de audio debe estar en mono y 16,000 Hz de frecuencia.")

        rec = KaldiRecognizer(model, wf.getframerate())
        texto_transcrito = ""

        while True:
            datos = wf.readframes(2000)  # Procesa en bloques de 2000 bytes
            if len(datos) == 0:
                break
            if rec.AcceptWaveform(datos):
                resultado = json.loads(rec.Result())
                texto_transcrito += resultado.get("text", "") + " "
            else:
                resultado_parcial = json.loads(rec.PartialResult())
                texto_transcrito += resultado_parcial.get("partial", "") + " "

        resultado_final = json.loads(rec.FinalResult())
        texto_transcrito = resultado_final.get("text", "")
        return texto_transcrito.strip()

# Llama a la función con el archivo de audio
texto = transcribir_voz_vosk('./src/funciones_basicas/hombre.wav')
print("Transcripción: " + texto)
