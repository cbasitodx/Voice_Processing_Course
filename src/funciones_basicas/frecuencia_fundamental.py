#pip install numpy scipy matplotlib


import numpy as np
from scipy.fftpack import fft, ifft
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# Función para calcular la frecuencia fundamental usando cepstrum
def calcular_f0_cepstrum(señal, fs, min_frequency, max_frequency):
    # Aplicar una ventana (Hamming) a la señal
    ventana = np.hamming(len(señal))
    señal_ventaneada = señal * ventana

    # Calcular la transformada de Fourier
    espectro = fft(señal_ventaneada)
    espectro_log = np.log(np.abs(espectro) + 1e-10)  # Logaritmo del espectro de magnitud

    # Calcular el cepstrum (transformada inversa del log-espectro)
    cepstrum = np.abs(ifft(espectro_log))

    # Definir el rango de quefrencias (tiempos del cepstrum) a buscar (0.002 a 0.02 segundos aprox. para F0 típicos)
    min_quefrency = int(fs / max_frequency)  # para F0 máx ≈ 500 Hz
    max_quefrency = int(fs / min_frequency)   # para F0 mín ≈ 50 Hz

    # Encontrar el pico en el rango de quefrencias del cepstrum
    pico_cepstral = np.argmax(cepstrum[min_quefrency:max_quefrency]) + min_quefrency

    # Convertir el pico de quefrencia a frecuencia fundamental
    f0 = fs / pico_cepstral
    return f0



# Cargar una señal de audio (archivo WAV)
fs, data = wav.read("./src/funciones_basicas/hombre.wav")
if data.ndim > 1:
    data = data[:, 0]  # Convertir a mono si es estéreo

min_frequency = 75 #Mínima frecuencia fundamental
max_frequency = 400 #Máxima frecuencia fundamental


# Seleccionar un segmento corto de la señal en torno al máximo (donde haya voz)
posicion_max = np.argmax(np.abs(data))
segmento = data[posicion_max-512:posicion_max+512]  # 1024 puntos para análisis

# Calcular la frecuencia fundamental
frecuencia_fundamental = calcular_f0_cepstrum(segmento, fs, min_frequency, max_frequency)
print(f"Frecuencia Fundamental (F0): {frecuencia_fundamental:.2f} Hz")

# Opcional: Graficar el cepstrum para visualizar el pico
ventana = np.hamming(len(segmento))
señal_ventaneada = segmento * ventana
espectro = fft(señal_ventaneada)
espectro_log = np.log(np.abs(espectro) + np.finfo(float).eps)
cepstrum = np.abs(ifft(espectro_log))


min_quefrency = int(fs / max_frequency)  # para F0 máx ≈ 500 Hz
max_quefrency = int(fs / min_frequency)   # para F0 mín ≈ 50 Hz
w = np.linspace(min_quefrency, max_quefrency, max_quefrency-min_quefrency)
f0_values = fs / w

plt.figure()
plt.plot(f0_values, cepstrum[min_quefrency:max_quefrency])
plt.title("Cepstrum de la señal")
plt.xlabel("Frecuencia fundamental")
plt.ylabel("Amplitud")
plt.show()
