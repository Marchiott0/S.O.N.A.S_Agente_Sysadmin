# 🧠 S.O.N.A.S - v7.0 (Cloud-Agent Architecture)
**Sistema de Orquestração Nativa para Agentes e Scripts**

O S.O.N.A.S é um framework híbrido de agentes de IA focado em **Alta Disponibilidade (Self-Healing)**, **Roteamento Dinâmico de LLMs** e **Persistência de Memória**. Ele não apenas conversa, mas escreve, executa e conserta o próprio código no ambiente do usuário.

## 🚀 Arquitetura e Features
* **LLM Routing:** Avalia a complexidade do prompt e roteia para o motor mais eficiente. Usa **Together AI (Llama 3.3)** para velocidade em comandos curtos e **Gemini 2.5 Flash** para contexto profundo.
* **Auto-Fallback (Modo Offline):** Se as APIs falharem ou a internet cair, o sistema redireciona a carga automaticamente para o motor local **Ollama (Qwen 2.5 Coder)**.
* **Self-Healing Code:** O agente cria scripts `.py` (Skills). Se uma biblioteca externa estiver faltando durante a execução, o interceptador do SONAS faz o `pip install` em background e reexecuta o código sem intervenção humana.
* **Dual-Cloud Memory (PNL):** Extrai fatos do usuário silenciosamente e os salva em um banco de dados NoSQL (**Firebase/Firestore**) com fallback de espelhamento para um arquivo `.json` local.

---

## ⚙️ Instalação Rápida (Windows)

Para instalar todo o ecossistema com apenas 2 cliques:
1. Faça o clone deste repositório.
2. Dê um duplo clique no arquivo **`setup_SONAS.bat`**. 
*(Ele instalará as bibliotecas, baixará o motor Ollama e fará o pull do modelo Qwen automaticamente).*

---

## 🔑 Configuração do Ambiente (.env)

O S.O.N.A.S precisa de chaves de acesso para operar na nuvem. Crie um arquivo chamado `.env` na raiz do projeto e preencha com a seguinte estrutura:

```env
TOGETHER_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
FIREBASE_CREDENTIALS=firebase_credentials.json