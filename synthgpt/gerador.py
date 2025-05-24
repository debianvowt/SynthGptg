import random
import re

def gerar_resposta(msg, memoria):
    """
    Gera uma resposta com base na mensagem recebida e na memória.
    - msg: string da mensagem do usuário.
    - memoria: instância da classe Memoria.
    """

    msg_lower = msg.lower()

    # 1. Verificar se a mensagem corresponde a algum fato aprendido
    fato = memoria.buscar_fato(msg_lower)
    if fato:
        return fato

    # 2. Respostas básicas e padrões
    respostas_basicas = {
        r"oi|olá|ei|e aí": ["Olá! Como posso ajudar?", "Oi, em que posso ajudar?"],
        r"tchau|adeus|falou": ["Até mais!", "Tchau, volte sempre!"],
        r"como você está\??": ["Estou sempre pronto para ajudar.", "Funcionando 100%, obrigado por perguntar!"],
    }

    for padrao, respostas in respostas_basicas.items():
        if re.search(padrao, msg_lower):
            return random.choice(respostas)

    # 3. Verificar histórico recente para manter contexto
    ultimas = memoria.recuperar_ultimo()
    if ultimas:
        # Simples exemplo: se última resposta foi pergunta, pode usar aqui
        ultima_msg = ultimas[-1]["usuario"].lower()
        if "quem foi" in ultima_msg and "quem foi" not in msg_lower:
            return "Quer saber mais sobre isso? Posso buscar para você."

    # 4. Resposta padrão quando não entendeu
    respostas_fallback = [
        "Desculpe, não entendi muito bem. Pode reformular?",
        "Não sei responder isso ainda, me ensine?",
        "Vamos conversar sobre outro assunto?",
    ]
    return random.choice(respostas_fallback)
