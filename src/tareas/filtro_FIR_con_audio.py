import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import threading
import time
import sounddevice as sd
import scipy.io.wavfile as wav

# Empezamos cargando la senal de audio
frecuencia_muestreo : float                                           # Frecuencia con la que se muestreo la senal (en Hz)
senal : np.ndarray                                                    # Valores de la senal registrada

frecuencia_muestreo, senal = wav.read('./src/funciones_basicas/hombre.wav')    # Obtencion del audio wav generado
senal = senal.astype('float64')

numero_de_muestras : int = len(senal)
duracion : float = (numero_de_muestras - 1)/frecuencia_muestreo 
volumen : float = 0.3  

t : np.ndarray = np.linspace(0, duracion, numero_de_muestras, endpoint=False) # Dominio de tiempo

senal -= np.mean(senal)        # Normalizacion de la senal
senal /= np.max(np.abs(senal))
senal *= volumen               # Escalamiento de la senal

# Fijamos los parametros de los filtros a usar
min_num_taps : int = 5                                                      # Minimo numero de muestras que usaran los filtros (ESTE NUMERO TIENE QUE SER IMPAR)
max_num_taps : int = 256                                                    # Maximo numero de muestras que usaran los filtros (no tiene porqué ser impar)
num_taps_increment : int = 10                                               # Incremento entre numero de muestras (ESTE NUMERO TIENE QUE SER PAR)

low_cut_off : float = 2000  # Hz
high_cut_off : float = 4400 # Hz

# Combinaciones:
# use_low_cut_off and not use_high_cut_off     -> Pasa bajas
# not use_low_cut_off and use_high_cut_off     -> Pasa altas
# use_low_cut_off and use_high_cut_off         -> Pasa banda
# not use_low_cut_off and not use_high_cut_off -> Suprime banda

use_low_cut_off : bool = True                                               # ESTA VARIABLE PUEDE TOMAR VALORES True o False
use_high_cut_off : bool = False                                             # ESTA VARIABLE PUEDE TOMAR VALORES True o False
play_audio : bool = False                                                   # Determina si se va a reproducir el audio filtrado o no

tipo_filtro : str = 'hamming'

# Funcion para la animacion (espera 3 segundos (por defecto) y pinta la imagen)
def plt_show_sec(duration: float = 3):
    def _stop():
        time.sleep(duration)
        # plt.close()
    if duration:
        threading.Thread(target=_stop).start()
    plt.show(block=False)
    plt.pause(duration)

# Creamos una ventana donde dibujaremos
plt.figure(1)

# Declaramos la variable donde almacenaremos el filtro
h : np.ndarray

# Iteramos por el numero de muestras que utilizara el filtro
for num_taps in range(min_num_taps, max_num_taps, num_taps_increment):
    
    # Obtenemos el filtro

    # Filtro paso baja
    if use_low_cut_off == True and use_high_cut_off == False:
        h = signal.firwin(num_taps, low_cut_off, fs=frecuencia_muestreo, pass_zero=True, window=tipo_filtro)
    
    # Filtro paso alta
    elif use_low_cut_off == False and use_high_cut_off == True:
        h = signal.firwin(num_taps, high_cut_off, fs=frecuencia_muestreo, pass_zero=False, window=tipo_filtro)
    
    # Filtro pasa banda
    elif use_low_cut_off == True and use_high_cut_off == True:
        h = signal.firwin(num_taps, [low_cut_off, high_cut_off], fs=frecuencia_muestreo, pass_zero=False, window=tipo_filtro)
    
    # Filtro suprime banda
    else:
        h = signal.firwin(num_taps, [low_cut_off, high_cut_off], fs=frecuencia_muestreo, pass_zero=True, window=tipo_filtro)

    # Obtenemos la respuesta en frecuencia
    H : np.ndarray = 20*np.log10(np.maximum(np.abs(np.fft.fft(h, 1024)), 1e-5))         # FFT de 1024 muestras en Db
    H = np.fft.fftshift(H)                                                              # Centramos la FFT
    w : np.ndarray = np.linspace(-frecuencia_muestreo/2, frecuencia_muestreo/2, len(H)) # Eje 'x' en el dominio de la frecuencia

    # Filtramos la senal y la reproducimos (en caso de play_audio == True)
    senal_filtrada : np.ndarray = signal.lfilter(h, 1.0, senal)
    if play_audio:
        sd.play(senal_filtrada, frecuencia_muestreo)
        sd.wait()

    # Obtenemos la FT de la senal filtrada
    H_senal : np.ndarray = 20*np.log10(np.maximum(np.abs(np.fft.fft(senal_filtrada, 1024)), 1e-5))
    H_senal = np.fft.fftshift(H_senal) # Desplazamos los 0 Hz hasta el centro
    w_senal : np.ndarray = np.linspace(-frecuencia_muestreo/2, frecuencia_muestreo/2, len(H_senal))

    # Obtenemos la respuesta al impulso del filtro
    imp = np.zeros(100) # Impulso unitario
    imp[0] = 1
    respuesta_impulso : np.ndarray = signal.lfilter(h, 1.0, imp)

    # Dibujamos la senal obtenida
    plt.subplot(4,1,1)
    plt.plot(t, senal, color="red")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud (V)")
    plt.title("Señal")
    plt.grid(True)

    # Dibujamos la FT de la senal filtrada
    plt.subplot(4,1,2)
    plt.plot(w_senal, H_senal)
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Ganancia (dB)")
    plt.title("Transformada de Fourier de la señal filtrada")
    plt.grid(True)

    # Dibujamos la respuesta al impulso del filtro (dominio del tiempo)
    plt.subplot(4,1,3)
    plt.plot(respuesta_impulso, '.-')
    plt.xlabel("Taps (n° de muestras)")
    plt.ylabel("Respuesta al impulso")
    plt.title("Respuesta al impulso del filtro")
    plt.grid(True)

    # Dibujamos el filtro en el dominio de la frecuencia  
    plt.subplot(4,1,4)
    plt.plot(w, H, '.-')
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Respuesta en frecuencia (dB)")
    plt.title("Filtro en el dominio de la frecuencia")

    # Marcadores de las frecuencias de corte
    # Filtro paso baja
    if use_low_cut_off == True and use_high_cut_off == False:
        plt.axvline(x=low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    
    # Filtro paso alta
    elif use_low_cut_off == False and use_high_cut_off == True:
        plt.axvline(x=high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    
    # Filtro pasa banda o suprime banda
    else:
        plt.axvline(x=low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')

    plt.grid(True)
    plt.tight_layout()
    plt_show_sec(1.1)

plt.tight_layout()
plt.show()


