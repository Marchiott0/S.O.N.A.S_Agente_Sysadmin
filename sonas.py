from core.utils import Cor, habilitar_ansi_windows, descobrir_area_de_trabalho, imprimir_banner, executar_python
from core.engine import construir_system_prompt, chamar_ia
import os

def main():
    habilitar_ansi_windows()
    imprimir_banner()
    
    area_trabalho = descobrir_area_de_trabalho()
    sys_prompt = construir_system_prompt(area_trabalho)
    historico = []

    print(f"  {Cor.VERDE}✔ Sistema Pronto em:{Cor.RESET} {area_trabalho}\n")

    while True:
        entrada = input(f"{Cor.MAGENTA}{Cor.BOLD}você{Cor.RESET} › ").strip()
        if entrada.lower() in ['sair', 'exit']: break
        if entrada.lower() == 'limpar':
            historico.clear()
            os.system('cls' if os.name == 'nt' else 'clear')
            imprimir_banner()
            continue

        historico.append({"role": "user", "content": entrada})
        
        try:
            dados, backend = chamar_ia(historico, sys_prompt)
            texto = dados.get("texto_resposta", "Processamento concluído.")
            codigo = dados.get("codigo_python", "")

            print(f"\n{Cor.CINZA}─ (Backend: {backend}) ─{Cor.RESET}")
            print(f"{Cor.CIANO}{Cor.BOLD}sonas{Cor.RESET} › {texto}")

            if dados.get("acao") == "executar_codigo" and codigo:
                print(f"\n{Cor.AMARELO}⚡ Executando código...{Cor.RESET}")
                resultado = executar_python(codigo, area_trabalho)
                print(f"{Cor.VERDE}▶ Output:{Cor.RESET}\n{resultado}")
                historico.append({"role": "assistant", "content": f"{texto}\nOutput: {resultado}"})
            else:
                historico.append({"role": "assistant", "content": texto})

        except Exception as e:
            print(f"{Cor.VERMELHO}Erro: {e}{Cor.RESET}")

if __name__ == "__main__":
    main()