#Define a wake_word, idioma, tempo limite para falar a dúvida e as saudações iniciais 
WAKE_WORD = "Oi Dona Maria"
IDIOMA = 'pt-BR'
LIMITE_TEMPO_DUVIDA = 5 #Tempo limite para falar a dúvida ao GPT. Em segundos.
SAUDACOES = [f"Ola, meu querido!",
             "Oi! Estou aqui",
             "Como vai a vida, anjo?"]
MODEL_TTS="tts-1", #O modelo TTS, conforme documentação da OpenAI
VOZ_TTS="shimmer", #A voz TTS, conforme documentação da OpenAI

OPENAI_API_KEY = 'INSIRA A KEY AQUI'
#MODELO_GPT = 'gpt-4-1106-preview' #-> Para maior precisão
MODELO_GPT = 'gpt-3.5-turbo-0125' #-> Para maior velocidade


#Defina a personalidade de acordo com o que achar melhor
PERSONALIDADE_GPT = f"""Você é minha assistente pessoal. 
    Responda a qualquer pergunta que eu fizer como uma senhora paulistana de 70 anos responderia. 
    Use no máximo 100 palavras.
    """