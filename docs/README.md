# Gabi - Chat Multi-Agentes

Um chat inteligente baseado no padrão BMAD com tecnologia Agno SDK, implementado seguindo o documento oficial do Agno. Permite criação dinâmica de agentes e múltiplas fontes de conhecimento.

## 🚀 Características

- **Chat Multi-Agentes**: Criação dinâmica de até 3 agentes + 1 orquestrador por sessão
- **Múltiplas Fontes de Conhecimento**: RAG, sites, documentos, MCP servers
- **Tecnologia Agno SDK**: Integração completa com Agno seguindo documento oficial
- **Interface Moderna**: Design dark-first com design system ness
- **Deployment Docker**: Configuração completa com Portainer e Traefik
- **Banco Neon**: Uso de banco Neon para todos os ambientes conforme especificado

## 🏗️ Arquitetura

### Gabi Chat (Next.js)
- Interface de chat moderna
- Design system ness com cores frias
- Componentes reutilizáveis
- Estado gerenciado com Zustand
- Brand guidelines implementadas

### Gabi OS (Python + FastAPI)
- API REST completa compatível com Agno UI
- Integração com Agno SDK seguindo documento oficial
- Gerenciamento de agentes dinâmicos
- Sistema de workflows/teams
- Múltiplas fontes de conhecimento
- Banco de dados Neon (produção)

### BMAD (Business Model Agent Design)
- Padrão BMAD implementado
- Estruturação dinâmica de agentes
- Máximo 3 agentes + 1 orquestrador por sessão
- Templates de workflow pré-definidos

### Infraestrutura
- Docker Compose para orquestração
- Redis para cache e sessões
- Banco Neon para persistência (todos os ambientes)
- Portainer para gerenciamento

## 📁 Estrutura do Projeto

```
Gabi/
├── backend/                      # Backend Python com Agno SDK
├── bmad/                        # Padrão BMAD implementado
├── src/                         # Frontend Next.js
├── config/                      # Arquivos de configuração
│   ├── components.json          # Configuração do shadcn/ui
│   ├── eslint.config.mjs        # Configuração do ESLint
│   ├── next.config.ts           # Configuração do Next.js
│   ├── postcss.config.mjs       # Configuração do PostCSS
│   ├── prettier.config.cjs      # Configuração do Prettier
│   ├── tailwind.config.ts       # Configuração do Tailwind
│   ├── tsconfig.json            # Configuração do TypeScript
│   └── env.example              # Exemplo de variáveis de ambiente
├── docs/                        # Documentação
│   ├── README.md                # Documentação principal
│   ├── BRAND_GUIDELINES.md      # Diretrizes de marca
│   └── AGNO_SDK_INTEGRATION_GUIDE.md # Guia de integração Agno SDK
├── assets/                      # Assets públicos
│   ├── favicon.ico              # Favicon
│   ├── gabi.png                 # Logo Gabi
│   └── gabia.png                # Logo Gabi alternativo
├── docker-compose.yml           # Orquestração Docker
├── Dockerfile                   # Container do frontend
├── package.json                 # Dependências do frontend
└── pnpm-lock.yaml              # Lock file do pnpm
```

## 🛠️ Instalação

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento)
- Python 3.11+ (para desenvolvimento)

### Deployment
```bash
# 1. Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações

# 2. Construir e iniciar serviços
docker-compose up -d

# 3. Executar migrações
docker-compose exec backend alembic upgrade head
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Neon Database (produção)
DATABASE_URL=postgresql://neon_connection_string_here

# Agno SDK
AGNO_API_KEY=your_agno_api_key
OPENAI_API_KEY=your_openai_api_key

# Security
SECRET_KEY=your_secret_key

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Fontes de Conhecimento

#### RAG (Retrieval Augmented Generation)
```bash
POST /api/v1/knowledge/sources/rag
{
  "name": "Documentos da Empresa",
  "documents": [...],
  "config": {
    "embedding_model": "text-embedding-ada-002",
    "chunk_size": 1000
  }
}
```

#### Website
```bash
POST /api/v1/knowledge/sources/website
{
  "name": "Site da Empresa",
  "urls": ["https://example.com"],
  "config": {
    "crawl_depth": 2,
    "max_pages": 100
  }
}
```

#### Document
```bash
POST /api/v1/knowledge/sources/document
{
  "name": "Manual Técnico",
  "file_paths": ["/uploads/manual.pdf"],
  "config": {
    "supported_formats": ["pdf", "txt", "docx"]
  }
}
```

#### MCP (Model Context Protocol)
```bash
POST /api/v1/knowledge/sources/mcp
{
  "name": "Context7 MCP",
  "server_url": "https://context7.example.com",
  "api_key": "your_api_key",
  "capabilities": ["search", "retrieval"]
}
```

## 🤖 Criação de Agentes e Workflows

### Templates de Workflow Disponíveis
- **research_workflow**: Pesquisa e análise com múltiplos agentes
- **writing_workflow**: Criação de conteúdo colaborativa
- **analysis_workflow**: Análise e relatórios estruturados

### Criar Workflow Customizado
```bash
POST /teams/create-workflow
{
  "session_id": "session-123",
  "task_description": "Analisar dados de vendas e criar relatório"
}
```

### Criar Workflow por Template
```bash
POST /teams/create-from-template
{
  "session_id": "session-123",
  "template_name": "research_workflow",
  "custom_config": {
    "name": "Análise de Dados",
    "description": "Workflow personalizado para análise"
  }
}
```

### Criar Agente Individual
```bash
POST /agents/
{
  "session_id": "session-123",
  "name": "Analista de Dados",
  "description": "Especialista em análise de dados",
  "type": "agent",
  "model": "gpt-4"
}
```

## 📊 Monitoramento

### Health Checks
- Gabi Chat: http://localhost:3000
- Gabi OS: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

### Logs
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f gabi-os
docker-compose logs -f gabi-chat
```

### Status dos Serviços
```bash
docker-compose ps
```

## 🔄 Desenvolvimento

### Gabi Chat
```bash
cd .
npm install
npm run dev
```

### Gabi OS
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Banco de Dados
```bash
# Migrações
alembic upgrade head

# Nova migração
alembic revision --autogenerate -m "description"
```

## 🚀 Deployment em Produção

### Com Portainer
1. Configure Portainer com Traefik
2. Use o docker-compose.yml fornecido
3. Configure SSL automaticamente
4. Monitore via Portainer dashboard

### Variáveis de Produção
- Use banco Neon para todos os ambientes (desenvolvimento e produção)
- Configure CORS adequadamente
- Use secrets para API keys
- Configure backup automático do Neon

## 🔗 Integração com Agno SDK

Este projeto implementa o padrão BMAD seguindo o documento oficial do Agno:

### Características da Implementação
- **Compatibilidade Total**: API compatível com Agno UI
- **Padrão BMAD**: Estruturação dinâmica de agentes
- **Workflows Inteligentes**: Criação automática baseada em descrição de tarefas
- **Templates Pré-definidos**: Workflows para pesquisa, escrita e análise
- **Banco Neon**: Persistência em banco Neon para todos os ambientes

### Endpoints Principais
- `GET /agents/` - Lista agentes disponíveis
- `POST /agents/` - Cria novo agente
- `GET /sessions/` - Lista sessões ativas
- `POST /sessions/` - Cria nova sessão
- `GET /teams/` - Lista workflows/teams
- `POST /teams/create-workflow` - Cria workflow customizado
- `POST /teams/create-from-template` - Cria workflow por template

## 📚 Documentação

### API Documentation
Acesse a documentação interativa em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Agno SDK Integration Guide
- [Guia Completo de Integração Agno SDK](AGNO_SDK_INTEGRATION_GUIDE.md)
- Documentação completa de todas as possibilidades de integração
- Exemplos práticos de implementação
- Guias de migração e configuração

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 🆘 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação da API
- Verifique os logs dos serviços