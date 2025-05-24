import requests
from bs4 import BeautifulSoup

def buscar_wikipedia(termo):
    try:
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo}"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get("extract", "Sem resumo disponível na Wikipedia.")
        else:
            return None
    except Exception:
        return None

def buscar_duckduckgo(termo):
    try:
        url = f"https://api.duckduckgo.com/?q={termo}&format=json&no_redirect=1"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            texto = dados.get("AbstractText", "")
            return texto if texto else None
        else:
            return None
    except Exception:
        return None

def buscar_multifonte(termo):
    # Tenta Wikipedia primeiro
    resultado = buscar_wikipedia(termo)
    if resultado:
        return resultado
    
    # Se não achar na Wikipedia, tenta DuckDuckGo
    resultado = buscar_duckduckgo(termo)
    if resultado:
        return resultado

    return "Desculpe, não consegui encontrar informações sobre isso."
