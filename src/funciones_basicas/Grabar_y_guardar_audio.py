#pip install scipy sounddevice keyboard numpy

import scipy.io.wavfile as wav
import sounddevice as sd
import sys
import keyboard
import numpy as np

def grabar_audio(device_index : int, frecuencia_muestreo = 44100):
    # Frecuencia de muestreo
    print("Pulsa la tecla 'espacio' para detener la grabación.")

    # Lista para almacenar los fragmentos de voz grabados
    audio_grabado = []

    # Función de callback para grabar voz
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_grabado.append(indata.copy())  # Agregar el fragmento grabado a la lista

    # Iniciar la grabación
    with sd.InputStream(samplerate=frecuencia_muestreo, channels=1, dtype='int16', callback=callback, device=device_index):
        keyboard.wait('space', suppress=True)  # Esperar a que se suelte la tecla 'espacio'

    # Convertir la lista de fragmentos a un arreglo numpy
    audio_grabado = np.concatenate(audio_grabado, axis=0)
    print("Grabación finalizada.\n")
    return audio_grabado


# Parámetros de grabación
frecuencia_muestreo = 48000  # Tasa de muestreo
device_index = 8 # Para ver los indices print(sd.query_devices()) y buscar 2 in 0 out

# Grabar el audio
voz = grabar_audio(device_index, frecuencia_muestreo)

#Guardar en disco duro la pregunta realizada.
wav.write('./src/tareas/voz_para_fft.wav', frecuencia_muestreo, voz)
