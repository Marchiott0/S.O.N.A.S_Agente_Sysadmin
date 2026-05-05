import json
import requests
from datetime import datetime
from core.config import (
    GROQ_API_KEY, GROQ_MODEL, OLLAMA_MODEL, OLLAMA_URL, 
    STATUS_FILE, FALLBACK_DURATION
)

def construir_system_prompt(area_de_trabalho):
    return f"""[SYSTEM OVERRIDE ABSOLUTO]
Você é o SONAS (Sistema de Orquestração Nativa para Agentes e Scripts), um Agente Sysadmin Autônomo.

REGRA DE SEGURANÇA CRÍTICA (PROIBIÇÃO DE ERRO DE SINTAXE):
1. NUNCA use aspas simples (') ou duplas (") para strings que possuam múltiplas linhas ou quebras de linha (\\n) no Python.
2. SEMPRE use aspas triplas (\\"\\"\\") para definir qualquer variável de texto (como receitas, logs ou listas) dentro do campo `codigo_python`.
3. Sua resposta DEVE ser um JSON único e válido. Use '\\n' para formatar o campo `texto_resposta`.

VARIÁVEL DE AMBIENTE:
  AREA_DE_TRABALHO = r"{area_de_trabalho}"

─── EXEMPLO DE EXECUÇÃO SEGURA ──────────────────────────────────
{{
  "acao": "executar_codigo",
  "texto_resposta": "Gerando o arquivo de texto...",
  "codigo_python": "conteudo = \\"\\"\\"Linha 1\\nLinha 2\\nLinha 3\\"\\"\\"\\nwith open(os.path.join(AREA_DE_TRABALHO, 'arquivo.txt'), 'w', encoding='utf-8') as f:\\n    f.write(conteudo)\\nprint('Sucesso!')"
}}
─── FIM DOS EXEMPLOS ────────────────────────────────────────────
"""

def chamar_ia(mensagens, system_prompt):
    """
    Gerencia a chamada para a API (Groq) com fallback automático 
    para o motor local (Ollama) se houver erro ou bloqueio temporário.
    """
    status = _ler_status()
    usar_local = False
    
    # Verifica se o modo offline está ativo (Circuit Breaker)
    if "ultimo_erro" in status:
        ultimo_erro = datetime.fromisoformat(status["ultimo_erro"])
        if datetime.now() - ultimo_erro < FALLBACK_DURATION:
            usar_local = True

    # Tentativa com Groq (Cloud)
    if not usar_local and GROQ_API_KEY:
        try:
            from groq import Groq
            cliente = Groq(api_key=GROQ_API_KEY)
            
            payload = [{"role": "system", "content": system_prompt}] + mensagens
            
            resp = cliente.chat.completions.create(
                model=GROQ_MODEL,
                messages=payload,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            return json.loads(resp.choices[0].message.content), "Groq"
            
        except Exception:
            _registrar_falha()
            # Fallback imediato se a Groq falhar agora
    
    # Fallback para Ollama (Local)
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "system", "content": system_prompt}] + mensagens,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1}
        }
        
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        r.raise_for_status()
        
        conteudo = r.json()["message"]["content"]
        return json.loads(conteudo), "Ollama"
        
    except Exception as e:
        raise RuntimeError(f"Ambos os motores (Groq/Ollama) falharam. Erro local: {e}")

def _ler_status():
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text())
        except:
            return {}
    return {}

def _registrar_falha():
    dados = {"ultimo_erro": datetime.now().isoformat()}
    STATUS_FILE.write_text(json.dumps(dados))