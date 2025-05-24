import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

from googlesearch import search
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('portuguese'))
lemmatizer = WordNetLemmatizer()

def lematizar(frase):
    tokens = word_tokenize(frase.lower())
    tokens_filtrados = [token for token in tokens if token.isalnum() and token not in stop_words]
    return [lemmatizer.lemmatize(token) for token in tokens_filtrados]

def detectar_categoria(pergunta):
    lem_tokens = lematizar(pergunta)
    if any(p in lem_tokens for p in ["quem", "quando", "onde", "qual", "quais"]):
        return "fato"
    elif any(p in lem_tokens for p in ["como", "faço", "fazer", "criar", "resolver"]):
        return "tutorial"
    elif any(p in lem_tokens for p in ["vale", "melhor", "bom", "ruim", "opinião"]):
        return "opinião"
    else:
        return "geral"

def responder_local(pergunta):
    categoria = detectar_categoria(pergunta)
    if categoria == "fato":
        return "Pergunta factual detectada. Use a busca web para melhores resultados."
    elif categoria == "tutorial":
        return "Talvez eu consiga te ensinar! Pergunta de tutorial detectada."
    elif categoria == "opinião":
        return "Essa parece ser uma pergunta de opinião. Aqui vai minha visão!"
    else:
        return "Não consegui identificar o tipo da pergunta, mas aqui vai minha tentativa!"

def buscar_no_google_e_resumir(query, num_resultados=1):
    resultados = search(query, num_results=num_resultados)
    descricoes = []

    for url in resultados:
        try:
            resposta = requests.get(url, timeout=5)
            soup = BeautifulSoup(resposta.content, 'html.parser')
            texto = ' '.join([p.get_text() for p in soup.find_all('p')])
            resumo = texto[:1000]  # Limite para não ultrapassar resposta
            descricoes.append(f"🔗 **Fonte:** {url}\n📄 **Resumo:**\n{resumo}")
        except Exception as e:
            descricoes.append(f"❌ Erro ao acessar {url}: {str(e)}")

    return "\n\n".join(descricoes)

def responder_pergunta(pergunta, usar_busca_web=False):
    if usar_busca_web:
        return buscar_no_google_e_resumir(pergunta)
    else:
        return responder_local(pergunta)

def get_memoria():
    return "Função de memória ainda em desenvolvimento."
