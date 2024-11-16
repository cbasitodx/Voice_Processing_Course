# https://pypi.org/project/SpeechRecognition/

#pip install scipy SpeechRecognition

import scipy.io.wavfile as wav
import speech_recognition as sr


# Función para transcribir voz a texto
def transcribir_voz(voz, frecuencia_muestreo = 44100):
    print("Transcribiendo voz (esta función requiere una conexión a internet)")
    recognizer = sr.Recognizer()
    voz_data = sr.AudioData(voz.tobytes(), frecuencia_muestreo, 2)
    try:
        texto = recognizer.recognize_google(voz_data, language="es-ES")
        # texto = recognizer.recognize_google(voz_data, language="en-EN")
        print("Transcripción: " + texto + "\n")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender la voz.\n")
        return ""
    except sr.RequestError as e:
        print("Error con el servicio de reconocimiento de voz; {0}\n".format(e))
        return ""



#Cargar audio con frecuencia de muestreo.
frecuencia_muestreo, voz = wav.read('./src/funciones_basicas/hombre.wav')

texto = transcribir_voz(voz, frecuencia_muestreo)
