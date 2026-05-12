# 🗝️ Guia de Como obter as Chaves de API para o S.O.N.A.S

O S.O.N.A.S precisa se comunicar com serviços na nuvem para pensar rápido, raciocinar e guardar memórias. Para isso, ele usa "Chaves de API" (API Keys), que são como senhas de acesso exclusivas para o seu agente.

Siga o passo a passo abaixo para conseguir as suas. É tudo 100% gratuito para começar.

---

## 1. Together AI (O Motor de Velocidade ⚡)
Usamos o Together AI (com o modelo Llama 3.3) para responder a comandos rápidos e rotear as tarefas.

**Passo a passo:**
1. Acesse o site: [https://www.together.ai/](https://www.together.ai/)
2. Clique no botão **"Sign Up"** (ou "Start Building") e faça login com a sua conta do Google.
3. No painel principal (Dashboard), olhe no canto superior direito e clique nas suas iniciais para abrir o menu.
4. Clique em **"Settings"** e depois vá na aba **"API Keys"**.
5. Clique em "Create Key" de o Nome que achar melhor (SONAS_key por exemplo). Clique no botão de copiar.
6. Cole essa chave no seu arquivo `.env` na linha `TOGETHER_API_KEY=`.

*Aviso: O Together AI dá créditos gratuitos, mas eventualmente pode pedir que você cadastre um cartão de crédito apenas para verificar que você não é um robô (mesmo sem cobrar nada, CUIDADO PARA NÃO COMPRAR NADA POR ENGANO).*

---

## 2. Google Gemini (O Motor de Raciocínio 🧠)
Usamos o Gemini 2.5 Flash para tarefas que exigem muita leitura, interpretação de textos longos ou raciocínio complexo.

**Passo a passo:**
1. Acesse o Google AI Studio: [https://aistudio.google.com/](https://aistudio.google.com/)
2. Faça login com a sua conta do Google.
3. No menu lateral esquerdo, clique no ícone de chave ou no botão **"Get API key"**.
4. Clique no botão azul **"Create API key"**.
5. Selecione um projeto do Google Cloud existente ou escolha criar um novo projeto.
6. Copie a chave gerada.
7. Cole essa chave no seu arquivo `.env` na linha `GEMINI_API_KEY=`.

---

## 3. Firebase (O Banco de Memória ☁️)
Usamos o Firebase Firestore para guardar as informações que o S.O.N.A.S aprende sobre você ao longo do tempo (sua rotina, setup, etc).

**Passo a passo:**
1. Acesse o Console do Firebase: [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Faça login com o Google e clique em **"Criar um projeto"** (ou "Adicionar projeto").
3. Dê o nome de `sonas-db` (ou o nome que preferir), desative o Google Analytics (não precisamos disso) e clique em "Criar projeto".
4. Dentro do projeto, no menu esquerdo, vá em **"Criação"** > **"Firestore Database"**.
5. Clique em **"Criar banco de dados"**. Escolha a sua região (ex:`southamerica-east1` em São Paulo) e inicie no **Modo de Teste**.

**Como baixar a chave do Firebase:**
1. Ainda no Firebase, olhe no menu esquerdo, no topo, e clique na **Engrenagem** ao lado de "Visão geral do projeto".
2. Clique em **"Configurações do projeto"**.
3. Vá na aba superior chamada **"Contas de serviço"**.
4. Certifique-se de que "Node.js" ou "Python" esteja selecionado e clique no botão azul **"Gerar nova chave privada"**.
5. Um arquivo `.json` será baixado no seu computador.
6. Mova esse arquivo para a pasta raiz do seu projeto S.O.N.A.S.
7. **Muito Importante:** Renomeie esse arquivo para `firebase_credentials.json`.

---

## 🏁 Finalizando

Depois de seguir estes passos, o seu arquivo `.env` deve estar exatamente assim:

```env
TOGETHER_API_KEY=sua_chave_do_together_aqui
GEMINI_API_KEY=sua_chave_do_gemini_aqui
FIREBASE_CREDENTIALS=firebase_credentials.json