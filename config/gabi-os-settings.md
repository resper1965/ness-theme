# ⚙️ Configurações do Gabi.OS

## 🔑 **Chaves de API (Obrigatórias)**

```bash
# OpenAI API Key - Necessária para modelos de IA
OPENAI_API_KEY=sk-your-openai-api-key-here

# Agno SDK API Key - Necessária para integração com Agno
AGNO_API_KEY=your-agno-api-key-here
```

## 🗄️ **Banco de Dados**

```bash
# URL de conexão com PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database

# Para desenvolvimento local
POSTGRES_DB=gabi
POSTGRES_USER=gabi
POSTGRES_PASSWORD=gabi123
```

## 🔒 **Segurança**

```bash
# Chave secreta para JWT e criptografia
SECRET_KEY=your-super-secret-key-here-change-in-production
```

## 🌐 **CORS e Hosts**

```bash
# Origens permitidas para CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://yourdomain.com

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

## 🚀 **Ambiente**

```bash
# Ambiente de execução
ENVIRONMENT=production  # ou development

# Debug mode
DEBUG=false  # ou true para desenvolvimento
```

## 📊 **Configurações de Agentes**

```bash
# Máximo de agentes por sessão
MAX_AGENTS_PER_SESSION=3

# Máximo de orquestradores por sessão
MAX_ORCHESTRATOR_PER_SESSION=1

# Máximo de fontes de conhecimento
MAX_KB_SOURCES=10
```

## 🔧 **URLs de API**

```bash
# URL da API do backend (para frontend)
NEXT_PUBLIC_API_URL=http://localhost:7777
```

## 📁 **Volumes e Logs**

```bash
# Caminhos para dados persistentes
DATA_PATH=/app/data
LOGS_PATH=/app/logs
UPLOADS_PATH=/app/uploads
```

## 🚀 **Como Configurar**

1. **Copie o arquivo de exemplo:**
   ```bash
   cp config/env.example .env
   ```

2. **Edite as variáveis:**
   ```bash
   nano .env
   ```

3. **Configure as chaves de API:**
   - Obtenha sua chave OpenAI em: https://platform.openai.com/api-keys
   - Obtenha sua chave Agno em: https://agno.ai

4. **Configure o banco de dados:**
   - Para produção: Use Neon Database
   - Para desenvolvimento: Use PostgreSQL local

5. **Inicie o sistema:**
   ```bash
   docker-compose up -d
   ```

## ⚠️ **Importante**

- **Nunca** commite o arquivo `.env` no Git
- Use chaves diferentes para desenvolvimento e produção
- Mantenha as chaves de API seguras
- Configure CORS adequadamente para seu domínio
