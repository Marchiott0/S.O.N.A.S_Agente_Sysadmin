# S.O.N.A.S
**Sistema de Orquestração Nativa para Agentes e Scripts**

## Sobre o Projeto
O **S.O.N.A.S** é um Agente Sysadmin Autônomo construído em Python. Ele atua como um assistente inteligente capaz de interagir nativamente com o sistema operacional, executar scripts dinâmicos, gerenciar arquivos e integrar-se com APIs externas. 

O grande diferencial deste projeto é a sua **Arquitetura Híbrida e Resiliente**. Ele não depende exclusivamente da nuvem, possuindo um mecanismo de *Circuit Breaker* (Disjuntor) que alterna automaticamente o processamento entre um modelo LLM na nuvem e um modelo local, garantindo que o assistente continue operando mesmo sem internet.

## Principais Funcionalidades
* **Execução Nativa de Código:** O agente é capaz de gerar e executar código Python de forma isolada no ambiente local, capturando `stdout` e `stderr` em tempo real para tomar decisões.
* **Arquitetura Híbrida (Nuvem/Local):** Integração com a API da **Groq** (para altíssima velocidade e capacidade de raciocínio lógico) com um fallback automático para o **Ollama** (rodando modelos Llama localmente).
* **Circuit Breaker:** Sistema de tolerância a falhas que detecta quedas na API da nuvem e redireciona o tráfego para o motor local por um período de segurança (24 horas).
* **Comunicação Estruturada:** O motor de inferência é travado para responder exclusivamente em formato JSON, garantindo que o fluxo de automação não quebre com alucinações de formatação.

## Tecnologias Utilizadas
* **Linguagem:** Python 3
* **LLMs:** Llama 3.3 70B (via Groq Cloud) e Llama 3.1 8B (via Ollama Local)
* **Bibliotecas:** `groq`, `requests`, manipulação nativa de SO (`os`, `sys`, `pathlib`).

## Como executar localmente
1. Clone este repositório: `git clone https://github.com/SEU_USUARIO/SONAS-Agente-Sysadmin.git`
2. Instale as dependências: `pip install groq requests`
3. No arquivo `sonas.py`, adicione a sua própria chave da Groq na variável `CHAVE_GROQ_DIRETA`.
4. (Opcional) Para o modo offline, certifique-se de ter o Ollama instalado e rodando em sua máquina.
5. Execute o sistema: `python sonas.py`

---
*Projeto desenvolvido como estudo prático de integração de IAs autônomas, orquestração de scripts locais e criação de arquiteturas de software tolerantes a falhas. Ainda está em desenvolvimento e melhorando a cada atualização!*