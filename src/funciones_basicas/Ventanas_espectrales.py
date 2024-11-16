# Comparación de Ventanas
# Ventana	Ancho principal (resolución de frecuencia)	Atenuación de lóbulos laterales (fuga espectral)
# Bartlett	                Media	                                       Baja
# Hamming	                Media	                                     Moderada
# Hanning	                Media	                                 Moderada a Alta
# Blackman	                Ancho	                                      Alta

#pip install numpy matplotlib scipy


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window, freqz

# Definir los tipos de ventanas y la longitud
ventanas = ['rect', 'bartlett', 'hamming', 'hann', 'blackman']
n = 50  # Número de puntos en cada ventana (ajustable para observar el efecto en otras longitudes)

# Crear una figura para las formas de ventana en el dominio del tiempo
plt.figure(figsize=(12, 8))

for i, nombre_ventana in enumerate(ventanas):
    # Crear la ventana
    ventana = get_window(nombre_ventana, n)

    # Graficar la forma de la ventana en el dominio del tiempo
    plt.subplot(2, 3, i+1)
    plt.plot(ventana, label=f'Ventana {nombre_ventana.capitalize()}', color='b')
    plt.title(f'Ventana {nombre_ventana.capitalize()} (Dominio del Tiempo)')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.ylim(-0.1, 1.1)
    plt.legend()

plt.tight_layout()


# Crear una figura para la respuesta en frecuencia
plt.figure(figsize=(12, 8))

for i, nombre_ventana in enumerate(ventanas):
    # Crear la ventana
    ventana = get_window(nombre_ventana, n)

    # Calcular la respuesta en frecuencia
    frecuencias, respuesta = freqz(ventana, worN=8000)
    respuesta_db = 20 * np.log10(np.maximum(np.abs(respuesta), 1e-10))  # Convertir a dB

    # Graficar la respuesta en frecuencia
    plt.subplot(2, 3, i+1)
    plt.plot(frecuencias / np.pi, respuesta_db, color='r')
    plt.title(f'Ventana {nombre_ventana.capitalize()} (Respuesta en Frecuencia)')
    plt.xlabel('Frecuencia Normalizada [π rad/muestra]')
    plt.ylabel('Magnitud [dB]')
    plt.grid(True)
    plt.ylim(-100, 40)  # Ajustar el eje Y para ver bien la atenuación

plt.tight_layout()
plt.show()
