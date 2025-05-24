import re
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from googlesearch import search
import wikipedia

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()

# Função de lematização segura
def lematizar(frase):
    tokens = tokenizer.tokenize(frase.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

# Classificação simples por palavra-chave
def detectar_categoria(pergunta):
    tokens = lematizar(pergunta)
    if any(word in tokens for word in ['quem', 'quando', 'onde', 'por', 'como', 'história', 'biografia']):
        return 'wikipedia'
    elif any(word in tokens for word in ['site', 'google', 'buscar', 'pesquisar', 'traduzir', 'link']):
        return 'google'
    else:
        return 'local'

# Resposta local simples
def responder_local(pergunta):
    if 'oi' in pergunta.lower():
        return "Olá! Como posso te ajudar?"
    elif 'tudo bem' in pergunta.lower():
        return "Estou bem! E você?"
    return "Desculpe, ainda estou aprendendo. Pode reformular?"

# Resposta usando Wikipedia
def responder_wikipedia(pergunta):
    try:
        wikipedia.set_lang("pt")
        resumo = wikipedia.summary(pergunta, sentences=2)
        return f"📚 {resumo}"
    except:
        return "Não encontrei nada na Wikipédia."

# Busca no Google e descreve o conteúdo
def responder_google(pergunta):
    try:
        for url in search(pergunta, num_results=1, lang="pt"):
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            titulo = soup.title.string.strip() if soup.title else "Sem título"
            paragrafos = soup.find_all('p')
            conteudo = ' '.join(p.get_text() for p in paragrafos if len(p.get_text()) > 60)
            resumo = conteudo.strip().replace('\n', ' ')[:600] + "..." if conteudo else "Não foi possível resumir o site."

            return f"🔗 **Fonte:** {url}\n📄 **Resumo:** {titulo} — {resumo}"
        return "Nenhum resultado encontrado no Google."
    except Exception as e:
        return f"Erro ao acessar a web: {str(e)}"

# Função principal
def responder_pergunta(pergunta, usar_web=False):
    categoria = detectar_categoria(pergunta)
    if categoria == 'local':
        return responder_local(pergunta)
    elif categoria == 'wikipedia':
        return responder_wikipedia(pergunta)
    elif categoria == 'google' or usar_web:
        return responder_google(pergunta)
    else:
        return "Não entendi sua pergunta."
