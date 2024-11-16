#pip install numpy sounddevice

import numpy as np
import sounddevice as sd

# Parámetros
frecuencia = 440  # Frecuencia en Hz
duracion = 2.0    # Duración en segundos
frecuencia_muestreo = 44100  # Frecuencia de muestreo en Hz (FRECUENCIA DE MUESTREO ESTANDAR)
volumen = 0.3 # entre 0 y 1

# Generación de la señal senoidal
# Tiempo de cada muestra
t = np.linspace(0, duracion, int(frecuencia_muestreo * duracion), endpoint=False)
# valor de la señal en cada muestra
onda_seno = volumen * np.sin(2 * np.pi * frecuencia * t)

# Reproducción de la onda
sd.play(onda_seno, frecuencia_muestreo)
sd.wait()
