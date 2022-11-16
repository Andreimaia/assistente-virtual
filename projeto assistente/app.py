from distutils.util import execute
#import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import datetime
import wikipedia
import pywhatkit
#criar um reconhecedor
# model=Model(r'C:\Users\Andrei\Desktop\projeto assistente\Model')
model=Model(model_path='model')
recognizer=KaldiRecognizer(model,16000)

#audio=sr.Recognizer()
#sintese de fala
maquina= pyttsx3.init()
maquina.say('bom dia ,senhor')
maquina.say('como posso lhe ajudar')
maquina.runAndWait()
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
# stream.start_stream()
# while True:
#      data= stream.read(4096)
#      if recognizer.AcceptWaveform(data):
def excuta_comando():
        
            #abri meicrofone para captura
            #with KaldiRecognizer.Microphone() as p :
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
            stream.start_stream()
            while True:
             data= stream.read(4096)
             if recognizer.AcceptWaveform(data):
             #with sr.Microphone() as source:
                
                            print('Ouvindo...')
                            voz = recognizer.listen(p)

                            try:
                                comando=recognizer.recognize_google(voz, language='pt-BR')
                                comando=comando.lower()
                                if'sexta feira' in comando:       
                                        comando=comando.replace('sexta feira','')
                                        maquina.say(comando )
                                        maquina.runAndWait()
                            except:
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
