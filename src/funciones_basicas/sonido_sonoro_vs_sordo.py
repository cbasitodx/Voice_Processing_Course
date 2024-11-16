#pip install numpy matplotlib scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq


# Detección de sonoridad usando ZCR (tasa de cruces por cero)
def cruce_por_cero_con_umbral(señal, longitud_ventana, salto_ventana, umbral_min=0.001, sonoro_vs_sordo=0.06):
    num_ventanas = (len(señal) - longitud_ventana) // salto_ventana + 1
    valores_cruce_cero = np.zeros(num_ventanas)
    clasificacion_sonora = np.zeros(num_ventanas)
    clasificacion_sorda = np.zeros(num_ventanas)
    for i in range(num_ventanas):
        inicio_ventana = i * salto_ventana
        fin_ventana = inicio_ventana + longitud_ventana
        ventana = señal[inicio_ventana:fin_ventana]

        # Calcular los cruces por cero con el umbral
        cruces_cero = np.where(np.abs(np.diff(np.sign(ventana))) > 0)[0]  # Posiciones de cruces por cero
        cruces_significativos = np.where(np.abs(ventana[cruces_cero]) > umbral_min)[0]  # Cruces por encima del umbral

        valores_cruce_cero[i] = len(cruces_significativos) / len(ventana)
        if valores_cruce_cero[i] > 0:
            if valores_cruce_cero[i] < sonoro_vs_sordo:
                clasificacion_sonora[i] = 1
            else:
                clasificacion_sorda[i] = 1

    return valores_cruce_cero, clasificacion_sonora, clasificacion_sorda


# Parámetros comunes
frecuencia_muestreo = 44100  # Frecuencia de muestreo en Hz
duracion = 0.05  # Duración del sonido en segundos

# Generación del sonido sonoro (onda senoidal)
frecuencia_sonoro = 440  # Frecuencia de 440 Hz (La4)
tiempo = np.linspace(0, duracion, int(frecuencia_muestreo * duracion), endpoint=False)
sonido_sonoro = 0.5 * np.sin(2 * np.pi * frecuencia_sonoro * tiempo)

# Generación del sonido sordo (ruido blanco)
sonido_sordo = 0.5 * np.random.normal(0, 1, tiempo.shape)


# Transformada de Fourier para el espectro de frecuencias
fft_sonoro = fft(sonido_sonoro)
fft_sordo = fft(sonido_sordo)
frecuencias = fftfreq(len(tiempo), 1 / frecuencia_muestreo)


longitud_ventana = 512  # Longitud de ventana en muestras
salto_ventana = int(longitud_ventana / 4)  # Solapamiento 75%
num_ventanas = (len(tiempo) - longitud_ventana) // salto_ventana + 1
valores_cruce_cero_sonoro, clasificacion_sonora_sonoro, clasificacion_sorda_sonoro = cruce_por_cero_con_umbral(
    sonido_sonoro, longitud_ventana, salto_ventana, umbral_min=0.001, sonoro_vs_sordo=0.06
)
valores_cruce_cero_sordo, clasificacion_sonora_sordo, clasificacion_sorda_sordo = cruce_por_cero_con_umbral(
    sonido_sordo, longitud_ventana, salto_ventana, umbral_min=0.001, sonoro_vs_sordo=0.06
)


# Gráfico de los sonidos y sus espectros de frecuencias
figura, ejes = plt.subplots(3, 2, figsize=(14, 8))

# Señales de tiempo
ejes[0, 0].plot(tiempo, sonido_sonoro)
ejes[0, 0].set_title("Sonido Sonoro (Onda Senoidal)")
ejes[0, 0].set_xlabel("Tiempo [s]")
ejes[0, 0].set_ylabel("Amplitud")

ejes[0, 1].plot(tiempo, sonido_sordo)
ejes[0, 1].set_title("Sonido Sordo (Ruido Blanco)")
ejes[0, 1].set_xlabel("Tiempo [s]")
ejes[0, 1].set_ylabel("Amplitud")

# Espectros de frecuencias
ejes[1, 0].plot(frecuencias[:len(frecuencias) // 2], np.abs(fft_sonoro)[:len(frecuencias) // 2])
ejes[1, 0].set_title("Espectro de Frecuencias - Sonido Sonoro")
ejes[1, 0].set_xlabel("Frecuencia [Hz]")
ejes[1, 0].set_ylabel("Amplitud")

ejes[1, 1].plot(frecuencias[:len(frecuencias) // 2], np.abs(fft_sordo)[:len(frecuencias) // 2])
ejes[1, 1].set_title("Espectro de Frecuencias - Sonido Sordo")
ejes[1, 1].set_xlabel("Frecuencia [Hz]")
ejes[1, 1].set_ylabel("Amplitud")


eje_tiempo_energia = np.linspace(0, len(tiempo) / frecuencia_muestreo, num_ventanas)

ejes[2, 0].plot(eje_tiempo_energia, valores_cruce_cero_sonoro, label='Tasa de Cruces por Cero (ZCR)')
ejes[2, 0].fill_between(eje_tiempo_energia, 0, np.max(valores_cruce_cero_sonoro),
                        where=clasificacion_sonora_sonoro, color='orange', alpha=0.5, label="Voz sonora")
ejes[2, 0].fill_between(eje_tiempo_energia, 0, np.max(valores_cruce_cero_sonoro),
                        where=clasificacion_sorda_sonoro, color='green', alpha=0.5, label="Voz sorda")
ejes[2, 0].set_title("Detección de Sonoridad")
ejes[2, 0].set_ylabel("ZCR")
ejes[2, 0].set_xlabel("Tiempo (s)")
ejes[2, 0].legend()

ejes[2, 1].plot(eje_tiempo_energia, valores_cruce_cero_sordo, label='Tasa de Cruces por Cero (ZCR)')
ejes[2, 1].fill_between(eje_tiempo_energia, 0, np.max(valores_cruce_cero_sordo),
                        where=clasificacion_sonora_sordo, color='orange', alpha=0.5, label="Voz sonora")
ejes[2, 1].fill_between(eje_tiempo_energia, 0, np.max(valores_cruce_cero_sordo),
                        where=clasificacion_sorda_sordo, color='green', alpha=0.5, label="Voz sorda")
ejes[2, 1].set_title("Detección de Sonoridad")
ejes[2, 1].set_ylabel("ZCR")
ejes[2, 1].set_xlabel("Tiempo (s)")
ejes[2, 1].legend()

plt.tight_layout()
plt.show()
