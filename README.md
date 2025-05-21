
# 🗓️ Nucleus Inc. Calendar Discord Bot

Este repositório contém o **bot de integração entre Discord e Zoho Calendar** da Nucleus Inc.  

O projeto foi originalmente desenvolvido em JavaScript, mas foi **reescrito em Python** para maior confiabilidade, organização e facilidade de manutenção.

---

## ✨ Principais Melhorias

### 🔹 Modal Interativo para Criação de Eventos

Antes, os usuários precisavam digitar comandos no formato exato:

```
!createEvent | Reunião do Projeto | Discussão semanal sobre progresso | 23/01/2025 15:00 | 1330929105985732651 | email1@gmail.com,email2@gmail.com
```

Agora, ao usar o comando de evento, um **modal descritivo** é exibido, guiando o usuário pelo processo de criação do evento. Isso reduz erros de formatação e torna a experiência muito mais amigável.

---

### 🔹 Sistema de Logs 📋

Toda a atividade relevante do bot é registrada em arquivos de log, incluindo:

- Inicialização do bot
- Comandos recebidos
- Fluxo de autenticação com o Zoho
- Sucesso ou falha na criação de eventos

Isso facilita o monitoramento e a depuração.

---

### 🔹 Gerenciamento Seguro de Tokens

Implementação de um **Token Manager** para lidar com a autenticação OAuth2 do Zoho:

- 🔁 Atualização automática do access token ao expirar
- 💾 Armazenamento seguro dos tokens em memória
- ♻️ Fluxo desacoplado e reutilizável

---

### 🔹 Cliente Zoho API Modular

Foi criado um cliente dedicado para comunicação com a API do Zoho Calendar, facilitando manutenção e expansão futura.

---

## 🚀 Como Funciona

- O bot utiliza **slash commands** e **modals do Discord** para criar eventos.
- Os dados do evento são enviados para o Zoho Calendar via API, com autenticação automática.
- Logs detalhados são gerados no arquivo `logs/discord.log`.

---

## ⚙️ Configuração

### 1️⃣ Criar Ambiente Virtual

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

- No Linux/MacOS:

```bash
source .venv/bin/activate
```

- No Windows:

```bash
.venv\Scripts\activate
```

---

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DISCORD_TOKEN="..."
ZOHO_CLIENT_ID="..."
ZOHO_CLIENT_SECRET="..."
ZOHO_REFRESH_TOKEN="..."
ZOHO_REDIRECT_URI="..."
ZOHO_CALENDAR_UID="..."
```

---

### 4️⃣ Executar o Projeto

```bash
python3 app.py
```

---

## 🛠️ Tecnologias Utilizadas

- Python
- Discord API (discord.py)
- Zoho Calendar API
- dotenv
- logging

---
