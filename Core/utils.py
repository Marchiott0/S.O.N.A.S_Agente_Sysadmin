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
        except Exception: pass

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

def executar_python(codigo, area_de_trabalho):
    namespace_global = {"__builtins__": __builtins__, "AREA_DE_TRABALHO": area_de_trabalho, "os": os, "Path": Path}
    stdout_buf, stderr_buf = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            exec(codigo, namespace_global)
        saida, erros = stdout_buf.getvalue(), stderr_buf.getvalue()
        return f"[STDOUT]\n{saida}\n[STDERR]\n{erros}".strip() if erros else saida.strip() or "✔ Sucesso."
    except Exception:
        return f"[ERRO DE EXECUÇÃO]\n{traceback.format_exc()}"

def imprimir_banner(versao="6.4"):
    print(f"""{Cor.CIANO}{Cor.BOLD}
  ╔════════════════════════════════════════════════════════════╗
  ║        ███████  ██████  ███  ██   █████  ███████           ║
  ║        ██       ██  ██  ████ ██  ██  ██  ██                ║
  ║        ███████  ██  ██  ██ ████  ███████ ███████           ║
  ║             ██  ██  ██  ██  ███  ██  ██       ██           ║
  ║        ███████  ██████  ██   ██  ██  ██  ███████           ║
  ║                                                            ║
  ║  Sistema de Orquestração Nativa para Agentes e Scripts     ║
  ║                        v{versao}                           ║
  ╚════════════════════════════════════════════════════════════╝
  
  {Cor.RESET}""")