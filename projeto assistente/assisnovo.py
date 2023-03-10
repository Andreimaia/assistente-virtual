import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configuração das credenciais de API do Spotify
client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Criar um modelo treinado para reconhecimento de fala offline
model = Model('model')
# Criar um reconhecedor usando o modelo criado
recognizer = KaldiRecognizer(model, 16000)

# Inicializar a biblioteca de síntese de fala
maquina = pyttsx3.init()

# Dar as boas-vindas
maquina.say('Como posso lhe ajudar?')
maquina.runAndWait()

# Inicializar a biblioteca de áudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

# Função para sintetizar a fala
def speak(text):
    maquina.say(text)
    maquina.runAndWait()

# Capturar o áudio e reconhecê-lo
while True:
    # Capturar o áudio
    data = stream.read(4000)
    
    # Verificar se o áudio está vazio
    if len(data) == 0:
        break
    
    # Processar o áudio e obter o texto reconhecido
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result = json.loads(result)
        
        # Verificar se o resultado não está vazio
        if result is not None:
            text = result['text']
            
            # Exibir o texto reconhecido
            print(text)
            # Verificar se o comando inclui o nome do programa
            if '' in text:
              # Verificar se a palavra "horas" está presente
              if 'horário' in text:
                # Obter a hora atual do sistema
                hora = datetime.datetime.now().strftime('%H:%M')
                # Sintetizar a hora atual
                maquina.say('Agora são ' + hora)
                maquina.runAndWait()
            elif'pesquise por' in text:
                query=text.replace('procure por','')
                urls=list(search(query,num_results=2))
                if urls:
                    url=urls[0]
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'lxml')
                    ler = soup.get_ler()
                    ler = re.sub('\s+', ' ', ler)
                    print(f"Resultados da pesquisa para '{query}':")
                    print(ler)
                    maquina.say(f"Eu encontrei alguns resultados para '{query}'. O primeiro resultado é:")
                    maquina.say(url)
                    maquina.runAndWait()
                else:
                    print(f"Nenhum resultado encontrado para '{query}'. Tente novamente com uma consulta diferente.")
                    maquina.say(f"Desculpe, eu não consegui encontrar nenhum resultado para '{query}'. Por favor, tente novamente com uma consulta diferente.")
                    maquina.runAndWait()    

                    # Extrair o nome da música do comando de voz
            elif 'toque' in text:
                musica = text.replace('toque', '').strip()

                # Encontrar a música no Spotify
                resultados = sp.search(q=musica, type='track')

                 # Verificar se a música foi encontrada
                if len(resultados['tracks']['items']) > 0:
                    uri = resultados['tracks']['items'][0]['uri']

                    # Reproduzir a música no Spotify
                    sp.start_playback(uris=[uri])

                    # Confirmar que a música está tocando
                    maquina.say(f"Tocando {musica}")
                    maquina.runAndWait()
                else:
                    maquina.say("Não consegui encontrar a música que você pediu.")
                    maquina.runAndWait()




                
