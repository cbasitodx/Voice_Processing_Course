#pip install scipy matplotlib

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.signal import spectrogram, get_window
from mpl_toolkits.mplot3d import Axes3D


# Esta función calcula el espectrograma de una señal de audio con soporte para múltiples tipos de ventana
def espectrograma_personalizado(señal, frecuencia_muestreo, ventana='bartlett', nperseg=512, solapamiento=256, nfft=512):
    """
    Calcula el espectrograma de una señal de audio con soporte para múltiples ventanas.

    Parámetros:
    - señal: array de la señal de audio.
    - frecuencia_muestreo: frecuencia de muestreo de la señal.
    - ventana: tipo de ventana a aplicar ('rect', 'hamming', 'bartlett', 'hann' o 'blackman').
    - nperseg: longitud de cada segmento.
    - solapamiento: cantidad de solapamiento entre segmentos.
    - nfft: número de puntos de la FFT.

    Retorna:
    - f: frecuencias
    - t: tiempos
    - Sxx: espectrograma (potencia espectral en cada segmento)
    """

    # Seleccionar la ventana especificada
    try:
        vent = get_window(ventana, nperseg)
    except ValueError:
        raise ValueError(f"Tipo de ventana '{ventana}' no soportado. Usa 'rect', 'bartlett', 'hamming', 'hann' o 'blackman'.")

    paso = nperseg - solapamiento  # Calcular el desplazamiento entre ventanas (Cuantas muestras se mueve la ventana)
    num_segmentos = (len(señal) - solapamiento) // paso  # Número de segmentos en la señal (Numero de ventanas que tendre)

    # Inicializar arrays para almacenar el espectrograma
    Sxx = np.zeros((nfft // 2 + 1, num_segmentos))  # Espectrograma vacío
    t = np.arange(num_segmentos) * paso / frecuencia_muestreo  # Tiempos de cada segmento
    f = np.fft.rfftfreq(nfft, 1 / frecuencia_muestreo)  # Frecuencias de cada bin de la FFT (solo de la parte positiva)

    # Calcular el espectrograma
    for i in range(num_segmentos):
        # Extraer la ventana de señal y aplicarle la ventana seleccionada
        inicio = i * paso
        segmento = señal[inicio:inicio + nperseg] * vent

        # Realizar la FFT de una señal real y devuelve solo la magnitud positiva del espectro
        espectro = np.fft.rfft(segmento, n=nfft)
        # Potencia espectral (puede cambiarse a magnitud si prefieres)
        Sxx[:, i] = np.abs(espectro)**2

    return f, t, Sxx



# Cargar el archivo de audio
frecuencia_muestreo, señal = wav.read('./src/funciones_basicas/hombre.wav')  # Cambia el nombre del archivo según sea necesario
señal = señal - np.mean(señal)  # Resta la media (para centrarlas en 0)
señal /= np.max(np.abs(señal))  # Normalizacion (para que la senal oscile entre +1 y -1) 

tiempo = np.linspace(0, len(señal) / frecuencia_muestreo, len(señal), endpoint=False)
ventanas = ['rect', 'hamming', 'bartlett', 'hann', 'blackman']

plt.figure(figsize=(12, 8))
# Graficar la señal de audio
plt.subplot(3, 2, 1)
plt.plot(tiempo, señal)
plt.title("Señal de audio")
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')

for i, nombre_ventana in enumerate(ventanas):
    f, t, Sxx = spectrogram(señal, frecuencia_muestreo, window=nombre_ventana, nperseg=512, noverlap=384, nfft=512) #se puede usar la scipy.signal.spectrogram
    # f, t, Sxx = espectrograma_personalizado(señal, frecuencia_muestreo, ventana=nombre_ventana, nperseg=512, solapamiento=384, nfft=512)

    # Graficar el espectrograma
    plt.subplot(3, 2, i+2)
    plt.pcolormesh(t, f, 10 * np.log10(np.maximum(Sxx, 1e-10)), shading='gouraud', cmap='jet')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Frecuencia [Hz]')
    plt.title(f'Ventana {nombre_ventana}')
    plt.colorbar(label='Amplitud (dB)')

plt.tight_layout()
plt.show()
