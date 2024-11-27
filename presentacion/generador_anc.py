from scipy.io.wavfile import write
import numpy as np

# Parametros de la señal de audio
sample_rate = 44100  # Frecuencia de muestreo en Hz
duration = 5         # Duración de la señal en segundos
frequency = 151.6    # Frecuencia de la onda (La4) en Hz

# Generamos la senal de audio (onda sinusoidal)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)  # Tiempo
signal = 0.5 * np.sin(2 * np.pi * frequency * t)                           # Amplitud normalizada
# signal = -0.5 * np.sin(2 * np.pi * frequency * t)                        # Amplitud normalizada

# Guardar la señal en un archivo .wav
write("./presentacion/senal_audio_directa.wav", sample_rate, np.int16(signal * 32767))  # Convertir a 16 bits
# write("senal_audio_inversa.wav", sample_rate, np.int16(signal * 32767))  # Convertir a 16 bits

print("Archivo guardado como 'senal_audio_directa/inversa.wav'")