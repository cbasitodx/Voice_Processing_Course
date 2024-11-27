import numpy as np
import sounddevice as sd
import threading

# Parametros de la onda
frequency   : float = 2000  # Frecuencia en Hz
duration    : float = 5.0   # Duración en segundos
sample_rate : float = 44100 # Frecuencia de muestreo (Hz)

# Generamos las ondas
time          : np.ndarray = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
wave_original : np.ndarray = np.sin(2 * np.pi * frequency * time)
wave_inverted : np.ndarray = -np.sin(2 * np.pi * frequency * time)

# Función para reproducir la onda original
def play_original() -> None:
    print("Reproduciendo la onda original...")
    sd.play(wave_original, sample_rate)
    sd.wait()
    print("Reproducción de la onda original terminada.")

# Función para reproducir la onda invertida
def play_inverted() -> None:
    print("Reproduciendo la onda invertida...")
    sd.play(wave_inverted, sample_rate)
    sd.wait()
    print("Reproducción de la onda invertida terminada.")

# Ejecutamos ambas ondas en paralelo usando hilos
thread_original = threading.Thread(target=play_original)
thread_inverted = threading.Thread(target=play_inverted)
    
# Iniciamos ambos hilos
thread_original.start()
thread_inverted.start()
    
# Esperamos a que ambos hilos terminen
thread_original.join()
thread_inverted.join()
print("Ambas ondas se han reproducido.")