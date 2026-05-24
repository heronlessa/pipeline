# src/ai_agent.py
# Agente de IA simulado para os pipelines da SmartShop Cloud
# Em produção: substituir por chamada real à API da Anthropic/OpenAI

import json
import sys


def analisar_qualidade(cobertura: float) -> dict:
    """Agente de Testes — decide APROVADO ou BLOQUEADO com base na cobertura."""
    if cobertura >= 80:
        status = "APROVADO"
        risco = "BAIXO"
        mensagem = (
            f"Cobertura de {cobertura:.1f}% está acima do threshold de 80%. "
            "Pipeline liberada para deploy."
        )
    elif cobertura >= 60:
        status = "BLOQUEADO"
        risco = "MÉDIO"
        mensagem = (
            f"Cobertura de {cobertura:.1f}% está abaixo do mínimo de 80%. "
            "Recomendado adicionar testes antes do deploy."
        )
    else:
        status = "BLOQUEADO"
        risco = "ALTO"
        mensagem = (
            f"Cobertura de {cobertura:.1f}% está criticamente baixa. "
            "Deploy bloqueado. Adicione testes urgentemente."
        )
    return {"status": status, "risco": risco, "mensagem": mensagem, "cobertura": cobertura}


def analisar_logs(conteudo_log: str) -> dict:
    """Agente de Incidente — interpreta logs e decide se cria issue."""
    linhas = conteudo_log.strip().splitlines()
    erros_criticos = [l for l in linhas if "CRITICAL" in l or "ERROR" in l]
    criar_issue = len(erros_criticos) > 0

    if erros_criticos:
        resumo = f"Encontrados {len(erros_criticos)} evento(s) crítico(s): " + "; ".join(erros_criticos[:3])
        severidade = "CRÍTICA" if any("CRITICAL" in l for l in erros_criticos) else "ALTA"
    else:
        resumo = "Nenhum erro crítico encontrado nos logs."
        severidade = "NORMAL"

    return {
        "criar_issue": criar_issue,
        "severidade": severidade,
        "resumo": resumo,
        "total_erros": len(erros_criticos),
    }


def analisar_metricas(metricas: dict) -> dict:
    """Agente de Custo/Observabilidade — detecta degradação de performance."""
    alertas = []
    if metricas.get("cpu", 0) > 85:
        alertas.append(f"CPU crítica: {metricas['cpu']}%")
    if metricas.get("memory", 0) > 85:
        alertas.append(f"Memória crítica: {metricas['memory']}%")
    if metricas.get("latency_ms", 0) > 2000:
        alertas.append(f"Latência alta: {metricas['latency_ms']}ms")

    risco = "CRÍTICO" if len(alertas) >= 2 else "ALTO" if alertas else "NORMAL"
    return {
        "risco": risco,
        "alertas": alertas,
        "acao": "ESCALAR INCIDENTE" if risco == "CRÍTICO" else "MONITORAR" if risco == "ALTO" else "OK",
    }


def analisar_traces(trace: str) -> dict:
    """Agente de Deploy — detecta gargalos no trace distribuído."""
    servicos = [s.strip() for s in trace.split("->")]
    gargalo = None

    problemas_conhecidos = ["Payment Service", "Database", "Auth Service"]
    for servico in servicos:
        if any(p in servico for p in problemas_conhecidos):
            gargalo = servico
            break

    return {
        "gargalo": gargalo or "Nenhum",
        "servicos": servicos,
        "recomendacao": f"Investigar '{gargalo}'" if gargalo else "Trace saudável",
    }


def analisar_seguranca(codigo: str) -> dict:
    """Agente de Segurança — detecta vulnerabilidades no código."""
    vulnerabilidades = []
    padroes = {
        "eval(":        "Uso de eval() — risco de execução de código arbitrário",
        "exec(":        "Uso de exec() — risco de execução de código arbitrário",
        "password":     "Possível credencial hardcoded",
        "secret":       "Possível secret hardcoded",
        "SELECT *":     "SQL sem filtro — risco de SQL injection",
        "shell=True":   "subprocess com shell=True — risco de command injection",
    }
    for padrao, descricao in padroes.items():
        if padrao.lower() in codigo.lower():
            vulnerabilidades.append(descricao)

    return {
        "vulnerabilidades": vulnerabilidades,
        "total": len(vulnerabilidades),
        "status": "REPROVADO" if vulnerabilidades else "APROVADO",
    }


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "qualidade"

    if modo == "qualidade":
        cobertura = float(sys.argv[2]) if len(sys.argv) > 2 else 85.0
        resultado = analisar_qualidade(cobertura)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        sys.exit(0 if resultado["status"] == "APROVADO" else 1)

    elif modo == "logs":
        conteudo = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
        resultado = analisar_logs(conteudo)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        sys.exit(1 if resultado["criar_issue"] else 0)

    elif modo == "metricas":
        metricas = json.loads(open(sys.argv[2]).read()) if len(sys.argv) > 2 else {}
        resultado = analisar_metricas(metricas)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        sys.exit(1 if resultado["risco"] == "CRÍTICO" else 0)

    elif modo == "traces":
        trace = open(sys.argv[2]).read().strip() if len(sys.argv) > 2 else ""
        resultado = analisar_traces(trace)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    elif modo == "seguranca":
        codigo = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
        resultado = analisar_seguranca(codigo)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        sys.exit(1 if resultado["status"] == "REPROVADO" else 0)
