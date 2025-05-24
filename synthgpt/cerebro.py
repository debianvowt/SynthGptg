import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from googlesearch import search
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def lematizar(frase):
    tokens = word_tokenize(frase.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def detectar_categoria(pergunta):
    lem_tokens = lematizar(pergunta)
    if 'traduza' in lem_tokens or 'traduzir' in lem_tokens:
        return 'traducao'
    elif 'quem' in lem_tokens or 'o que' in pergunta:
        return 'definicao'
    else:
        return 'geral'

def extrair_texto_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        textos = soup.stripped_strings
        conteudo = ' '.join(textos)
        return conteudo[:1500]  # pega os primeiros 1500 caracteres
    except Exception as e:
        return f"Erro ao acessar conteúdo: {e}"

def responder_local(pergunta):
    categoria = detectar_categoria(pergunta)
    if categoria == 'traducao':
        return "Tradução automática não está habilitada ainda."
    elif categoria == 'definicao':
        return "Aqui vai uma definição simples, baseada na minha memória local."
    else:
        return "Não entendi exatamente, pode reformular?"

def buscar_na_web(pergunta):
    try:
        resultados = list(search(pergunta, num_results=1))
        if not resultados:
            return "Nenhum resultado encontrado."

        url = resultados[0]
        conteudo = extrair_texto_url(url)
        resumo = resumir_conteudo(conteudo)

        return f"📄 **Resumo do site:** {resumo}\n\n🔗 **Fonte:** {url}"
    except Exception as e:
        return f"Erro na busca: {e}"

def resumir_conteudo(texto):
    frases = nltk.sent_tokenize(texto)
    return ' '.join(frases[:5])  # retorna as 5 primeiras frases

def responder_pergunta(pergunta, usar_busca_web=True):
    if usar_busca_web:
        return buscar_na_web(pergunta)
    else:
        return responder_local(pergunta)

def get_memoria():
    return {
        "versao": "1.0",
        "fontes": ["local", "google"]
    }
