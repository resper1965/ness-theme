#!/bin/bash

# Gabi Production Deployment Script
# Configurado para usar Traefik com SSL automático

set -e

echo "🚀 Iniciando deploy do Gabi em produção..."

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copiando env.production para .env..."
    cp env.production .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas configurações antes de continuar!"
    echo "   - DOMAIN: seu domínio (ex: gabi.exemplo.com)"
    echo "   - AGNO_API_KEY: sua chave da API Agno"
    echo "   - OPENAI_API_KEY: sua chave da API OpenAI"
    echo "   - SECRET_KEY: chave secreta para produção"
    echo ""
    read -p "Pressione Enter após editar o .env..."
fi

# Carregar variáveis de ambiente
source .env

# Verificar variáveis obrigatórias
if [ -z "$DOMAIN" ]; then
    echo "❌ DOMAIN não definido no .env!"
    exit 1
fi

if [ -z "$AGNO_API_KEY" ] || [ "$AGNO_API_KEY" = "your_agno_api_key_here" ]; then
    echo "❌ AGNO_API_KEY não configurado no .env!"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ OPENAI_API_KEY não configurado no .env!"
    exit 1
fi

if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your_production_secret_key_here" ]; then
    echo "❌ SECRET_KEY não configurado no .env!"
    exit 1
fi

echo "✅ Variáveis de ambiente verificadas"

# Verificar se Traefik está rodando
if ! docker network ls | grep -q traefik; then
    echo "❌ Rede Traefik não encontrada!"
    echo "📝 Certifique-se de que o Traefik está rodando com Portainer"
    exit 1
fi

echo "✅ Traefik detectado"

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f docker-compose.production.yml down || true

# Construir imagens
echo "🔨 Construindo imagens..."
docker-compose -f docker-compose.production.yml build --no-cache

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose -f docker-compose.production.yml up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar saúde dos serviços
echo "🔍 Verificando saúde dos serviços..."

# Verificar frontend
if curl -f -s "https://$DOMAIN" > /dev/null; then
    echo "✅ Frontend: https://$DOMAIN"
else
    echo "❌ Frontend não está respondendo"
fi

# Verificar backend
if curl -f -s "https://$DOMAIN/api/health" > /dev/null; then
    echo "✅ Backend: https://$DOMAIN/api/health"
else
    echo "❌ Backend não está respondendo"
fi

# Verificar Supabase Studio
if curl -f -s "https://studio.$DOMAIN" > /dev/null; then
    echo "✅ Supabase Studio: https://studio.$DOMAIN"
else
    echo "❌ Supabase Studio não está respondendo"
fi

echo ""
echo "🎉 Deploy concluído!"
echo ""
echo "📋 URLs de acesso:"
echo "   - Frontend: https://$DOMAIN"
echo "   - Backend API: https://$DOMAIN/api"
echo "   - Supabase Studio: https://studio.$DOMAIN"
echo "   - API Docs: https://$DOMAIN/api/docs"
echo ""
echo "🔧 Comandos úteis:"
echo "   - Ver logs: docker-compose -f docker-compose.production.yml logs -f"
echo "   - Parar: docker-compose -f docker-compose.production.yml down"
echo "   - Restart: docker-compose -f docker-compose.production.yml restart"
echo ""
