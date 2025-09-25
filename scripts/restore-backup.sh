#!/bin/bash

echo "🚀 Iniciando restauração do backup REB_BI_IA..."

# Aguarda o SQL Server ficar pronto
echo "⏳ Aguardando SQL Server ficar pronto..."
sleep 60

# Verifica se o SQL Server está rodando
echo "🔍 Verificando conexão com SQL Server..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -Q "SELECT 1" || {
    echo "❌ Erro: Não foi possível conectar ao SQL Server"
    exit 1
}

echo "✅ SQL Server está rodando!"

# Lista os arquivos do backup para identificar os nomes lógicos
echo "📋 Listando arquivos do backup..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -Q "RESTORE FILELISTONLY FROM DISK = '/backup/REB_BI_IA.bak'"

# Restaura o banco de dados
echo "🔄 Restaurando banco REB_BI_IA..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -Q "
RESTORE DATABASE [REB_BI_IA] 
FROM DISK = '/backup/REB_BI_IA.bak'
WITH 
  MOVE 'REB_BI_IA' TO '/var/opt/mssql/data/REB_BI_IA.mdf',
  MOVE 'REB_BI_IA_Log' TO '/var/opt/mssql/data/REB_BI_IA_Log.ldf',
  REPLACE,
  STATS = 10
"

if [ $? -eq 0 ]; then
    echo "✅ Backup REB_BI_IA restaurado com sucesso!"
    
    # Verifica se o banco foi restaurado
    echo "🔍 Verificando banco restaurado..."
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "Gabi123!" -Q "
    SELECT name, database_id, create_date 
    FROM sys.databases 
    WHERE name = 'REB_BI_IA'
    "
    
    echo "🎉 Banco REB_BI_IA está disponível em: localhost:1433"
    echo "📊 Usuário: sa | Senha: Gabi123!"
else
    echo "❌ Erro ao restaurar backup"
    exit 1
fi
