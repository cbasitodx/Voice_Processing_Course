#pip install numpy matplotlib sounddevice

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import random


# Parámetros
frecuencia_muestreo = 44100  # Frecuencia de muestreo en Hz
frecuencias = [1000, 2254, 4780]  # Frecuencia en Hz (COMPROBAR RESPUESTA PARA VALORES CON Y SIN DECIMALES)
# frecuencias = numeros_random = [random.randint(100, 10000) for _ in range(1000)]  # Frecuencia en Hz (COMPROBAR RESPUESTA PARA VALORES CON Y SIN DECIMALES)

duracion = 2.0    # Duración en segundos
volumen = 0.5 # entre 0 y 1

# COMPROBAR RESPUESTA PARA DISTINTO NUMERO DE MUESTRAS DE LA FFT EN COMBINACIÓN CON LAS FRECUENCIAS USADAS
# numero_de_muestras_para_fft = 1024
numero_de_muestras_para_fft = int(frecuencia_muestreo*duracion)

# Generación de la señal senoidal
# Tiempo de cada muestra
t = np.linspace(0, duracion, int(frecuencia_muestreo * duracion), endpoint=False)
señal = np.zeros(len(t))
for frecuencia in frecuencias:
    # Vamos acumulando las señales sinusoidales de cada frecuencia.
    señal = señal + volumen * np.sin(2 * np.pi * frecuencia * t)

# Sustraemos la media.
señal -= np.mean(señal)
señal /= np.max(np.abs(señal))
señal *= volumen



# Espectro en frecuencias.
H = 20*np.log10(np.maximum(np.abs(np.fft.fft(señal, numero_de_muestras_para_fft)), 1e-5)) # Tomamos distintos numeros de muestras para la fft, viendo como afecta al resultado.
H = np.fft.fftshift(H) # Desplazamos los 0 Hz hasta el centro
w = np.linspace(-frecuencia_muestreo/2, frecuencia_muestreo/2, len(H)) # Calculamos los valores de frecuencia en el eje x.

# Reproducción de la onda
sd.play(señal, frecuencia_muestreo)
sd.wait()

# Dibujar la señal generada y su espectro.
plt.figure()
plt.subplot(2,1,1)
plt.plot(t[:int(5*frecuencia_muestreo/np.min(frecuencias))], señal[:int(5*frecuencia_muestreo/np.min(frecuencias))])
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.subplot(2,1,2)
plt.plot(w, H)
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("ganancia (dB)")
plt.show()

