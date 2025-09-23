#!/bin/bash

# Script de deployment do Gabi
# Configuração para Portainer e Traefik

set -e

echo "🚀 Iniciando deployment do Gabi..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não encontrado. Instale primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp env.example .env
    echo "⚠️  Configure as variáveis no arquivo .env antes de continuar."
    echo "   - DATABASE_URL (Neon)"
    echo "   - AGNO_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - SECRET_KEY"
    read -p "Pressione Enter após configurar o .env..."
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p backend/data backend/logs backend/uploads

# Build das imagens
echo "🔨 Construindo imagens Docker..."
docker-compose build --no-cache

# Executar migrações do banco
echo "🗄️ Executando migrações do banco..."
docker-compose run --rm gabi-os alembic upgrade head

echo "🔧 Configurando Supabase Local..."
# Aguardar Supabase estar pronto
sleep 15

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose up -d

# Verificar saúde dos serviços
echo "🏥 Verificando saúde dos serviços..."
sleep 10

# Health checks
echo "Gabi Chat: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "❌")"
echo "Gabi OS: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "❌")"
echo "Supabase DB: $(docker-compose exec -T supabase-db pg_isready -U postgres -d gabi && echo "✅" || echo "❌")"
echo "Supabase Studio: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001 || echo "❌")"
echo "Redis: $(docker-compose exec -T redis redis-cli ping && echo "✅" || echo "❌")"

echo ""
echo "✅ Deployment concluído!"
echo ""
echo "🌐 URLs:"
echo "   Gabi Chat: http://localhost:3000"
echo "   Gabi OS API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Supabase Studio: http://localhost:3001"
echo "   Supabase DB: postgresql://postgres:postgres@localhost:5432/gabi"
echo ""
echo "📊 Monitoramento:"
echo "   Logs: docker-compose logs -f"
echo "   Status: docker-compose ps"
echo ""
echo "🛑 Para parar: docker-compose down"
