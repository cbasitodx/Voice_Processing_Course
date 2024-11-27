import matplotlib.axes
import matplotlib.figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.fftpack import fft, ifft

# **************************************************************************** #
#                             FUNCIONES A UTILIZAR                             #
# **************************************************************************** #

def deteccion_act_voz(senal          : np.ndarray, 
                      umbral_energia : float, 
                      long_ventana   : int, 
                      despl_ventana  : float) -> tuple[np.ndarray]:
    '''
    Detecta la activacion de voz en una señal dada y su energia en dicho caso

    Args:
        * senal: Array con los valores de la señal en el tiempo
        * umbral_energia: Umbral que se tiene que superar para considerar que la energia de la señal es significativa
        * long_ventana: Longitud de la ventana de analisis (en numero de muestras)
        * despl_ventana: Número de muestras que se desplaza la ventana de análisis

    Return:
        Una tupla de 3 elementos: El primero es un array de booleanos que determina si ha habido activacion de la voz o no por ventana, 
        el segundo el vector de energias de la señal normalizado entre 0 y 1 por ventana, y el tercero el umbral de energia normalizado entre 0 y 1 (para poder dibujarlo)
    '''
    # Empezamos obteniendo el numero de ventanas que vamos a procesar
    num_ventanas : int = (len(senal) - long_ventana) // despl_ventana + 1

    # Inicializamos los vectores que vamos a devolver
    energia_senal : list[float] = [] # Energia de la senal en cada ventana
    act_voz : list[bool] = []        # Vector de booleanos que determina si hubo activacion de la voz

    # Recorremos la senal ventana a ventana
    for idx in range(num_ventanas):
        # Obtenemos la senal en la ventana
        init_ventana : int = int(idx*despl_ventana)
        fin_ventana  : int = int(init_ventana + long_ventana)

        senal_en_ventana : np.ndarray = senal[init_ventana : fin_ventana]

        # Obtenemos su energia y la anadimos al vector de energias  
        energia_en_ventana : np.ndarray = np.sum(senal_en_ventana ** 2)
        energia_senal.append(energia_en_ventana)

        # Comprobamos si la energia supera el umbral. Anadimos el resultado al vector de activacion de voz
        if energia_en_ventana < umbral_energia: 
            act_voz.append(False) # No hubo activacion
        else:
            act_voz.append(True) # Si hubo activacion

    # Normalizamos las energias en funcion de de la maxima energia obtenida
    energia_senal_norm = energia_senal / np.max(energia_senal)

    # Retornamos tambien el umbral de energia normalizado para poder dibujarlo correctamente
    umbral_normalizado : float = umbral_energia / np.max(energia_senal)

    return act_voz, energia_senal_norm, umbral_normalizado
    
def deteccion_sonoridad(senal          : np.ndarray, 
                        long_ventana   : int, 
                        despl_ventana  : float, 
                        umbral_energia : float = 0.01,
                        umbral_min     : float = 0.001, 
                        umbral_sordo   : float = 0.06) -> tuple[np.ndarray]:
    '''
    Clasifica una señal enventanada como sonido sonoro o sordo

    Args:
        * senal: Array con los valores de la señal en el tiempo
        * long_ventana: Longitud de la ventana de analisis (en numero de muestras)
        * despl_ventana: Número de muestras que se desplaza la ventana de análisis
        * umbral_energia: Umbral que se tiene que superar para considerar que la energia de la señal es significativa
        * umbral_min: Umbral que tiene que superar la señal (su valor) en los puntos donde se ha detectado que cruza por 0 para poder considerar que el cruce ha sido significativo
                      (si no lo supera asumimos que ha sido una oscilascion insignificante y realmente no ha cruzado por 0) 
        * umbral_sordo: Umbral que debe superar el numero de veces que la señal cruza por 0 para clasificar a la señal en la ventana como un sonido *sonoro*. Si no lo supera se clasifica como un sonido *sordo*.
                        Este umbral se mide en "número de cruces por muestras en ventana"
    
    Return:
        Una tupla de 3 elementos: El primero es un array con el número de cruces por 0 en cada ventana, el segundo y tercero son arrays de booleanos
        donde se clasifica a la señal en sonido sonoro o sordo por ventana
    '''
    # Empezamos obteniendo el numero de ventanas que vamos a procesar
    num_ventanas : int = (len(senal) - long_ventana) // despl_ventana + 1

    # Inicializamos los vectores que vamos a devolver
    valores_cruce_cero   : np.ndarray = np.zeros(num_ventanas) # Tasa de crucer por cero (ZCR)
    clasificacion_sonora : np.ndarray = np.zeros(num_ventanas) # Vectores de 0's y 1's que determinan si los sonidos son sonoros o sordos
    clasificacion_sorda  : np.ndarray = np.zeros(num_ventanas)

    # Obtenemos el vector para detectar si hubo activacion de la voz
    act_voz_bool : np.ndarray
    act_voz_bool, _, _ = deteccion_act_voz(senal=senal, umbral_energia=umbral_energia, long_ventana=long_ventana, despl_ventana=despl_ventana)

    # Recorremos la senal ventana a ventana
    for idx in range(num_ventanas):
        # Obtenemos la senal en la ventana
        init_ventana : int = int(idx*despl_ventana)
        fin_ventana  : int = int(init_ventana + long_ventana)

        senal_en_ventana : np.ndarray = senal[init_ventana : fin_ventana]

        # Calcular los cruces por cero con el umbral solo cuando haya habido activacion de la voz
        if act_voz_bool[idx]:
            cruces_cero           : np.ndarray = np.where(np.abs(np.diff(np.sign(senal_en_ventana))) > 0)[0]      # Posiciones de cruces por cero
            cruces_significativos : np.ndarray = np.where(np.abs(senal_en_ventana[cruces_cero]) > umbral_min)[0]  # Cruces por encima del umbral

            # Ratio de numero de cruces significativos por numero de muestras en la ventana
            valores_cruce_cero[idx] = len(cruces_significativos) / len(senal_en_ventana)
            
            # Si se produjo algun cruce por cero significativo, los clasificamos en sonoros o sordos
            if valores_cruce_cero[idx] > 0:
                if valores_cruce_cero[idx] < umbral_sordo:
                    clasificacion_sonora[idx] = 1
                else:
                    clasificacion_sorda[idx] = 1
        
        else:
            valores_cruce_cero[idx] = 0

    return valores_cruce_cero, clasificacion_sonora, clasificacion_sorda    

def calcular_f0_cepstrum(senal : np.ndarray, 
                         freq_muestreo : float, 
                         min_frequency : float, 
                         max_frequency : float) -> float:
    '''
    Calcula la frecuencia fundamental de una señal

    Args:
        * senal: Array con los valores de la señal en el tiempo
        * freq_muestreo: Frecuencia (en Hz) a la que se muestreo la señal {senal}
        * min_frequency, max_frequency: Rango de frecuencias en el que se busca hallar la frecuencia fundamental del sonido (para la voz están entre 75 y 400Hz)
    
    Return:
        Devuelve el la frecuencia fundamental (f0, en Hz) de una señal {senal} como la frecuencia en la que se da el pico cepstral
    '''
    # Aplicamos una ventana (Hamming) a la señal
    ventana : np.ndarray = np.hamming(len(senal))
    senal_ventaneada : np.ndarray = senal * ventana

    # Calculamos la transformada de Fourier de la senal ventaneada
    espectro : np.ndarray = fft(senal_ventaneada)
    espectro_log : np.ndarray = np.log(np.abs(espectro) + np.finfo(float).eps)  # Logaritmo del espectro de magnitud

    # Calculamos el cepstrum (que es la transformada inversa del log-espectro)
    cepstrum : np.ndarray = np.abs(ifft(espectro_log))

    # Definimos el rango de quefrencias (tiempos del cepstrum) a buscar
    min_quefrency : float = int(freq_muestreo / max_frequency)
    max_quefrency : float = int(freq_muestreo / min_frequency)

    # Encontramos la frecuencia en la que ocurre el pico cepstral (en el rango de quefrencias del cepstrum)
    pico_cepstral : float = np.argmax(cepstrum[min_quefrency:max_quefrency]) + min_quefrency

    # Convertimos el pico de quefrencia a frecuencia fundamental
    f0 : float = freq_muestreo / pico_cepstral
    return f0

def calcular_freq_fundamental_por_ventana(senal          : np.ndarray, 
                                          freq_muestreo  : float,
                                          long_ventana   : float,
                                          despl_ventana  : float, 
                                          umbral_energia : float = 0.01,
                                          min_frequency  : float = 75, 
                                          max_frequency  : float = 400) -> np.ndarray:
    '''
    Calcula las frecuencias fundamentales de una señal en cada una de las ventanas de análisis

    Args:
        * senal: Array con los valores de la señal en el tiempo
        * freq_muestreo: Frecuencia (en Hz) a la que se muestreo la señal {senal}
        * long_ventana: Longitud de la ventana de analisis (en numero de muestras)
        * despl_ventana: Número de muestras que se desplaza la ventana de análisis
        * umbral_energia: Umbral que se tiene que superar para considerar que la energia de la señal es significativa
        * min_frequency
        * max_frequency
    
    Return:
        Devuelve un array con las frecuencias fundamentales de la señal {senal} por ventana
    '''
    # Inicializamos el vector que vamos a devolver
    frecuencias_fundamentales_por_ventana : list[float] = []

    # Obtenemos el vector para detectar si hubo activacion de la voz
    act_voz_bool : np.ndarray
    act_voz_bool, _, _ = deteccion_act_voz(senal, umbral_energia, long_ventana, despl_ventana)

    # Recorremos la senal ventana a ventana
    for idx in range(len(act_voz_bool)):
        
        # Calcular la frecuencia fundamental de la senal en la ventana solo cuando haya habido activacion de la voz
        if act_voz_bool[idx]:
            # Obtenemos la senal en la ventana
            init_ventana : int = int(idx*despl_ventana)
            fin_ventana  : int = int(init_ventana + long_ventana)

            senal_en_ventana : np.ndarray = senal[init_ventana : fin_ventana]
            frecuencias_fundamentales_por_ventana.append(calcular_f0_cepstrum(senal_en_ventana, freq_muestreo, min_frequency, max_frequency))
        
        else:
            frecuencias_fundamentales_por_ventana.append(0.0)
    
    return frecuencias_fundamentales_por_ventana

# **************************************************************************** #
#                      PARAMETROS Y CARGA DE DATOS                             #
# **************************************************************************** #

# Cargamos la senal a usar y la normalizamos
frecuencia_muestreo, senal = wav.read('./src/funciones_basicas/mujer.wav')
senal = senal.astype('float64') 

senal -= np.mean(senal)
senal /= np.max(np.abs(senal))

# Parametros para deteccion de actividad de voz
umbral_energia : float = 0.01
long_ventana   : int = 2048 # En numero de muestras

porcentaje_solapamiento : float = 0.75
despl_ventana           : int = int(long_ventana * (1 - porcentaje_solapamiento)) # Numeros de muestras que se desplaza la ventana

num_ventanas : int = (len(senal) - long_ventana) // despl_ventana + 1 # Numero de ventanas a procesar

# Vector de tiempo de la senal
duracion_entre_muestras : float = 1 / frecuencia_muestreo
tiempo : np.ndarray = np.linspace(start=0, stop=(len(senal)*duracion_entre_muestras - 1), num=len(senal))

# Vector de tiempos de las ventanas (cada punt es el tiempo final de cada ventana)
tiempo_ventanas : np.ndarray = np.array([
                                            (i * despl_ventana + long_ventana - 1) * duracion_entre_muestras
                                            for i in range(num_ventanas)
                                        ])

# Activaciones de la voz
act_voz_bool  : np.ndarray
energia_senal : np.ndarray
umbral_energia_normalizado : float

act_voz_bool, energia_senal, umbral_energia_normalizado = deteccion_act_voz(senal=senal, 
                                                                            umbral_energia=umbral_energia, 
                                                                            long_ventana=long_ventana, 
                                                                            despl_ventana=despl_ventana)

# Deteccion de sonoridad
valores_cruce_cero   : np.ndarray
clasificacion_sonora : np.ndarray
clasificacion_sorda  : np.ndarray   

valores_cruce_cero, clasificacion_sonora, clasificacion_sorda = deteccion_sonoridad(senal=senal, 
                                                                                    long_ventana=long_ventana, 
                                                                                    despl_ventana=despl_ventana, 
                                                                                    umbral_energia=umbral_energia)

# Deteccion de frecuencia fundamental
frecuencias_fundamentales_por_ventana : np.ndarray = calcular_freq_fundamental_por_ventana(senal=senal, 
                                                                                          freq_muestreo=frecuencia_muestreo, 
                                                                                          long_ventana=long_ventana, 
                                                                                          despl_ventana=despl_ventana,
                                                                                          umbral_energia=umbral_energia)

# **************************************************************************** #
#                             GRAFICAS                                         #
# **************************************************************************** #

N_ROWS : int = 4
N_COLS : int = 1

figura : matplotlib.figure.Figure
ejes   : matplotlib.axes.Axes
figura, ejes = plt.subplots(N_ROWS, N_COLS, figsize=(14, 8))

# Senal en el tiempo
ejes[0].plot(tiempo, senal, label="Señal normalizada en el tiempo")
ejes[0].set_title("Señal normalizada en el tiempo")
ejes[0].set_xlabel("Tiempo [s]")
ejes[0].set_ylabel("Amplitud [V]")
ejes[0].grid()
ejes[0].legend()

# Deteccion de actividad de voz
ejes[1].plot(tiempo_ventanas, energia_senal, label="Energía de la señal")
ejes[1].fill_between(tiempo_ventanas, 0, np.max(energia_senal), where=act_voz_bool, color='yellow', alpha=0.5, label="Voz detectada")
ejes[1].axhline(y = umbral_energia_normalizado, color = "red", linestyle = "--", label="Umbral de energía") 
ejes[1].set_title("Deteccion de actividad de voz")
ejes[1].set_xlabel("Tiempo [s]")
ejes[1].set_ylabel("Energia de la senal")
ejes[1].grid()
ejes[1].legend()

# Sonoridad de la voz
ejes[2].plot(tiempo_ventanas, valores_cruce_cero, label="Tasa de Cruces por Cero (ZCR)")
ejes[2].fill_between(tiempo_ventanas, 0, np.max(valores_cruce_cero), where=clasificacion_sonora, color='yellow', alpha=0.5, label="Voz sonora")
ejes[2].fill_between(tiempo_ventanas, 0, np.max(valores_cruce_cero), where=clasificacion_sorda, color='green', alpha=0.5, label="Voz sorda")
ejes[2].set_title("Deteccion de sonoridad de voz")
ejes[2].set_xlabel("Tiempo [s]")
ejes[2].set_ylabel("ZCR")
ejes[2].grid()
ejes[2].legend()

# Frecuencia fundamental de la voz
ejes[3].plot(tiempo_ventanas, frecuencias_fundamentales_por_ventana, label="Frecuencia fundamental (f0)")
ejes[3].fill_between(tiempo_ventanas, 0, np.max(frecuencias_fundamentales_por_ventana), where=clasificacion_sonora, color='yellow', alpha=0.5, label="Voz sonora")
ejes[3].fill_between(tiempo_ventanas, 0, np.max(frecuencias_fundamentales_por_ventana), where=clasificacion_sorda, color='green', alpha=0.5, label="Voz sorda")
ejes[3].set_title("Deteccion de frecuencia fundamental (f0)")
ejes[3].set_xlabel("Tiempo [s]")
ejes[3].set_ylabel("f0 [Hz]")
ejes[3].grid()
ejes[3].legend()

plt.tight_layout()
plt.show()