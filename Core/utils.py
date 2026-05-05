import os
import sys
import io
import contextlib
import traceback
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
        except Exception:
            pass

BANNER = f"""{Cor.CIANO}{Cor.BOLD}
  ╔════════════════════════════════════════════════════════════╗
  ║        ███████  ██████  ███  ██   █████  ███████           ║
  ║        ██       ██  ██  ████ ██  ██  ██  ██                ║
  ║        ███████  ██  ██  ██ ████  ███████ ███████           ║
  ║             ██  ██  ██  ██  ███  ██  ██       ██           ║
  ║        ███████  ██████  ██   ██  ██  ██  ███████           ║
  ║                                                            ║
  ║  Sistema de Orquestração Nativa para Agentes e Scripts     ║
  ║                        v6.4.1                              ║
  ╚════════════════════════════════════════════════════════════╝
{Cor.RESET}"""

def descobrir_area_de_trabalho():
    perfil = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    candidatos = [
        os.path.join(perfil, "OneDrive", "Área de Trabalho"),
        os.path.join(perfil, "OneDrive", "Desktop"),
        os.path.join(perfil, "Área de Trabalho"),
        os.path.join(perfil, "Desktop"),
    ]
    for caminho in candidatos:
        if os.path.isdir(caminho):
            return caminho
    fallback = str(Path(__file__).parent.parent / "output_sonas")
    os.makedirs(fallback, exist_ok=True)
    return fallback

def executar_python(codigo, area_de_trabalho):
    namespace_global = {
        "__builtins__": __builtins__,
        "AREA_DE_TRABALHO": area_de_trabalho,
        "os": os,
        "Path": Path,
    }
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            exec(codigo, namespace_global)
        saida = stdout_buf.getvalue()
        erros = stderr_buf.getvalue()
        if erros:
            return f"[STDOUT]\n{saida}\n[STDERR]\n{erros}".strip()
        return saida.strip() if saida.strip() else "✔ Código executado com sucesso (sem output)."
    except Exception:
        return f"[ERRO DE EXECUÇÃO]\n{traceback.format_exc()}"

def imprimir_separador(char="─", largura=60, cor=Cor.CINZA):
    print(f"{cor}{char * largura}{Cor.RESET}")

def imprimir_badge_backend(backend):
    if backend == "Groq":
        icone, cor = "☁", Cor.AZUL
    else:
        icone, cor = "⚙", Cor.AMARELO
    print(f"  {cor}{icone} Backend: {backend}{Cor.RESET}")

def exibir_codigo(codigo):
    linhas = codigo.strip().splitlines()
    print(f"{Cor.CINZA}  ┌{'─' * 52}┐{Cor.RESET}")
    for i, linha in enumerate(linhas, 1):
        print(f"{Cor.CINZA}  │{Cor.RESET} {Cor.CIANO}{i:>3}{Cor.RESET}  {linha}")
    print(f"{Cor.CINZA}  └{'─' * 52}┘{Cor.RESET}")