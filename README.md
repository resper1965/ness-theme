# Gabi - Chat Multi-Agentes

Um chat inteligente baseado no padrão BMAD com tecnologia Agno SDK, permitindo criação dinâmica de agentes e múltiplas fontes de conhecimento.

## 🚀 Características

- **Chat Multi-Agentes**: Criação dinâmica de até 3 agentes + 1 orquestrador por sessão
- **Múltiplas Fontes de Conhecimento**: RAG, sites, documentos, MCP servers
- **Tecnologia Agno SDK**: Integração com Agno para orquestração de agentes
- **Interface Moderna**: Design dark-first com design system ness
- **Deployment Docker**: Configuração completa com Portainer e Traefik

## 🏗️ Arquitetura

### Gabi Chat (Next.js)
- Interface de chat moderna
- Design system ness com cores frias
- Componentes reutilizáveis
- Estado gerenciado com Zustand

### Gabi OS (Python + FastAPI)
- API REST completa
- Integração com Agno SDK
- Gerenciamento de agentes dinâmicos
- Múltiplas fontes de conhecimento
- Banco de dados Supabase Local

### Infraestrutura
- Docker Compose para orquestração
- Nginx como proxy reverso
- Redis para cache e sessões
- Supabase Local para persistência
- Portainer para gerenciamento

## 🛠️ Instalação

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento)
- Python 3.11+ (para desenvolvimento)

### Deployment Automático
```bash
# Executar script de deployment
./scripts/deploy.sh
```

### Deployment Manual
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
# Supabase Local Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gabi

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

## 🤖 Criação de Agentes

### Templates Disponíveis
- **research_agent**: Pesquisa e análise
- **writing_agent**: Criação de conteúdo
- **analysis_agent**: Análise de dados
- **orchestrator**: Coordenação de agentes

### Criar Workflow de Agentes
```bash
POST /api/v1/workflows/create-workflow
{
  "session_id": "session-123",
  "task_description": "Analisar dados de vendas e criar relatório"
}
```

### Criar Agente por Template
```bash
POST /api/v1/workflows/create-from-template
{
  "session_id": "session-123",
  "template_name": "research_agent",
  "custom_config": {
    "name": "Analista de Dados",
    "model": "gpt-4"
  }
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
- Use banco Neon para produção
- Configure CORS adequadamente
- Use secrets para API keys
- Configure backup automático

## 📚 API Documentation

Acesse a documentação interativa em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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