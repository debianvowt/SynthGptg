import re

# Lista simples de stopwords em português (você pode expandir)
STOPWORDS_PT = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para",
    "é", "com", "não", "uma", "os", "no", "se", "na", "por",
    "mais", "as", "dos", "como", "mas", "foi", "ao", "ele",
    "das", "tem", "à", "seu", "sua", "ou", "ser", "quando",
    "muito", "há", "nos", "já", "está", "eu", "também", "só",
    "pelo", "pela", "até", "isso", "ela", "entre", "depois",
    "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me",
    "esse", "eles", "estão", "você", "tinha", "foram", "essa",
    "num", "nem", "suas", "meu", "às", "minha", "têm", "numa",
    "pelos", "elas", "havia", "seja", "qual", "será", "nós",
    "tenho", "lhe", "deles", "essas", "esses", "pelas", "este",
    "fosse", "dele", "tu", "te", "vocês", "vos", "lhes", "meus",
    "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa",
    "nossos", "nossas", "dela", "delas", "esta", "estes", "estas",
    "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo",
    "estou", "está", "estamos", "estão", "estive", "esteve",
    "estivemos", "estiveram", "estava", "estávamos", "estavam",
    "estivera", "estivéramos", "esteja", "estejamos", "estejam",
    "estivesse", "estivéssemos", "estivessem", "estiver", "estivermos",
    "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos",
    "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam",
    "houvesse", "houvéssemos", "houvessem", "houver", "houvermos",
    "houverem", "houverei", "houverá", "houveremos", "houverão",
    "houveria", "houveríamos", "houveriam", "sou", "somos", "são",
    "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora",
    "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem",
    "for", "formos", "forem", "serei", "será", "seremos", "serão",
    "seria", "seríamos", "seriam", "tenho", "tem", "temos", "têm",
    "tinha", "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram",
    "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse",
    "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei",
    "terá", "teremos", "terão", "teria", "teríamos", "teriam"
}

def limpar_texto(texto):
    """
    Remove caracteres especiais, números e deixa só letras e espaços.
    """
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúãõâêîôûç\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def tokenizar(texto):
    """
    Separa o texto em palavras.
    """
    return texto.split()

def remover_stopwords(palavras):
    """
    Remove stopwords do texto tokenizado.
    """
    return [p for p in palavras if p not in STOPWORDS_PT]

def stemmer(palavras):
    """
    Stemming básico: reduz palavras ao radical simples, cortando sufixos comuns.
    Isso não é tão avançado quanto Porter Stemmer, mas funciona para demos simples.
    """
    sufixos = ['mente', 'ções', 'ção', 'mente', 'mente', 'mente', 'mente', 'mente',
               'mente', 'mente', 'mente', 'mente', 'mente', 'mente', 'mente', 'mente',
               'ar', 'er', 'ir', 'os', 'as', 'ais', 'eis', 'óis', 'is', 'am', 'em',
               'am', 'avam', 'iam', 'ado', 'ido', 'ando', 'endo', 'indo', 'ou', 'ar',
               'er', 'ir']
    radicais = []
    for palavra in palavras:
        raiz = palavra
        for sufixo in sufixos:
            if palavra.endswith(sufixo) and len(palavra) > len(sufixo) + 2:
                raiz = palavra[:-len(sufixo)]
                break
        radicais.append(raiz)
    return radicais

def preprocessar_texto(texto):
    """
    Pipeline completa: limpar, tokenizar, remover stopwords, stemmer.
    Retorna lista de radicais.
    """
    texto_limpo = limpar_texto(texto)
    tokens = tokenizar(texto_limpo)
    tokens_sem_stopwords = remover_stopwords(tokens)
    radicais = stemmer(tokens_sem_stopwords)
    return radicais


# Teste simples
if __name__ == "__main__":
    frase = "Quem foi Albert Einstein e qual a importância dele para a física moderna?"
    print("Original:", frase)
    print("Pré-processado:", preprocessar_texto(frase))
