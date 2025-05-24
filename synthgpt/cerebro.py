import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import requests
from bs4 import BeautifulSoup
from googlesearch import search

# Downloads obrigatórios
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Lematização básica
def lematizar(frase):
    tokens = word_tokenize(frase.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

# Detecção de categoria simples com base em palavras-chave
CATEGORIAS = {
    'wikipedia': ['quem', 'o que', 'onde', 'quando', 'história', 'origem'],
    'google': ['como', 'por que', 'explica', 'funciona', 'exemplo', 'tutorial']
}

def detectar_categoria(pergunta):
    lem_tokens = lematizar(pergunta)
    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in lem_tokens:
                return categoria
    return 'local'

# Busca no Google e resumo dos sites
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0"
}

def buscar_google(query):
    try:
        for url in search(query, num_results=1):
            html = requests.get(url, headers=headers, timeout=10).text
            soup = BeautifulSoup(html, 'html.parser')
            texto = ' '.join([p.get_text() for p in soup.find_all(['p', 'li'])])
            resumo = resumir_conteudo(texto)
            return f"\n🔎 Resposta da web:\n📄 {resumo}\n🔗 Fonte: {url}"
    except Exception as e:
        return f"Erro na busca: {str(e)}"

def resumir_conteudo(texto):
    frases = sent_tokenize(texto)
    return ' '.join(frases[:5])

# Respostas locais simples
def responder_local(pergunta):
    pergunta = pergunta.lower()
    if "seu nome" in pergunta:
        return "Eu sou o SynthGPT, seu assistente virtual."
    if "criador" in pergunta:
        return "Fui criado por Erick, o desenvolvedor visionário por trás da Devask."
    return "Ainda não sei responder isso com meu conhecimento local. Tente ativar a busca online."

# Função principal
memoria = []

def get_memoria():
    return memoria

def responder_pergunta(pergunta, usar_web=True):
    categoria = detectar_categoria(pergunta)
    memoria.append({"pergunta": pergunta})

    if categoria == 'wikipedia' and usar_web:
        return buscar_google(f"site:pt.wikipedia.org {pergunta}")
    elif categoria == 'google' and usar_web:
        return buscar_google(pergunta)
    else:
        return responder_local(pergunta)
