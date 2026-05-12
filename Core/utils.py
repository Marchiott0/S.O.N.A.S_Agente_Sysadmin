import os
import sys
import io
import contextlib
import traceback
import subprocess
from pathlib import Path

class Cor:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    CINZA    = "\033[90m"
    VERDE    = "\033[92m"
    AMARELO  = "\033[93m"
    AZUL     = "\033[94m"
    MAGENTA  = "\033[95m"
    CIANO    = "\033[96m"
    BRANCO   = "\033[97m"
    VERMELHO = "\033[91m"

def habilitar_ansi_windows():
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception: pass

# --- BANNER ATUALIZADO PARA A v7.0 CLOUD ---
BANNER = f"""{Cor.CIANO}{Cor.BOLD}
  ╔════════════════════════════════════════════════════════════╗
  ║        ███████  ██████  ███  ██   █████  ███████           ║
  ║        ██       ██  ██  ████ ██  ██  ██  ██                ║
  ║        ███████  ██  ██  ██ ████  ███████ ███████           ║
  ║             ██  ██  ██  ██  ███  ██  ██       ██           ║
  ║        ███████  ██████  ██   ██  ██  ██  ███████           ║
  ║                                                            ║
  ║  Sistema de Orquestração Nativa para Agentes e Scripts     ║
  ║               v7.0 - Cloud-Agent Architecture              ║
  ╚════════════════════════════════════════════════════════════╝{Cor.RESET}"""

def descobrir_area_de_trabalho():
    perfil = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    candidatos = [
        os.path.join(perfil, "OneDrive", "Área de Trabalho"),
        os.path.join(perfil, "OneDrive", "Desktop"),
        os.path.join(perfil, "Área de Trabalho"),
        os.path.join(perfil, "Desktop"),
    ]
    for caminho in candidatos:
        if os.path.isdir(caminho): return caminho
    return str(Path(__file__).parent.parent / "output_sonas")

# --- SISTEMA DE EXECUÇÃO COM AUTO-INSTALADOR (SELF-HEALING) ---
def executar_python(codigo, area_de_trabalho, skills_dir):
    if str(skills_dir) not in sys.path:
        sys.path.append(str(skills_dir))
        
    codigo_limpo = codigo.replace('\r', '').strip()
    namespace_global = {
        "__builtins__": __builtins__, 
        "AREA_DE_TRABALHO": area_de_trabalho, 
        "SKILLS_DIR": str(skills_dir),
        "os": os, "Path": Path, "sys": sys,
        "random": __import__('random'), "datetime": __import__('datetime')
    }
    
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        stdout_buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec(codigo_limpo, namespace_global)
            saida = stdout_buf.getvalue()
            return saida.strip() if saida else "✔ Execução finalizada com sucesso."
        
        except ModuleNotFoundError as e:
            nome_pacote = e.name
            print(f"\n  {Cor.AMARELO}📦 Dependência Ausente: Baixando biblioteca '{nome_pacote}' automaticamente...{Cor.RESET}")
            # Aciona o PIP silenciosamente no background
            resultado = subprocess.run(
                [sys.executable, "-m", "pip", "install", nome_pacote], 
                capture_output=True, text=True
            )
            if resultado.returncode == 0:
                print(f"  {Cor.VERDE}✔ '{nome_pacote}' instalado! Reiniciando a execução...{Cor.RESET}\n")
                continue # Volta para o começo do loop e executa o código do agente de novo
            else:
                return f"[ERRO FATAL DE PIP]\nO sistema tentou instalar '{nome_pacote}', mas o pacote não existe com este nome exato no repositório."
        
        except Exception:
            return f"[ERRO NO SCRIPT]\n{traceback.format_exc()}"
            
    return "[ERRO] Limite de tentativas de auto-instalação excedido."

# --- FUNÇÕES DE INTERFACE DO TERMINAL ---
def imprimir_separador(char="─", largura=64, cor=Cor.CINZA):
    print(f"{cor}{char * largura}{Cor.RESET}")

def imprimir_badge_backend(backend):
    icone = "🧠" if "Gemini" in backend else "⚡" if "Groq" in backend else "⚙️"
    cor = Cor.AZUL if "Gemini" in backend or "Groq" in backend else Cor.AMARELO
    print(f"  {cor}{icone} Processado via: {backend}{Cor.RESET}")

def exibir_codigo(codigo):
    linhas = codigo.strip().splitlines()
    print(f"{Cor.CINZA}  ┌{'─' * 52}┐{Cor.RESET}")
    for i, linha in enumerate(linhas, 1):
        print(f"{Cor.CINZA}  │{Cor.RESET} {Cor.CIANO}{i:>3}{Cor.RESET}  {linha}")
    print(f"{Cor.CINZA}  └{'─' * 52}┘{Cor.RESET}")