-- Script para restaurar backup do SQL Server
-- Aguarda o SQL Server ficar pronto
WAITFOR DELAY '00:00:30';

-- Lista os arquivos do backup para identificar os nomes lógicos
RESTORE FILELISTONLY FROM DISK = '/backup/REB_BI_IA.bak';

-- Restaura o banco de dados
RESTORE DATABASE [REB_BI_IA] 
FROM DISK = '/backup/REB_BI_IA.bak'
WITH 
  MOVE 'REB_BI_IA' TO '/var/opt/mssql/data/REB_BI_IA.mdf',
  MOVE 'REB_BI_IA_Log' TO '/var/opt/mssql/data/REB_BI_IA_Log.ldf',
  REPLACE,
  STATS = 10;

-- Verifica se o banco foi restaurado
SELECT name, database_id, create_date 
FROM sys.databases 
WHERE name = 'REB_BI_IA';

PRINT 'Backup REB_BI_IA restaurado com sucesso!';
