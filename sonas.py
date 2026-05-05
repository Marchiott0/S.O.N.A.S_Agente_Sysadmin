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
from core.engine import construir_system_prompt, chamar_ia, _ler_status
from core.config import FALLBACK_DURATION

def main() -> None:
    habilitar_ansi_windows()
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER.replace("v6.4.3", "v6.4.4")) # Garantindo a versão no banner

    area_de_trabalho = descobrir_area_de_trabalho()
    system_prompt    = construir_system_prompt(area_de_trabalho)
    
    print(f"  {Cor.VERDE}{Cor.BOLD}✔ SISTEMA OPERACIONAL:{Cor.RESET} {area_de_trabalho}")
    
    status_cb = _ler_status()
    if "ultimo_erro" in status_cb:
        ultimo = datetime.fromisoformat(status_cb["ultimo_erro"])
        restante = FALLBACK_DURATION - (datetime.now() - ultimo)
        h, m = int(restante.total_seconds() // 3600), int((restante.total_seconds() % 3600) // 60)
        print(f"  {Cor.AMARELO}⚠  STATUS: Offline (Ollama) — Cloud reconecta em: {h}h {m}m{Cor.RESET}")
    else:
        print(f"  {Cor.AZUL}☁  STATUS: Cloud (Groq) — Performance Ativa{Cor.RESET}")

    imprimir_separador("═")
    print(f"  {Cor.CINZA}Comandos: 'sair' | 'limpar'{Cor.RESET}")
    imprimir_separador("═")

    historico = []

    try:
        while True:
            print()
            try:
                entrada = input(f"{Cor.MAGENTA}{Cor.BOLD}você{Cor.RESET}{Cor.CINZA} › {Cor.RESET}").strip()
            except (EOFError, KeyboardInterrupt): break

            if not entrada: continue
            if entrada.lower() == "sair": break
            if entrada.lower() == "limpar":
                historico.clear()
                os.system("cls" if os.name == "nt" else "clear")
                print(BANNER.replace("v6.4.3", "v6.4.4"))
                imprimir_separador("═")
                continue

            historico.append({"role": "user", "content": entrada})
            print(f"  {Cor.CINZA}processando requisição...{Cor.RESET}", end="\r", flush=True)
            
            try:
                dados, backend = chamar_ia(historico, system_prompt)
                print(f"  {' ' * 35}\r", end="")
                
                # BLINDAGEM v6.4.4: Força conversão para string para evitar erro de .strip() em booleano
                texto = str(dados.get("texto_resposta") or "").strip()
                codigo = str(dados.get("codigo_python") or "").strip()
                acao = str(dados.get("acao") or "responder").strip()

                if not texto and not codigo:
                    texto = f"{Cor.VERMELHO}Erro: O motor retornou um objeto vazio.{Cor.RESET}"
                
                imprimir_separador()
                imprimir_badge_backend(backend)
                print(f"\n{Cor.CIANO}{Cor.BOLD}sonas{Cor.RESET} › {texto}")

                if acao == "executar_codigo" and codigo:
                    print(f"\n  {Cor.AMARELO}⚡ EXECUTANDO SCRIPT:{Cor.RESET}")
                    exibir_codigo(codigo)
                    time.sleep(0.5)
                    resultado = executar_python(codigo, area_de_trabalho)
                    print(f"\n  {Cor.VERDE}▶ SAÍDA DO TERMINAL:{Cor.RESET}\n    {resultado}")
                    historico.append({"role": "assistant", "content": f"{texto}\n\n[Output]:\n{resultado}"})
                else:
                    historico.append({"role": "assistant", "content": texto})

                imprimir_separador()
            except Exception as e:
                print(f"  {' ' * 35}\r", end="")
                print(f"{Cor.VERMELHO}![ERRO NO PROCESSAMENTO]: {str(e)}{Cor.RESET}")
                historico.pop()

            if len(historico) > 20: historico = historico[-20:]

    except Exception:
        traceback.print_exc()
        input(f"\n{Cor.CINZA}Pressione ENTER para encerrar...{Cor.RESET}")

if __name__ == "__main__":
    main()