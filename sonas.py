import os
import sys
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
    
    print(BANNER)

    area_de_trabalho = descobrir_area_de_trabalho()
    
    system_prompt    = construir_system_prompt(area_de_trabalho)

    print(f"  {Cor.VERDE}✔ Área de Trabalho:{Cor.RESET} {area_de_trabalho}")

    status_cb = _ler_status()
    
    if "ultimo_erro" in status_cb:
        
        ultimo  = datetime.fromisoformat(status_cb["ultimo_erro"])
        
        restante = FALLBACK_DURATION - (datetime.now() - ultimo)
        
        h = int(restante.total_seconds() // 3600)
        
        m = int((restante.total_seconds() % 3600) // 60)
        
        print(f"  {Cor.AMARELO}⚠  Modo Offline ativo — retorno à nuvem em: {h}h {m}m{Cor.RESET}")
        
    else:
        
        print(f"  {Cor.AZUL}☁  Modo Cloud (Groq) ativo{Cor.RESET}")

    imprimir_separador("═", 60, Cor.CIANO)
    
    print(f"  {Cor.CINZA}Digite 'sair' para encerrar | 'limpar' para novo contexto{Cor.RESET}")
    
    imprimir_separador("═", 60, Cor.CIANO)

    historico = []

    try:
        
        while True:
            
            print()
            
            try:
                
                entrada = input(f"{Cor.MAGENTA}{Cor.BOLD}você{Cor.RESET}{Cor.CINZA} › {Cor.RESET}").strip()
                
            except (EOFError, KeyboardInterrupt):
                
                print(f"\n\n{Cor.CIANO}SONAS encerrado. Até logo!{Cor.RESET}\n")
                
                break

            if not entrada:
                
                continue

            if entrada.lower() == "sair":
                
                print(f"\n{Cor.CIANO}SONAS encerrado. Até logo!{Cor.RESET}\n")
                
                break

            if entrada.lower() == "limpar":
                
                historico.clear()
                
                os.system("cls" if sys.platform == "win32" else "clear")
                
                print(BANNER)
                
                print(f"  {Cor.VERDE}✔ Contexto limpo. Nova sessão iniciada.{Cor.RESET}\n")
                
                imprimir_separador("═", 60, Cor.CIANO)
                
                continue

            historico.append({"role": "user", "content": entrada})
            
            # A animação clássica de processamento
            print(f"  {Cor.CINZA}processando...{Cor.RESET}", end="\r", flush=True)

            try:
                
                resposta_dict, backend_usado = chamar_ia(historico, system_prompt)
                
            except RuntimeError as e:
                
                print(f"  {' ' * 20}\r", end="")
                
                print(f"\n{Cor.VERMELHO}[ERRO] {e}{Cor.RESET}\n")
                
                historico.pop() 
                
                continue

            acao           = resposta_dict.get("acao", "responder")
            
            texto_resposta = resposta_dict.get("texto_resposta", "").strip()
            
            codigo_python  = resposta_dict.get("codigo_python", "").strip()

            if not texto_resposta:
                
                if codigo_python:
                    
                    texto_resposta = "Executando o código solicitado..."
                    
                else:
                    
                    texto_resposta = "Processamento concluído, mas o modelo não gerou texto."

            # Apaga o "processando..." e imprime a resposta
            print(f"  {' ' * 20}\r", end="")  
            
            imprimir_separador()
            
            imprimir_badge_backend(backend_usado)
            
            print()
            
            print(f"{Cor.CIANO}{Cor.BOLD}sonas{Cor.RESET}{Cor.CINZA} › {Cor.RESET}{texto_resposta}")

            output_execucao = ""

            if acao == "executar_codigo" and codigo_python:
                
                print()
                
                print(f"  {Cor.AMARELO}⚡ Executando código Python:{Cor.RESET}")
                
                exibir_codigo(codigo_python)
                
                print()

                output_execucao = executar_python(codigo_python, area_de_trabalho)

                if output_execucao:
                    
                    print(f"  {Cor.VERDE}▶ Output:{Cor.RESET}")
                    
                    for linha in output_execucao.splitlines():
                        
                        print(f"    {linha}")

            imprimir_separador()

            conteudo_assistente = texto_resposta
            
            if output_execucao:
                
                conteudo_assistente += f"\n\n[Resultado da execução]\n{output_execucao}"

            historico.append({"role": "assistant", "content": conteudo_assistente})

            if len(historico) > 20:
                
                historico = historico[-20:]

    except Exception:
        
        print(f"\n{Cor.VERMELHO}{'═' * 60}")
        
        print("  ERRO FATAL — SONAS encontrou um problema crítico:")
        
        print(f"{'═' * 60}{Cor.RESET}")
        
        print(traceback.format_exc())
        
        print(f"{Cor.VERMELHO}{'═' * 60}{Cor.RESET}\n")
        
        input("Pressione ENTER para fechar...")
        
        sys.exit(1)


if __name__ == "__main__":
    
    main()