# 🚀 Deploy em Produção - Gabi

Este documento descreve como fazer o deploy do Gabi em produção usando Docker, Traefik e SSL automático.

## 📋 Pré-requisitos

### 1. Infraestrutura
- **VPS/Server** com Docker e Docker Compose
- **Domínio** configurado apontando para o servidor
- **Traefik** rodando com Portainer [[memory:7438586]]
- **Portas** 80 e 443 abertas

### 2. Configurações
- **Agno SDK** instalado e configurado [[memory:8871375]]
- **OpenAI API Key** válida
- **Domínio** configurado

## 🔧 Configuração

### 1. Preparar Ambiente

```bash
# 1. Clonar o repositório
git clone <seu-repositorio>
cd Gabi

# 2. Configurar variáveis de ambiente
cp env.production .env
```

### 2. Editar .env

```bash
# Domínio principal
DOMAIN=gabi.exemplo.com

# Database
DATABASE_URL=postgresql://postgres:postgres@supabase-db:5432/gabi
POSTGRES_DB=gabi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Agno SDK
AGNO_API_KEY=sua_chave_agno_aqui
OPENAI_API_KEY=sua_chave_openai_aqui

# Security
SECRET_KEY=sua_chave_secreta_producao_aqui

# CORS
CORS_ORIGINS=https://gabi.exemplo.com,https://www.gabi.exemplo.com
ALLOWED_HOSTS=gabi.exemplo.com,www.gabi.exemplo.com

# Environment
ENVIRONMENT=production
DEBUG=false
NODE_ENV=production

# API URLs
NEXT_PUBLIC_API_URL=https://gabi.exemplo.com/api
```

### 3. Verificar Traefik

Certifique-se de que o Traefik está rodando com Portainer e a rede `traefik` existe:

```bash
docker network ls | grep traefik
```

## 🚀 Deploy

### Deploy Automático

```bash
# Executar script de deploy
./scripts/deploy-production.sh
```

### Deploy Manual

```bash
# 1. Parar containers existentes
docker-compose -f docker-compose.production.yml down

# 2. Construir imagens
docker-compose -f docker-compose.production.yml build --no-cache

# 3. Iniciar serviços
docker-compose -f docker-compose.production.yml up -d

# 4. Verificar logs
docker-compose -f docker-compose.production.yml logs -f
```

## 🔍 Verificação

### URLs de Acesso

- **Frontend**: https://gabi.exemplo.com
- **Backend API**: https://gabi.exemplo.com/api
- **API Docs**: https://gabi.exemplo.com/api/docs
- **Supabase Studio**: https://studio.gabi.exemplo.com

### Health Checks

```bash
# Frontend
curl -f https://gabi.exemplo.com

# Backend
curl -f https://gabi.exemplo.com/api/health

# Supabase Studio
curl -f https://studio.gabi.exemplo.com
```

## 🛠️ Comandos Úteis

### Gerenciamento de Containers

```bash
# Ver status
docker-compose -f docker-compose.production.yml ps

# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Restart
docker-compose -f docker-compose.production.yml restart

# Parar
docker-compose -f docker-compose.production.yml down

# Update
docker-compose -f docker-compose.production.yml pull
docker-compose -f docker-compose.production.yml up -d
```

### Backup

```bash
# Backup do banco de dados
docker-compose -f docker-compose.production.yml exec supabase-db pg_dump -U postgres gabi > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup dos volumes
docker run --rm -v gabi_supabase_db_data:/data -v $(pwd):/backup alpine tar czf /backup/supabase_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

## 🔒 Segurança

### SSL/HTTPS
- **Automático** via Let's Encrypt com Traefik
- **Renovação** automática
- **Redirecionamento** HTTP → HTTPS

### Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable
```

### Secrets
- **Nunca** commitar arquivos `.env`
- **Rotacionar** chaves regularmente
- **Usar** variáveis de ambiente no Portainer

## 📊 Monitoramento

### Logs
```bash
# Todos os serviços
docker-compose -f docker-compose.production.yml logs -f

# Serviço específico
docker-compose -f docker-compose.production.yml logs -f gabi-chat
docker-compose -f docker-compose.production.yml logs -f gabi-os
```

### Métricas
- **Portainer** para monitoramento de containers
- **Traefik** para métricas de proxy
- **Supabase Studio** para métricas de banco

## 🚨 Troubleshooting

### Problemas Comuns

1. **SSL não funciona**
   - Verificar se o domínio aponta para o servidor
   - Verificar se o Traefik está rodando
   - Verificar logs do Traefik

2. **Backend não responde**
   - Verificar logs: `docker-compose logs gabi-os`
   - Verificar variáveis de ambiente
   - Verificar conexão com banco

3. **Frontend não carrega**
   - Verificar logs: `docker-compose logs gabi-chat`
   - Verificar NEXT_PUBLIC_API_URL
   - Verificar CORS settings

4. **Banco de dados não conecta**
   - Verificar logs: `docker-compose logs supabase-db`
   - Verificar DATABASE_URL
   - Verificar volumes

### Logs Importantes

```bash
# Traefik
docker logs traefik

# Gabi Backend
docker-compose -f docker-compose.production.yml logs gabi-os

# Gabi Frontend
docker-compose -f docker-compose.production.yml logs gabi-chat

# Supabase
docker-compose -f docker-compose.production.yml logs supabase-db
```

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs
2. Verificar configurações
3. Verificar documentação
4. Abrir issue no repositório
