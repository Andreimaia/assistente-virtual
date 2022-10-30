from distutils.util import execute
#import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyttsx3
import datetime
import wikipedia
import pywhatkit
#criar um reconhecedor
model=Model('Model')
recognizer=KaldiRecognizer(model,16000)
audio=KaldiRecognizer.Recognizer()
#audio=sr.Recognizer()
maquina= pyttsx3.init()
maquina.say('bom dia ,senhor')
maquina.say('como posso lhe ajudar')
maquina.runAndWait()

def excuta_comando():
    
        #abri meicrofone para captura
        with KaldiRecognizer.Microphone() as source:
       # with sr.Microphone() as source:
        while True:
                 print('Ouvindo...')
                 voz = audio.listen(source)

                 try:
                     comando=audio.recognize_google(voz, language='pt-BR')
                     comando=comando.lower()
                 if'sexta feira' in comando:       
                         comando=comando.replace('sexta feira','')
                         maquina.say(comando )
                         maquina.runAndWait()
                 except
                 print('microfone não esta ok')   

                 return comando 

def comando_voz_usuario():
       comando =excuta_comando()
       if 'horas' in comando:
           hora=datetime.datetime.now().strftime('%H:%M')
           maquina.say('Agora são'+hora)
           maquina.runAndWait()
       elif 'procure por' in comando:
           procurar=comando.replace('procure por','')
           wikipedia.set_lang('pt')
           resultado=wikipedia.summary(procurar,2)
           print(resultado)
           maquina.say(resultado)
           maquina.runAndWait()
       elif 'toque'in comando:
            musica= comando.replace('toque','')
            resultado = pywhatkit.playonyt(musica)
            maquina.say('tocando musica')
            maquina.runAndWait()    

comando_voz_usuario()
