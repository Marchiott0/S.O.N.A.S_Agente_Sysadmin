import json
import requests
import os
import firebase_admin
from firebase_admin import credentials, firestore
from core.config import (
    GEMINI_API_KEY, GEMINI_MODEL, TOGETHER_API_KEY, TOGETHER_MODEL, 
    OLLAMA_MODEL, OLLAMA_URL, MEMORIA_FILE, SKILLS_DIR, FIREBASE_CREDENTIALS
)
from core.utils import Cor

# --- INICIALIZAÇÃO DO FIREBASE (SISTEMA HÍBRIDO) ---
db = None
if FIREBASE_CREDENTIALS and os.path.exists(FIREBASE_CREDENTIALS):
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("  ☁️ [Memória Cloud: ATIVADA]")
    except Exception as e:
        print(f"  ⚠️ [Erro no Firebase, usando JSON local]: {e}")
else:
    print("  📁 [Memória Cloud: DESATIVADA - Usando arquivo local]")

# --- FUNÇÕES DE MEMÓRIA MUTANTES ---
def ler_memoria():
    if db: 
        try:
            doc_ref = db.collection('usuarios').document('caua')
            doc = doc_ref.get()
            if doc.exists:
                fatos = doc.to_dict().get("fatos", [])
                return "\n".join([f"- {m}" for m in fatos])
            return "Nenhum."
        except Exception:
            return "Erro ao ler memória da nuvem."
    else: 
        if not MEMORIA_FILE.exists(): return "Nenhum."
        try:
            dados = json.loads(MEMORIA_FILE.read_text(encoding='utf-8'))
            return "\n".join([f"- {m}" for m in dados.get("fatos", [])])
        except: return "Erro ao ler memória."

def salvar_memoria(nova_info):
    if db: 
        try:
            doc_ref = db.collection('usuarios').document('caua')
            doc = doc_ref.get()
            if doc.exists:
                fatos = doc.to_dict().get("fatos", [])
            else:
                fatos = []
            
            if nova_info not in fatos:
                fatos.append(nova_info)
                doc_ref.set({"fatos": fatos}) 
        except Exception:
            pass 
    else: 
        dados = {"fatos": []}
        if MEMORIA_FILE.exists():
            try: dados = json.loads(MEMORIA_FILE.read_text(encoding='utf-8'))
            except: pass
        if nova_info not in dados["fatos"]:
            dados["fatos"].append(nova_info)
            MEMORIA_FILE.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding='utf-8')

# --- SISTEMA DE SKILLS E PROMPT ---
def listar_skills():
    if not SKILLS_DIR.exists(): return "Nenhuma."
    arquivos = [f.name for f in SKILLS_DIR.glob("*.py") if f.name != "__init__.py"]
    return ", ".join(arquivos) if arquivos else "Nenhuma."

def construir_system_prompt(area_de_trabalho):
    return f"""[SISTEMA: SONAS v7.0]
Você é um Agente Sysadmin Especialista em Automação.

1. MEMÓRIA DE LONGO PRAZO DO USUÁRIO (LEIA COM ATENÇÃO):
{ler_memoria()}

2. REGRA CRÍTICA DE AUTO-MEMORY (ANÁLISE DE TEXTO NLP):
Você é o guardião do contexto. Analise a frase do usuário. Se ele afirmar algo sobre si mesmo (nome, rotina, gosto, projeto), você OBRIGATORIAMENTE deve extrair esse fato e colocar na lista "fatos_aprendidos".
- Exemplo: Se o usuário disser "meu nome é Cauã", adicione "O usuário se chama Cauã" em fatos_aprendidos.
- Se a informação pedida não estiver na memória, seja sincero e diga que não sabe.

3. SISTEMA DE SKILLS:
Skills Atuais: {listar_skills()}
-> Se o usuário pedir uma nova habilidade, gere um código criando um arquivo .py em SKILLS_DIR.

ESTRUTURA JSON OBRIGATÓRIA:
{{
  "acao": "responder" | "executar_codigo",
  "texto_resposta": "Sua resposta natural",
  "codigo_python": "Código (se necessário. PROIBIDO input(). Aspas triplas para strings)",
  "fatos_aprendidos": ["Fato novo extraído do texto"]
}}
AREA_DE_TRABALHO = r"{area_de_trabalho}"
SKILLS_DIR = r"{SKILLS_DIR}" """

# --- ROTEADOR DUAL-CLOUD COM FALLBACK E DEBUG ---
def chamar_ia(mensagens, system_prompt):
    ultima_msg = mensagens[-1]["content"].lower()
    
    motor = "auto"
    if "together" in ultima_msg: motor = "together"
    elif "gemini" in ultima_msg: motor = "gemini"
    elif "ollama" in ultima_msg or "local" in ultima_msg: motor = "ollama"

    if motor == "auto":
        # Escolhe Together AI para interações rápidas e curtas; Gemini para o resto
        if len(ultima_msg) < 60 and TOGETHER_API_KEY:
            motor = "together"
        else:
            motor = "gemini" if GEMINI_API_KEY else "together"
            
    # ROTAS DE EXECUÇÃO
    if motor == "gemini" and GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]} for m in mensagens],
                "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
            }
            resp = requests.post(url, json=payload, timeout=30)
            
            if resp.status_code == 200:
                conteudo = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(conteudo.replace("```json", "").replace("```", "").strip()), "Gemini 2.5 Flash 🧠"
            else:
                print(f"  {Cor.VERMELHO}ERRO GEMINI ({resp.status_code}): {resp.text}{Cor.RESET}")
                motor = "together"
        except Exception as e: 
            print(f"  {Cor.VERMELHO}FALHA GEMINI: {e}{Cor.RESET}")
            motor = "together"

    # ROTA TOGETHER AI (O novo motor de velocidade)
    if motor == "together" and TOGETHER_API_KEY:
        try:
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": TOGETHER_MODEL,
                "messages": [{"role": "system", "content": system_prompt}] + mensagens,
                "temperature": 0.1,
                "response_format": {"type": "json_object"}
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                return json.loads(resp.json()["choices"][0]["message"]["content"]), "Together Turbo ⚡"
            else:
                print(f"  {Cor.VERMELHO}ERRO TOGETHER ({resp.status_code}): {resp.text}{Cor.RESET}")
                motor = "ollama"
        except Exception as e: 
            print(f"  {Cor.VERMELHO}FALHA TOGETHER: {e}{Cor.RESET}")
            motor = "ollama"

    # FALLBACK LOCAL (O motor de sobrevivência)
    try:
        payload = {"model": OLLAMA_MODEL, "messages": [{"role": "system", "content": system_prompt}] + mensagens, "format": "json", "stream": False}
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        return json.loads(str(r.json()["message"]["content"]).replace("```json", "").replace("```", "").strip()), "Ollama Local (Qwen) ⚙️"
    except Exception as e:
        raise RuntimeError(f"Crítico: Todos os motores offline. Erro: {e}")