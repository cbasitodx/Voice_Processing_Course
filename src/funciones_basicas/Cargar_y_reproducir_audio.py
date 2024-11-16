#pip install scipy sounddevice

import scipy.io.wavfile as wav
import sounddevice as sd

#Cargar audio con frecuencia de muestreo.
frecuencia_muestreo, señal = wav.read('./src/audio_grabado.wav')

#Reproducir audio.
sd.play(señal, frecuencia_muestreo)
sd.wait()
