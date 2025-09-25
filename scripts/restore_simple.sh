#!/bin/bash

echo "🚀 Iniciando restauração do backup REB_BI_IA..."

# Aguarda o SQL Server ficar pronto
echo "⏳ Aguardando SQL Server ficar pronto..."
sleep 90

# Executa a restauração usando sqlcmd
echo "🔄 Restaurando banco REB_BI_IA..."

# Primeiro, lista os arquivos do backup para identificar os nomes lógicos
echo "📋 Listando arquivos do backup..."
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -C -Q "RESTORE FILELISTONLY FROM DISK = '/backup/REB_BI_IA.bak'" || {
    echo "❌ Erro ao listar arquivos do backup"
    exit 1
}

# Restaura o banco usando nomes genéricos
echo "🔄 Restaurando banco..."
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -C -Q "
RESTORE DATABASE [REB_BI_IA] 
FROM DISK = '/backup/REB_BI_IA.bak'
WITH 
  MOVE 'REB_BI_IA' TO '/var/opt/mssql/data/REB_BI_IA.mdf',
  MOVE 'REB_BI_IA_Log' TO '/var/opt/mssql/data/REB_BI_IA_Log.ldf',
  REPLACE,
  STATS = 10
" || {
    echo "❌ Erro ao restaurar backup"
    exit 1
}

echo "✅ Backup REB_BI_IA restaurado com sucesso!"

# Verifica se o banco foi restaurado
echo "🔍 Verificando banco restaurado..."
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -C -Q "
SELECT name, database_id, create_date 
FROM sys.databases 
WHERE name = 'REB_BI_IA'
"

echo "🎉 Banco REB_BI_IA está disponível em: localhost:1433"
echo "📊 Usuário: sa | Senha: Gabi123!"
