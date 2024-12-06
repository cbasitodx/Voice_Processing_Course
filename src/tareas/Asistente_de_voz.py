import speech_recognition as sr
import numpy as np
import sounddevice as sd
import sys
import re
import keyboard
from gtts import gTTS             # pip install gtts (Utilizaremos esta en vez de pyttsx3 porque nos ha dado mejores resultados en Pop_OS!, que fue el OS en el que se desarrollo el codigo)
# from pydub import AudioSegment  # pip install pydub (Utilizaremos estas para trabajar con formato mp3, pues gtts no permite guardar a wav)

class Asistente:
    '''
        Asistente de matemáticas que resuelve operaciones sencillas de suma, resta, multiplicación y división.
    '''
    def __init__(self,
                 frecuencia_muestreo : float,
                 lang : str,
                 gender : str,
                 device_index : int):
        '''
            Constructor del objeto Asistente.

            Params:
                * frecuencia_muestreo : frecuencia de muestreo del dispositivo de grabacion de audio
                * lang : Lenguage que va a esperar el modelo, y en el que va a responder. Por ejemplo, "es-ES"
                * gender: Género de la voz del modelo
                * device_index : Número que representa al dispositivo de grabación de audio. Para ver los indices, ejecutar print(sd.query_devices()) y buscar 2 in 0 out 
        '''
        
        # Guardamos los argumentos de entrada
        self.frecuencia_muestreo : float = frecuencia_muestreo
        self.lang : str = lang
        self.gender : str = gender
        self.device_index : int = device_index

        # Instanciamos el modelo reconocedor de la voz
        self.recognizer : sr.Recognizer = sr.Recognizer()

    def grabar_audio(self) -> np.ndarray:
        '''
            Da la pauta para grabar audio. Devuelve un array de numpy con los valores del audio grabado.
        '''

        # Esperamos la senal del usuario para empezar a grabar
        input("Pulsa la tecla 'Enter' para empezar la grabacion. Pulsa la tecla 'espacio' para detener la grabación.")

        # Lista para almacenar los fragmentos de voz grabados
        audio_grabado : list = []

        # Función de callback para grabar voz
        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            audio_grabado.append(indata.copy())  # Agregar el fragmento grabado a la lista

        # Iniciar la grabación
        with sd.InputStream(samplerate=self.frecuencia_muestreo, channels=1, dtype='int16', callback=callback, device=self.device_index):
            keyboard.wait('space')  # Esperar a que se suelte la tecla 'espacio'

        # Convertir la lista de fragmentos a un arreglo numpy y devolverlo
        audio_grabado : np.ndarray = np.concatenate(audio_grabado, axis=0)
        print("Grabación finalizada.\n")
        return audio_grabado

    def transcribir_voz(self, voz : np.ndarray) -> str:
        '''
            Haciendo uso de un modelo de DL de google, transcribe un audio (que viene dado como un array de numpy). 
            Devuelve un string con la transcripcion
        '''

        # Transformamos la voz a un objeto AudioData con sus bytes
        voz_data : sr.AudioData  = sr.AudioData(voz.tobytes(), self.frecuencia_muestreo, 2)        

        # Intentamos hacer la transcripcion y guardarla en 'texto'. Si no es posible, devolvemos una cadena vacia
        try:
            texto : str = self.recognizer.recognize_google(voz_data, language=self.lang)
            return texto
        
        except sr.UnknownValueError:
            print("No se pudo entender la voz.\n")
            return ""
        
        except sr.RequestError as e:
            print("Error con el servicio de reconocimiento de voz; {0}\n".format(e))
            return ""

    def sintetizar_voz(self, texto : str ) -> None:
        '''
            Dado un string, sintetiza este string mediante una voz computarizada.
            Para ello, se obtiene el audio de la sintetis en un fichero temporal mp3, luego se convierte a una array de numpy,
            se reproduce y, finalmente, se elimina.
        '''

        # Generamos la pista de audio en formato mp3 con tts de la voz sintetizada
        tts = gTTS(text=texto, lang=self.lang[0:2])
        tts.save("./.temp_sint.mp3")

        # # La leemos en un objeto AudioSegment, al cual le ajustamos la frecuencia de muestreo y ponemos en mono
        # audio : AudioSegment = AudioSegment.from_mp3("./.temp_sint.mp3")
        # audio = audio.set_frame_rate(self.frecuencia_muestreo)
        # audio = audio.set_channels(1)
        
        # # Convertimos esa pista de audio a un numpy array con sus valores entre -1 y 1
        # voz : np.ndarray = np.array(audio.get_array_of_samples(), dtype=np.float32) / (2**15) 

        # # Reproducimos la pista usando un array de numpy
        # sd.play(voz, self.frecuencia_muestreo)
        # sd.wait()

        # # Eliminamos el fichero mp3 residual
        # os.remove('./.temp_sint.mp3')

    def resolver_operacion(self, pregunta : str) -> str:
        '''
            Dada una pregunta de matematicas elementales (que viene dada como un string), devuelve una respuesta a la misma.
            La respuesta viene dada como un string. Si la pregunta no es válida o no se entendió, se devuelve un string acorde
        '''
        
        # Mediante expresiones regulares, buscamos todos los digitos en la pregunta
        numeros : list[str] = re.findall(r'\d+', pregunta)

        # Asegurarse de que hay al menos dos numeros
        if len(numeros) < 2:
            return "No entendí la operación. Proporcione al menos dos números."
        
        # Si hay mas de dos, tomamos los dos primeros
        num1 = int(numeros[0])
        num2 = int(numeros[1])

        # Detectamos la operacion y, si hemos podido detectarla, retornamos el resultado
        palabras : list[str] = pregunta.lower().split()
        
        if "+" in palabras or "más" in palabras or "suma" in palabras or "sumo" in palabras or "agrega" in palabras or "agrego" in palabras:
            return f"El resultado de {num1} más {num2} es {num1 + num2}."
        
        elif "-" in palabras or "menos" in palabras or "resta" in palabras or "resto" in palabras or "quita" in palabras or "quito" in palabras:
            return f"El resultado de {num1} menos {num2} es {num1 - num2}."
        
        elif "*" in palabras or "por" in palabras or "multiplica" in palabras or "multiplico" in palabras:
            return f"El resultado de {num1} por {num2} es {num1 * num2}."
        
        elif "/" in palabras or "entre" in palabras or "divide" in palabras or "divido" in palabras:
            if num2 == 0:
                return "No se puede dividir entre cero."
            return f"El resultado de {num1} entre {num2} es {num1 / num2}."

        else:
            return "No entendí la operación. Por favor, pregunta sobre sumas, restas, multiplicaciones o divisiones."

# Bucle de ejecucion principal
if __name__=="__main__":

    print("Bienvenido al asistente de matematicas! Por favor, indica una operación básica (como suma, resta, multiplicación o división) a realizar. Si deseas salir, di 'Salir'")

    # Creamos al asistente
    asistente : Asistente = Asistente(frecuencia_muestreo=48000, lang="es-ES", gender="male", device_index=8)

    # Variable donde almacenaremos el audio grabado del usuario
    voz : np.ndarray

    # Variable donde almacenaremos la transcripcion de la voz
    voz_transcrita : str

    # Variable donde almacenaremos la respuesta del asistente
    respuesta : str

    while True:
        # Grabamos el audio del usuario
        voz = asistente.grabar_audio()

        # Obtenemos la transcripcion
        voz_transcrita = asistente.transcribir_voz(voz)

        # Detectamos si el usuario quiere dejar de usar al asistente
        palabras : list[str] = voz_transcrita.lower().split()

        if "salir" in palabras:
            print("Gracias por usar al asistente de matemáticas!")
            break

        # Usando la transcripcion, obtenemos una respuesta
        respuesta = asistente.resolver_operacion(voz_transcrita)

        # Sintetizamos la respuesta 
        asistente.sintetizar_voz(respuesta)