import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

import random
import wikipedia
from googlesearch import search
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

wikipedia.set_lang("pt")

lemmatizer = WordNetLemmatizer()

# Memória simples de contexto (pode ser expandida)
memoria_contexto = []

respostas_base = {
    "oi": ["Olá!", "Oi, como posso ajudar?", "E aí!"],
    "tudo bem": ["Estou bem, obrigado!", "Tudo ótimo por aqui! E você?"],
    "quem é você": ["Eu sou o SynthGPT, seu assistente inteligente."],
    "obrigado": ["De nada!", "Por nada, sempre à disposição!"],
    "default": ["Não entendi muito bem, pode reformular?", "Não sei a resposta, mas vou tentar buscar na web."]
}

palavras_chave = {
    "saudacao": ["oi", "olá", "e aí", "ola"],
    "agradecimento": ["obrigado", "valeu"],
    "pergunta_geral": ["quem", "o que", "quando", "onde", "por que", "como"],
}

def lematizar(frase):
    tokens = word_tokenize(frase.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def detectar_categoria(pergunta):
    lem_tokens = lematizar(pergunta)
    for categoria, palavras in palavras_chave.items():
        if any(p in lem_tokens for p in palavras):
            return categoria
    return "desconhecido"

def responder_local(pergunta):
    categoria = detectar_categoria(pergunta)
    lem = lematizar(pergunta)
    for chave, respostas in respostas_base.items():
        if chave in lem:
            return random.choice(respostas)
    try:
        resumo = wikipedia.summary(pergunta, sentences=2)
        return resumo
    except:
        return None

def buscar_google(pergunta):
    try:
        resultados = list(search(pergunta, num_results=1))
        if resultados:
            return f"Encontrei isso no Google: {resultados[0]}"
        return "Não encontrei nada relevante no Google."
    except Exception as e:
        return f"Erro ao pesquisar no Google: {e}"

def responder_pergunta(pergunta, usar_busca_web=False):
    global memoria_contexto
    memoria_contexto.append({"pergunta": pergunta})

    resposta = responder_local(pergunta)
    if resposta:
        memoria_contexto.append({"resposta": resposta})
        return resposta

    if usar_busca_web:
        resposta_web = buscar_google(pergunta)
        memoria_contexto.append({"resposta": resposta_web})
        return resposta_web

    resposta = respostas_base["default"][0]
    memoria_contexto.append({"resposta": resposta})
    return resposta

def get_memoria():
    texto = ""
    for item in memoria_contexto:
        if "pergunta" in item:
            texto += f"Você: {item['pergunta']}\n"
        elif "resposta" in item:
            texto += f"SynthGPT: {item['resposta']}\n"
    return texto
