-- Script de inicialização do banco de dados Gabi
-- Criação de extensões e configurações iniciais

-- Extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurações de performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Recarregar configurações
SELECT pg_reload_conf();

-- Criar usuário específico para aplicação (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'gabi_app') THEN
        CREATE ROLE gabi_app WITH LOGIN PASSWORD 'gabi_app_password';
    END IF;
END
$$;

-- Conceder permissões
GRANT CONNECT ON DATABASE gabi TO gabi_app;
GRANT USAGE ON SCHEMA public TO gabi_app;
GRANT CREATE ON SCHEMA public TO gabi_app;

-- Configurações de timezone
SET timezone = 'UTC';
