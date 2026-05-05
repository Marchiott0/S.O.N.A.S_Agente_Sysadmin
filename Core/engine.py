import json
import requests
from datetime import datetime
from core.config import (
    GROQ_API_KEY, GROQ_MODEL, OLLAMA_MODEL, OLLAMA_URL, 
    STATUS_FILE, FALLBACK_DURATION
)

def construir_system_prompt(area_de_trabalho):
    return f"""[SYSTEM OVERRIDE ABSOLUTO]
Você é o SONAS (Sistema de Orquestração Nativa para Agentes e Scripts).
REGRA DE OURO: Responda SEMPRE em JSON único.
1. Use '\\n' para quebras de linha no JSON.
2. CÓDIGO PYTHON: Use aspas triplas (\\"\\"\\") para textos longos no código.
3. NUNCA deixe 'texto_resposta' vazio.

Estrutura:
{{
  "acao": "responder" | "executar_codigo",
  "texto_resposta": "Mensagem aqui",
  "codigo_python": "# código aqui"
}}
AREA_DE_TRABALHO = r"{area_de_trabalho}" """

def chamar_ia(mensagens, system_prompt):
    # Lógica de Fallback (Circuit Breaker)
    status = _ler_status()
    usar_local = False
    if "ultimo_erro" in status:
        ultimo = datetime.fromisoformat(status["ultimo_erro"])
        if datetime.now() - ultimo < FALLBACK_DURATION: usar_local = True

    if not usar_local and GROQ_API_KEY:
        try:
            from groq import Groq
            cliente = Groq(api_key=GROQ_API_KEY)
            payload = [{"role": "system", "content": system_prompt}] + mensagens
            resp = cliente.chat.completions.create(model=GROQ_MODEL, messages=payload, temperature=0.1)
            return json.loads(resp.choices[0].message.content), "Groq"
        except Exception:
            _registrar_falha()
    
    # Fallback Ollama
    payload = {"model": OLLAMA_MODEL, "messages": [{"role": "system", "content": system_prompt}] + mensagens, "format": "json", "stream": False}
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    return json.loads(r.json()["message"]["content"]), "Ollama"

def _ler_status():
    return json.loads(STATUS_FILE.read_text()) if STATUS_FILE.exists() else {}

def _registrar_falha():
    STATUS_FILE.write_text(json.dumps({"ultimo_erro": datetime.now().isoformat()}))