# Documentação Gabi - Chat Multi-Agentes

Bem-vindo à documentação completa do sistema Gabi - Chat Multi-Agentes baseado no padrão BMAD com tecnologia Agno SDK.

## 📚 Documentação Completa

### 🎯 **Documentação Técnica**
- **[GABI_SYSTEM_DOCUMENTATION.md](GABI_SYSTEM_DOCUMENTATION.md)** - Documentação completa do sistema
- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** - Diagramas de arquitetura
- **[AGNO_SDK_INTEGRATION_GUIDE.md](AGNO_SDK_INTEGRATION_GUIDE.md)** - Guia de integração Agno SDK

### 👤 **Documentação do Usuário**
- **[USER_GUIDE.md](USER_GUIDE.md)** - Guia completo do usuário
- **[README.md](README.md)** - Visão geral do projeto

### 🎨 **Design e Marca**
- **[BRAND_GUIDELINES.md](BRAND_GUIDELINES.md)** - Diretrizes de marca
- **[design-system.md](design-system.md)** - Sistema de design

### 🏗️ **Arquitetura**
- **[architecture/](architecture/)** - Documentação de arquitetura detalhada

## 🚀 Início Rápido

### 1. **Deploy Local**
```bash
docker-compose up -d
```

### 2. **Acessar Sistema**
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:7777
- **Health Check:** http://localhost:7777/health

### 3. **Configuração**
1. Acesse **Gabi.OS** para configurar AgentOS
2. Teste o **Chat** principal
3. Explore **Configurações** avançadas

## 📱 Telas do Sistema

### 1. **Chat Principal** (`/`)
- Interface de conversa em tempo real
- Histórico de mensagens
- Integração com Agno SDK

### 2. **Gabi.OS** (`/gabi-os`)
- Configuração de URL do AgentOS
- Teste de conectividade
- Informações do sistema

### 3. **Histórico** (`/chats`)
- Lista de chats salvos
- Recuperação de conversas
- Gerenciamento de histórico

### 4. **Configurações** (`/configuracoes`)
- Gestão de agentes dinâmicos
- Configurações do sistema
- Administração avançada

## 🔧 Tecnologias

- **Frontend:** Next.js 15 + React + TypeScript
- **Backend:** FastAPI + Python 3.11
- **Banco:** PostgreSQL (Neon)
- **Cache:** Redis
- **SDK:** Agno SDK
- **Container:** Docker + Docker Compose

## 📊 Status do Sistema

- ✅ **Frontend:** Operacional (Porta 3000)
- ✅ **Backend:** Operacional (Porta 7777)
- ✅ **Database:** Conectado (Porta 5432)
- ✅ **Cache:** Ativo (Porta 6379)
- ✅ **Performance:** Otimizada (~47ms)

## 🆘 Suporte

Para problemas técnicos:
1. Consulte a [documentação técnica](GABI_SYSTEM_DOCUMENTATION.md)
2. Verifique o [guia do usuário](USER_GUIDE.md)
3. Analise os logs: `docker-compose logs`
4. Reinicie o sistema: `docker-compose restart`

## 📁 Estrutura da Documentação

```
docs/
├── INDEX.md                           # Este arquivo - índice da documentação
├── GABI_SYSTEM_DOCUMENTATION.md       # Documentação completa do sistema
├── USER_GUIDE.md                      # Guia do usuário
├── ARCHITECTURE_DIAGRAM.md            # Diagramas de arquitetura
├── README.md                          # Documentação principal
├── BRAND_GUIDELINES.md                # Diretrizes de marca
├── design-system.md                   # Sistema de design
├── AGNO_SDK_INTEGRATION_GUIDE.md      # Guia de integração Agno SDK
└── architecture/                      # Documentação de arquitetura
```

---

**Sistema Gabi - Chat Multi-Agentes**  
*Powered by ness.*
