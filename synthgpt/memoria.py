import json
from datetime import datetime

ARQUIVO_MEMORIA = "memoria.json"

def carregar_memoria():
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_interacao(pergunta, resposta, feedback=None):
    memoria = carregar_memoria()
    memoria.append({
        "pergunta": pergunta,
        "resposta": resposta,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    })
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)
