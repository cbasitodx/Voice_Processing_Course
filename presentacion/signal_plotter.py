import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import threading
import time
import sounddevice as sd
import scipy.io.wavfile as wav

frecuencia_muestreo_res, senal_res = wav.read('./presentacion/resultado.wav')
senal_res = senal_res.astype('float64')

frecuencia_muestreo_base, senal_base = wav.read('./presentacion/base_directa.wav')
senal_base = senal_base.astype('float64')

plt.figure()
plt.plot(senal_res, "r-")
plt.plot(senal_base, "b--")
plt.grid(True)
plt.show()