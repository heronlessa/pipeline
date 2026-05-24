# SmartShop Cloud — Pipelines Inteligentes com IA

Projeto da atividade **Pipelines Inteligentes com IA aplicada ao DevOps**.  
Simula um ambiente real de CI/CD com agentes de IA tomando decisões automáticas.

---

## Objetivo

Transformar pipelines tradicionais em sistemas autônomos capazes de:
- Analisar qualidade de código
- Interpretar logs e métricas
- Detectar vulnerabilidades de segurança
- Tomar decisões sem intervenção humana

---

## Estrutura do Repositório

```
.github/workflows/     # 3 pipelines GitHub Actions
src/                   # Código da SmartShop + Agente IA
tests/                 # Testes automatizados (pytest)
logs/                  # Logs da aplicação
metrics/               # Métricas do sistema (JSON)
traces/                # Traces distribuídos
security/              # Código para análise de segurança
```

---

## Pipelines

### 1. Quality Gate com IA
Executa os testes, mede cobertura e consulta o **Agente de Testes**.  
- Cobertura ≥ 80% → **APROVADO** → deploy liberado  
- Cobertura < 80% → **BLOQUEADO** → pipeline falha

### 2. Observabilidade Inteligente
Três agentes rodando em paralelo:
- **Agente de Incidente** → analisa logs, cria issue se erro crítico
- **Agente de Custo** → analisa métricas (CPU, memória, latência)
- **Agente de Deploy** → analisa traces e detecta gargalos

### 3. Agente de Segurança
Escaneia o código em busca de vulnerabilidades:
- `eval()`, `exec()` → execução arbitrária de código
- Credenciais hardcoded → vazamento de secrets
- `SELECT *` sem filtro → SQL injection
- `shell=True` → command injection

---

## Como executar localmente

```bash
pip install pytest pytest-cov
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Tecnologias

- Python 3.11
- pytest + pytest-cov
- GitHub Actions
- Agente IA simulado (padrão Strategy)

---

## Resposta à questão da atividade

**Como a IA pode transformar pipelines tradicionais em sistemas autônomos de DevOps?**

Pipelines tradicionais executam etapas fixas e param em caso de erro — sem contexto, sem julgamento. Com IA, o pipeline passa a **interpretar** o que aconteceu e **decidir** o que fazer. Em vez de apenas reportar "cobertura 65%", o agente analisa o risco, bloqueia o deploy automaticamente e sugere onde adicionar testes. Em vez de apenas logar um erro, o agente abre uma issue com o contexto completo. A IA transforma o pipeline de um executor sequencial em um **sistema que raciocina sobre o próprio ambiente** — percebendo, decidindo e agindo sem esperar intervenção humana.
