# Gabi - Sistema de Chat Multi-Agentes
## Documentação Completa do Sistema

**Versão:** 1.0.0  
**Data:** 24/01/2024  
**Status:** Operacional  

---

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Arquitetura Técnica](#arquitetura-técnica)
3. [Fluxo Funcional](#fluxo-funcional)
4. [Telas e Navegação](#telas-e-navegação)
5. [Configuração e Deploy](#configuração-e-deploy)
6. [API Endpoints](#api-endpoints)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral do Sistema

### Propósito
O **Gabi** é um sistema de chat multi-agentes baseado no padrão BMAD (Business Model Agent Design) que permite:

- **Chat em tempo real** com agentes de IA
- **Configuração de AgentOS** para integração externa
- **Histórico de conversas** com recuperação de chats
- **Gestão de agentes** dinâmicos via API

### Tecnologias Principais
- **Frontend:** Next.js 15 + React + TypeScript
- **Backend:** FastAPI + Python 3.11
- **Banco de Dados:** PostgreSQL (Neon)
- **Cache:** Redis
- **Containerização:** Docker + Docker Compose
- **SDK:** Agno SDK para agentes

---

## 🏗️ Arquitetura Técnica

### Estrutura do Projeto
```
Gabi/
├── src/                    # Frontend Next.js
│   ├── app/               # Páginas da aplicação
│   ├── components/        # Componentes React
│   └── hooks/            # Custom hooks
├── backend/              # Backend FastAPI
│   ├── app/
│   │   ├── api/         # Endpoints da API
│   │   ├── services/    # Lógica de negócio
│   │   └── schemas/     # Modelos Pydantic
├── docs/                # Documentação
├── docker-compose.yml   # Orquestração de containers
└── bmad/               # Padrão BMAD
```

### Containers Docker
- **gabi-chat:** Frontend Next.js (Porta 3000)
- **gabi-os:** Backend FastAPI (Porta 7777)
- **gabi-postgres:** Banco PostgreSQL (Porta 5432)
- **gabi-redis:** Cache Redis (Porta 6379)

---

## 🔄 Fluxo Funcional

### 1. Inicialização do Sistema
```mermaid
graph TD
    A[Usuário acessa localhost:3000] --> B[Frontend carrega]
    B --> C[Sidebar com navegação]
    C --> D[Página inicial do Chat]
    D --> E[Sistema pronto para uso]
```

### 2. Fluxo de Chat
```mermaid
graph TD
    A[Usuário digita mensagem] --> B[Frontend valida entrada]
    B --> C[Envia para backend /chat/send-message]
    C --> D[Backend processa com Agno SDK]
    D --> E[Retorna resposta]
    E --> F[Frontend exibe mensagem]
    F --> G[Salva no histórico]
```

### 3. Configuração do AgentOS
```mermaid
graph TD
    A[Usuário acessa Gabi.OS] --> B[Insere URL do AgentOS]
    B --> C[Testa conexão]
    C --> D{Conectado?}
    D -->|Sim| E[Salva configuração]
    D -->|Não| F[Exibe erro]
    E --> G[Carrega agentes disponíveis]
```

---

## 📱 Telas e Navegação

### 1. **Chat Principal** (`/`)
- **Função:** Interface principal de conversa
- **Componentes:**
  - Sidebar com navegação
  - Área de mensagens
  - Campo de entrada
  - Botão de envio
- **Funcionalidades:**
  - Envio de mensagens em tempo real
  - Histórico de conversa
  - Limpeza do chat
  - Indicador de status

### 2. **Gabi.OS** (`/gabi-os`)
- **Função:** Configuração de conexão com AgentOS
- **Componentes:**
  - Campo de URL do AgentOS
  - Botão de teste de conexão
  - Status de conexão
  - Informações do AgentOS
- **Funcionalidades:**
  - Teste de conectividade
  - Salvamento de configuração
  - Exibição de dados do AgentOS

### 3. **Histórico de Chats** (`/chats`)
- **Função:** Gerenciamento de conversas salvas
- **Componentes:**
  - Lista de chats salvos
  - Informações de cada chat
  - Botões de ação
- **Funcionalidades:**
  - Visualização de chats anteriores
  - Recuperação de conversas
  - Exclusão de chats

### 4. **Configurações** (`/configuracoes`)
- **Função:** Configurações avançadas do sistema
- **Componentes:**
  - Tabs de configuração
  - Formulários de configuração
  - Botões de ação
- **Funcionalidades:**
  - Gestão de agentes dinâmicos
  - Configurações do sistema
  - Administração

---

## ⚙️ Configuração e Deploy

### Pré-requisitos
- Docker Desktop
- WSL2 (Windows) ou Linux
- 4GB RAM mínimo
- 10GB espaço em disco

### Deploy Local
```bash
# 1. Clone o repositório
git clone <repository-url>
cd Gabi

# 2. Inicie os containers
docker-compose up -d

# 3. Verifique o status
docker-compose ps

# 4. Acesse a aplicação
# Frontend: http://localhost:3000
# Backend: http://localhost:7777
```

### Variáveis de Ambiente
```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/gabi
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your-api-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:7777
```

---

## 🔌 API Endpoints

### Chat
- `POST /chat/send-message` - Enviar mensagem
- `POST /chat/start-session` - Iniciar sessão
- `GET /chat/session-status/{id}` - Status da sessão
- `POST /chat/clear-session/{id}` - Limpar sessão

### Agentes
- `GET /agents` - Listar agentes
- `POST /agents` - Criar agente
- `PUT /agents/{id}` - Atualizar agente
- `DELETE /agents/{id}` - Deletar agente

### Agno SDK
- `GET /agno/status` - Status do Agno SDK
- `POST /dynamic/agents` - Criar agente dinâmico

### Health Check
- `GET /health` - Status do sistema

---

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. **Containers não iniciam**
```bash
# Verificar logs
docker-compose logs

# Reiniciar containers
docker-compose down
docker-compose up -d
```

#### 2. **Frontend não carrega**
```bash
# Verificar se a porta 3000 está livre
netstat -tulpn | grep 3000

# Rebuild do frontend
docker-compose up --build -d gabi-chat
```

#### 3. **Backend não responde**
```bash
# Verificar health check
curl http://localhost:7777/health

# Verificar logs do backend
docker-compose logs gabi-os
```

#### 4. **Banco de dados não conecta**
```bash
# Verificar status do PostgreSQL
docker-compose ps gabi-postgres

# Verificar logs
docker-compose logs gabi-postgres
```

### Performance
- **Carregamento:** ~47ms (otimizado)
- **Resposta do chat:** ~18ms
- **Timeout:** 5 segundos máximo
- **Recursos:** 2GB RAM recomendado

---

## 📊 Monitoramento

### Health Checks
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:7777/health
- **Database:** Porta 5432
- **Redis:** Porta 6379

### Logs
```bash
# Ver todos os logs
docker-compose logs

# Logs específicos
docker-compose logs gabi-chat
docker-compose logs gabi-os
```

---

## 🔄 Próximos Passos

### Fase 4 - Configuração de Agentes
- Interface para configurar agentes via API do AgentOS
- Gestão de templates de agentes
- Configuração de workflows
- Monitoramento de agentes

### Melhorias Planejadas
- Autenticação de usuários
- Persistência de configurações
- Integração com mais AgentOS
- Analytics e métricas

---

## 📞 Suporte

Para problemas técnicos:
1. Verificar logs do sistema
2. Consultar esta documentação
3. Verificar status dos containers
4. Reiniciar sistema se necessário

**Sistema Gabi - Chat Multi-Agentes**  
*Powered by ness.*
