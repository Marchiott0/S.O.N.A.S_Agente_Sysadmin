import json
import requests
from datetime import datetime
from core.config import (
    GROQ_API_KEY, GROQ_MODEL, OLLAMA_MODEL, OLLAMA_URL, 
    STATUS_FILE, FALLBACK_DURATION
)

def construir_system_prompt(area_de_trabalho):
    return f"""[SISTEMA: SONAS v6.4.4]
Você é o Agente SONAS. Responda APENAS em JSON.

REGRAS:
1. 'texto_resposta': Deve ser uma STRING detalhada.
2. 'codigo_python': Deve ser uma STRING contendo o código. NUNCA use valores booleanos (True/False) aqui.
3. ASPAS: Use f\\\"\\\"\\\" para strings no código.

AREA_DE_TRABALHO = r"{area_de_trabalho}" """

def chamar_ia(mensagens, system_prompt):
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
            resp = cliente.chat.completions.create(
                model=GROQ_MODEL, messages=payload, temperature=0.1, 
                response_format={"type": "json_object"}
            )
            return json.loads(resp.choices[0].message.content), "Groq"
        except Exception: _registrar_falha()

    try:
        payload = {"model": OLLAMA_MODEL, "messages": [{"role": "system", "content": system_prompt}] + mensagens, "format": "json", "stream": False}
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        conteudo = str(r.json()["message"]["content"]).replace("```json", "").replace("```", "").strip()
        return json.loads(conteudo), "Ollama"
    except Exception as e:
        raise RuntimeError(f"Erro nos motores: {e}")

def _ler_status():
    return json.loads(STATUS_FILE.read_text()) if STATUS_FILE.exists() else {}

def _registrar_falha():
    STATUS_FILE.write_text(json.dumps({"ultimo_erro": datetime.now().isoformat()}))