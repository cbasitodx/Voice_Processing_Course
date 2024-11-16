#pip install numpy scipy matplotlib 

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import threading
import time


def plt_show_sec(duration: float = 3):
    def _stop():
        time.sleep(duration)
        # plt.close()
    if duration:
        threading.Thread(target=_stop).start()
    plt.show(block=False)
    plt.pause(duration)


frecuencia_muestreo = 44100
min_num_taps = 5 # ESTE NÚMERO TIENE QUE SER IMPAR
max_num_taps = 256
num_taps_increment = 10 # ESTE NÚMERO TIENE QUE SER PAR

low_cut_off = 2000 # Hz
high_cut_off = 4400 # Hz

use_low_cut_off = True # ESTA VARIABLE PUEDE TOMAR VALORES True o False
use_high_cut_off = False # ESTA VARIABLE PUEDE TOMAR VALORES True o False
play_audio = True



plt.figure(1)
for num_taps in range(min_num_taps, max_num_taps, num_taps_increment):
    if use_low_cut_off == True and use_high_cut_off == False:
        h = signal.firwin(num_taps, low_cut_off, fs=frecuencia_muestreo, pass_zero=True, window='hamming') #filtro paso baja
    elif use_low_cut_off == False and use_high_cut_off == True:
        h = signal.firwin(num_taps, high_cut_off, fs=frecuencia_muestreo, pass_zero=False, window='hamming') #filtro paso alta
    elif use_low_cut_off == True and use_high_cut_off == True:
        h = signal.firwin(num_taps, [low_cut_off, high_cut_off], fs=frecuencia_muestreo, pass_zero=False, window='hamming') #filtro paso banda
    else:
        h = signal.firwin(num_taps, [low_cut_off, high_cut_off], fs=frecuencia_muestreo, pass_zero=True, window='hamming') #filtro rechazo banda.

    # plot the frequency response
    H = 20*np.log10(np.maximum(np.abs(np.fft.fft(h, 1024)), 1e-5)) # take the 1024-point FFT and magnitude
    H = np.fft.fftshift(H) # make 0 Hz in the center
    w = np.linspace(-frecuencia_muestreo/2, frecuencia_muestreo/2, len(H)) # x axis

    imp = np.zeros(100)
    imp[0] = 1  # Impulso unitario
    respuesta_impulso = signal.lfilter(h, 1.0, imp)

    plt.subplot(2,1,1)
    plt.plot(respuesta_impulso, '.-')
    plt.xlabel("taps")
    plt.ylabel("respuesta al impulso")

    plt.subplot(2,1,2)
    plt.plot(w, H, '.-')
    if use_low_cut_off == True and use_high_cut_off == False:
        plt.axvline(x=low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    elif use_low_cut_off == False and use_high_cut_off == True:
        plt.axvline(x=high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    else:
        plt.axvline(x=low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-low_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
        plt.axvline(x=-high_cut_off, color='g', linestyle='--', label='Frecuencia de corte')
    plt.xlabel("frecuencia")
    plt.ylabel("respuesta al impulso")

    plt.tight_layout()
    plt_show_sec(1.1)

plt.tight_layout()
plt.show()
