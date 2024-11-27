import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import scipy.io.wavfile as wav

# Parametros
frecuencia_muestreo : float                                                   # Frecuencia con la que se muestreo la senal (en Hz)
senal : np.ndarray                                                            # Valores de la senal registrada

frecuencia_muestreo, senal = wav.read('./src/tareas/voz_para_fft.wav')        # Obtencion del audio wav generado
senal = senal.astype('float64')

numero_de_muestras : int = len(senal)                                         # Numero de muestras de la senal y de la fft
duracion : float = (numero_de_muestras - 1)/frecuencia_muestreo               # Duracion (en segundos) de la senal generada
volumen : float = 0.3                                                         # Entre 0 y 1

t : np.ndarray = np.linspace(0, duracion, numero_de_muestras, endpoint=False) # Dominio de tiempo

# Normalizacion de la senal
senal -= np.mean(senal)
senal /= np.max(np.abs(senal))

# Escalamiento de la senal
senal *= volumen

# Obtenemos el espectro de frecuencias de la senal
H = 20*np.log10(np.maximum(np.abs(np.fft.fft(senal, numero_de_muestras)), 1e-5)) # En Decibelios
H = np.fft.fftshift(H) # Desplazamos los 0 Hz hasta el centro

w = np.linspace(-frecuencia_muestreo/2, frecuencia_muestreo/2, len(H)) # Dominio de la frecuencia

# Reproducimos la senal
#sd.play(senal, frecuencia_muestreo)
#sd.wait()

# Dibujamos la senal obtenida y su espectro
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, senal, color="red")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (V)")
plt.subplot(2,1,2)
plt.plot(w, H)
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Ganancia (dB)")
plt.show()

