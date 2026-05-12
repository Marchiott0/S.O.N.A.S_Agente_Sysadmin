import os
import sys
import time
import traceback
from datetime import datetime

from core.utils import (
    Cor, habilitar_ansi_windows, descobrir_area_de_trabalho,
    BANNER, executar_python, imprimir_separador, 
    imprimir_badge_backend, exibir_codigo
)
from core.engine import construir_system_prompt, chamar_ia, salvar_memoria
from core.config import SKILLS_DIR

def main() -> None:
    habilitar_ansi_windows()
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)

    area_de_trabalho = descobrir_area_de_trabalho()
    
    print(f"  {Cor.VERDE}{Cor.BOLD}✔ SISTEMA OPERACIONAL:{Cor.RESET} {area_de_trabalho}")
    print(f"  {Cor.AZUL}☁  ARQUITETURA:{Cor.RESET} Dual-Cloud AI (Gemini 🧠 + Together Turbo ⚡)")
    print(f"  {Cor.AMARELO}⚙️  MÓDULOS:{Cor.RESET} Skills, Auto-Instalador & NLP Auto-Memory")
    
    imprimir_separador("═")
    historico = []

    try:
        while True:
            system_prompt = construir_system_prompt(area_de_trabalho)
            print()
            try:
                entrada = input(f"{Cor.MAGENTA}{Cor.BOLD}você{Cor.RESET}{Cor.CINZA} › {Cor.RESET}").strip()
            except (EOFError, KeyboardInterrupt): break

            if not entrada: continue
            if entrada.lower() in ["sair", "exit"]: break
            if entrada.lower() == "limpar":
                historico.clear()
                os.system("cls" if os.name == "nt" else "clear")
                print(BANNER)
                imprimir_separador("═")
                continue

            historico.append({"role": "user", "content": entrada})
            print(f"  {Cor.CINZA}processando via PNL...{Cor.RESET}", end="\r", flush=True)
            
            try:
                dados, backend_usado = chamar_ia(historico, system_prompt)
                print(f"  {' ' * 35}\r", end="")
                
                texto = str(dados.get("texto_resposta") or "").strip()
                codigo = str(dados.get("codigo_python") or "").strip()
                acao = str(dados.get("acao") or "responder").strip()
                fatos = dados.get("fatos_aprendidos", [])

                if isinstance(fatos, list) and fatos:
                    for fato in fatos:
                        salvar_memoria(fato)
                        print(f"  {Cor.CINZA}🧠 [SONAS Memorizou: {fato}]{Cor.RESET}")

                if not texto and not codigo:
                    texto = f"{Cor.VERMELHO}Erro: O motor não conseguiu formatar o JSON.{Cor.RESET}"
                
                imprimir_separador()
                imprimir_badge_backend(backend_usado)
                print(f"\n{Cor.CIANO}{Cor.BOLD}sonas{Cor.RESET} › {texto}")

                if acao == "executar_codigo" and codigo:
                    print(f"\n  {Cor.AMARELO}⚡ EXECUTANDO SCRIPT:{Cor.RESET}")
                    exibir_codigo(codigo)
                    time.sleep(0.4)
                    resultado = executar_python(codigo, area_de_trabalho, SKILLS_DIR)
                    print(f"\n  {Cor.VERDE}▶ SAÍDA DO TERMINAL:{Cor.RESET}\n    {resultado}")
                    historico.append({"role": "assistant", "content": f"{texto}\n\n[Output]:\n{resultado}"})
                else:
                    historico.append({"role": "assistant", "content": texto})

                imprimir_separador()
            except Exception as e:
                print(f"  {' ' * 35}\r", end="")
                print(f"{Cor.VERMELHO}![ERRO DE EXECUÇÃO]: {str(e)}{Cor.RESET}")
                historico.pop()

            if len(historico) > 30: historico = historico[-30:]

    except Exception:
        import traceback
        traceback.print_exc()
        input(f"\n{Cor.CINZA}Pressione ENTER para encerrar...{Cor.RESET}")

if __name__ == "__main__":
    main()