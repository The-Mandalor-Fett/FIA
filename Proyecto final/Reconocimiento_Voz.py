import speech_recognition as sr
import webbrowser as wb
import pyttsx3


def Reconocer_voz():
    sr.Microphone(device_index = 0) #INICIALIZA EL MICRÓFONO 0 = POR DEFECTO
    print("Micrfono encontrado en la PC:  \n {sr.Microphone.list_micophpne_names()}")
    #CREAMOS UN OBJETO DE RECONOCIMIENTO
    reconocimiento = sr.Recognizer()
    
    def hablar(frase,texto):
        engine = pyttsx3.init()
        voces = engine.getProperty('voices')
        engine.setProperty('Voz',voces[0].id)
        engine.say(texto)
        engine.say(frase)
        engine.runAndWait()

    '''index = 0
        for voice in voces:
        print(f'index-> {index} -- {voice.name}')
        index +=1'''


    reconocimiento.energy_threshold = 50000 #TENEMOS VALORES DE 150 A 4000 son los buenos, PONEMOS EL QUE QUEDE
    reconocimiento.dynamic_energy_threshold = False

    with sr.Microphone() as source:
        print("Por favor hable fuerte y claro: ")
        reconocimiento.adjust_for_ambient_noise(source) #REDUCE EL RUIDO AMBIENTAL
        audioDelMicrofono = reconocimiento.listen(source) #TOMA LA VOZ DEL MICRÓFONO
        try:
            frase = reconocimiento.recognize_google(audioDelMicrofono, language = "es-MX")
            texto = "Dijiste algo como?"
            hablar(frase,texto)
            url = "https://www.google.com/search?q="
            buscar  = url + frase
            #wb.open(buscar)
        except TimeoutException as msg:
            print(msg)
        except WaitTimeoutError:
            print("Tardaste mucho en hablar")
            quit()
        # SI NO ENTIENDE EL AUDIO   
        except LookupError:
            print("No entendí lo que quisiste decir")
        else:
            print("Tu resultado se mostrará en un momento. Adiós :) ")


Reconocer_voz()
#pip install pipwin
#pipwin install pyaudio
#pip uninstall pipwin