import numpy as np
import sounddevice as sd

def generate_tone(frecuencia : float, duracion : float, volumen : float = 0.3, frecuencia_muestreo : float = 44100) -> np.ndarray:
    '''
        * frecuencia (Hz): Frecuencia del tono
        * duracion (seg): Duracion del tono
        * volumen (0 a 1): Volumen (amplitud) del tono
        * frecuencia de muestreo (Hz)
    '''

    # Vector de tiempos del tono
    t = np.linspace(0, duracion, int(frecuencia_muestreo * duracion), endpoint=False)
    
    # Valor del tono en cada muestra
    tono : np.ndarray = volumen * np.sin(2 * np.pi * frecuencia * t)

    return tono

if __name__ == "__main__":

    # Rango de frecuencias (en Hz)
    frecuencia_inicial : float = 100
    frecuencia_final : float = 20000

    #  Duracion de cada tono
    duracion : float = 1

    # Frecuencia de muestreo
    frecuencia_muestreo : float = 44100

    # Contador de la frecuencia actual y los Hz en los que va aumentando
    frecuencia_actual : float = frecuencia_inicial
    aumento : int = 100
    while frecuencia_actual <= frecuencia_final:
        # Generamos tono, reproducimos e imprimimos la frecuencia
        tono : np.ndarray = generate_tone(frecuencia_actual, duracion)
        sd.play(tono, frecuencia_muestreo)

        print("FRECUENCIA ACTUAL: " + str(frecuencia_actual))

        frecuencia_actual += aumento