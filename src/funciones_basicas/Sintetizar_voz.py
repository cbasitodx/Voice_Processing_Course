# https://pyttsx3.readthedocs.io/en/latest/engine.html

#pip install pyttsx3

import pyttsx3


# Función para sintetizar y reproducir el texto
def sintetizar_voz(texto):
    print("Sintetizando voz.")
    engine = pyttsx3.init()
    engine.say(texto)
    engine.save_to_file(texto, './src/funciones_basicas/Voz_sintetizada.wav')
    engine.runAndWait()
    print("Voz sintetizada.\n")

sintetizar_voz("uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez")
