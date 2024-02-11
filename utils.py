import speech_recognition as sr
import numpy as np
import requests
import json
import pygame
from openai import OpenAI
from configs import *


def reconhece_audio(wake_word):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Ajusta para o ruído ambiente
        while True:
            print(f"Aguardando Wake Word {WAKE_WORD}...")
            audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language=IDIOMA)
                print(f"Você disse: {text}")
                if wake_word.lower() in text.lower():
                    print("Wake Word detectada!")
                    
                    saudacao = np.random.choice(SAUDACOES)
                    texto_para_fala(saudacao, idioma=IDIOMA)

                    print("Qual o seu desejo ou dúvida?")
                    prompt_audio = r.listen(source, phrase_time_limit=LIMITE_TEMPO_DUVIDA)
                    prompt_text = r.recognize_google(prompt_audio, language=IDIOMA)
                    print(prompt_text)
                    
                    response = requestGPT4(prompt_text)
                    texto_para_fala(response, idioma=IDIOMA)
                    #break
            except sr.UnknownValueError:
                print("Não entendi. Continue falando...")
                continue


def texto_para_fala(input, idioma='pt-br'):
    arquivo_audio = "response.mp3"

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.audio.speech.create(
        model=MODEL_TTS,
        voice=VOZ_TTS,
        input=input,
    )

    response.stream_to_file(arquivo_audio)
    
    # Inicializa pygame e reproduz o arquivo de áudio
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo_audio)
    pygame.mixer.music.play()

    # Aguarda até que o áudio termine
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Encerra o mixer após a execução do áudio
    pygame.mixer.quit()


def requestGPT4(chunk):
    print("Consultando o GPT...")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    system = PERSONALIDADE_GPT

    params = {
        "model": MODELO_GPT,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": chunk}
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "stop": None
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(params), timeout=180)

        if response.status_code == 429 or response.status_code == 404:
            output = "Meu filho, estou sobrecarregada no momento... Tenta daqui a pouquinho, pode ser?"
            return output
        if response.status_code == 400:
            output = "Eu fiquei confusa. Você poderia repetir, bem?"
            return output
        
        result = json.loads(response.text)

        outputGPT = result['choices'][0]['message']['content']
        output = outputGPT

    except requests.exceptions.Timeout:
        output = "A Maria não está. Ela foi tirar uma soneca no momento..."

    print(output)
    return output