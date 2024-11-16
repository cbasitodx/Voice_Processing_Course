#pip install numpy scipy matplotlib

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import threading
import time

# Función para mostrar gráficos por un período específico
def plt_show_sec(duracion: float = 3):
    def _stop():
        time.sleep(duracion)
    if duracion:
        threading.Thread(target=_stop).start()
    plt.show(block=False)
    plt.pause(duracion)


# Parámetros de configuración
frecuencia_muestreo = 44100
orden_minimo = 2  # Orden mínimo del filtro
orden_maximo = 10  # Orden máximo del filtro
incremento_orden = 2

frecuencia_corte_baja = 2000  # Hz
frecuencia_corte_alta = 4400  # Hz

usar_corte_bajo = False  # Define si se usa corte bajo
usar_corte_alto = True  # Define si se usa corte alto

# Parámetros para los filtros IIR que requieren rp y rs
tipo_filtro = 'butter'  # 'butter', 'cheby1', 'cheby2', 'ellip', 'bessel'
rp = 1  # Ondulación máxima en la banda de paso (solo para cheby1 y ellip)
rs = 40  # Atenuación mínima en la banda de rechazo (solo para cheby2 y ellip)


plt.figure(1)
for orden in range(orden_minimo, orden_maximo + 1, incremento_orden):
    # Seleccionar el tipo de filtro y definir rp/rs cuando sea necesario
    if tipo_filtro in 'cheby1':
        if usar_corte_bajo and not usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_baja, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)
        elif not usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_alta, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)
        elif usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)
        else:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp)

    elif tipo_filtro == 'cheby2':
        if usar_corte_bajo and not usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_baja, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)
        elif not usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_alta, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)
        elif usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)
        else:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rs=rs)

    elif tipo_filtro == 'ellip':
        if usar_corte_bajo and not usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_baja, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)
        elif not usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_alta, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)
        elif usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)
        else:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo, rp=rp, rs=rs)

    else:  # Para tipos que no necesitan rp/rs como butter y bessel
        if usar_corte_bajo and not usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_baja, btype='low', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)
        elif not usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, frecuencia_corte_alta, btype='high', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)
        elif usar_corte_bajo and usar_corte_alto:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandpass', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)
        else:
            b, a = signal.iirfilter(orden, [frecuencia_corte_baja, frecuencia_corte_alta], btype='bandstop', analog=False, ftype=tipo_filtro, fs=frecuencia_muestreo)

    # Obtener respuesta en frecuencia del filtro IIR
    w, h = signal.freqz(b, a, worN=1024, fs=frecuencia_muestreo)
    h_db = 20 * np.log10(np.maximum(abs(h), 1e-10))

    # Gráfico de la respuesta al impulso
    imp = np.zeros(100)
    imp[0] = 1  # Impulso unitario
    respuesta_impulso = signal.lfilter(b, a, imp)
    plt.subplot(2, 1, 1)
    plt.plot(respuesta_impulso, '.-', label=f'Orden {orden}')
    plt.xlabel("Muestras")
    plt.ylabel("Respuesta al impulso")
    # plt.legend()

    # Gráfico de la respuesta en frecuencia
    plt.subplot(2, 1, 2)
    plt.plot(w, h_db, label=f'Orden {orden}')
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud [dB]")
    plt.ylim(-60, 5)

    # Marcadores de las frecuencias de corte
    if usar_corte_bajo and not usar_corte_alto:
        plt.axvline(frecuencia_corte_baja, color='g', linestyle='--', label='Frecuencia de corte')
    elif not usar_corte_bajo and usar_corte_alto:
        plt.axvline(frecuencia_corte_alta, color='g', linestyle='--', label='Frecuencia de corte')
    else:
        plt.axvline(frecuencia_corte_baja, color='g', linestyle='--', label='Frecuencia de corte baja')
        plt.axvline(frecuencia_corte_alta, color='r', linestyle='--', label='Frecuencia de corte alta')

    # plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt_show_sec(1.1)

plt.tight_layout()
plt.show()
