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
min_order : int = 2         # Minimo orden del filtro a usar
max_order : int = 10        # Maximo orden del filtro a usar
order_increment : int = 2   # Incremento del orden del filtro

low_cut_off : float = 2000 # Hz
high_cut_off : float = 4400 # Hz

# Combinaciones:
# use_low_cut_off and not use_high_cut_off     -> Pasa bajas
# not use_low_cut_off and use_high_cut_off     -> Pasa altas
# use_low_cut_off and use_high_cut_off         -> Pasa banda
# not use_low_cut_off and not use_high_cut_off -> Suprime banda

use_low_cut_off : bool = True                                               # ESTA VARIABLE PUEDE TOMAR VALORES True o False
use_high_cut_off : bool = False                                             # ESTA VARIABLE PUEDE TOMAR VALORES True o False
play_audio : bool = False                                                   # Determina si se va a reproducir el audio filtrado o no

tipo_filtro = 'butter'  # Opciones: 'butter', 'cheby1', 'cheby2', 'ellip', 'bessel'
rp = 1                  # Ondulacion máxima en la banda de paso (solo para cheby1 y ellip)
rs = 40                 # Atenuacion mínima en la banda de rechazo (solo para cheby2 y ellip)

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

# Declaramos las variables donde almacenaremos los coeficientes del filtro
a : np.ndarray
b : np.ndarray

# Iteramos por el orden qye utilizara el filtro
for orden in range(min_order, max_order + 1, order_increment):

    # Seleccionamos el tipo de filtro y definimos rp/rs cuando sea necesario
    if tipo_filtro in 'cheby1':

        # Pasa bajas
        if use_low_cut_off and not use_high_cut_off:
            b, a = signal.iirfilter(orden, low_cut_off, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)

        # Pasa altas
        elif not use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, high_cut_off, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)

        # Pasa banda
        elif use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)

        # Suprime banda
        else:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)

    elif tipo_filtro == 'cheby2':
        if use_low_cut_off and not use_high_cut_off:
            b, a = signal.iirfilter(orden, low_cut_off, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)
        elif not use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, high_cut_off, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)
        elif use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)
        else:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)

    elif tipo_filtro == 'ellip':
        if use_low_cut_off and not use_high_cut_off:
            b, a = signal.iirfilter(orden, low_cut_off, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)
        elif not use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, high_cut_off, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)
        elif use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)
        else:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)

    else:  # Para tipos que no necesitan rp/rs como butter y bessel
        if use_low_cut_off and not use_high_cut_off:
            b, a = signal.iirfilter(orden, low_cut_off, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)
        elif not use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, high_cut_off, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)
        elif use_low_cut_off and use_high_cut_off:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)
        else:
            b, a = signal.iirfilter(orden, [low_cut_off, high_cut_off], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)

    # Obtenemos la respuesta en frecuencia del filtro IIR
    w, H = signal.freqz(b, a, worN=1024, fs=frecuencia_muestreo)
    H = 20 * np.log10(np.maximum(abs(H), 1e-10)) # Obtenemos la imagen en decibelios

    # Filtramos la senal y la reproducimos (en caso de play_audio == True)
    senal_filtrada : np.ndarray = signal.lfilter(b, a, senal)
    if play_audio:
        sd.play(senal_filtrada, frecuencia_muestreo)
        sd.wait()

    # Obtenemos la FT de la senal filtrada
    H_senal : np.ndarray = 20*np.log10(np.maximum(np.abs(np.fft.fft(senal_filtrada, 1024)), 1e-5))
    H_senal = np.fft.fftshift(H_senal) # Desplazamos los 0 Hz hasta el centro
    w_senal : np.ndarray = np.linspace(-frecuencia_muestreo/2, frecuencia_muestreo/2, len(H_senal))

    # Obtenemos la respuesta al impulso del filtro
    imp = np.zeros(100)
    imp[0] = 1  # Impulso unitario
    respuesta_impulso = signal.lfilter(b, a, imp)

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
    plt.subplot(4, 1, 3)
    plt.plot(respuesta_impulso, '.-', label=f'Orden {orden}')
    plt.xlabel("Muestras")
    plt.ylabel("Respuesta al impulso")
    plt.title("Respuesta al impulso del filtro")
    plt.grid(True)

    # Dibujamos el filtro en el dominio de la frecuencia  
    plt.subplot(4, 1, 4)
    plt.plot(w, H, label=f'Orden {orden}')
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Amplitud (dB)")
    plt.ylim(-60, 5)
    plt.title("Filtro en el dominio de la frecuencia")

    # Marcadores de las frecuencias de corte
    if use_low_cut_off and not use_high_cut_off:
        plt.axvline(low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    elif not use_low_cut_off and use_high_cut_off:
        plt.axvline(high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    else:
        plt.axvline(low_cut_off, color='g', linestyle='--', label='Frecuencia de corte baja')
        plt.axvline(high_cut_off, color='r', linestyle='--', label='Frecuencia de corte alta')

    plt.grid(True)
    plt.tight_layout()
    plt_show_sec(1.1)

plt.tight_layout()
plt.show()

