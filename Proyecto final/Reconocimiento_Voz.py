import speech_recognition as sr
import webbrowser as wb

def Reconocer_voz():
    sr.Microphone(device_index = 0) #INICIALIZA EL MICRÓFONO 0 = POR DEFECTO
    print("Micrfono encontrado en la PC:  \n {sr.Microphone.list_micophpne_names()}")
    

