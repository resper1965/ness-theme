#!/usr/bin/env python3
"""
Script para restaurar backup do SQL Server usando pyodbc
"""
import pyodbc
import time
import sys
import os

def wait_for_sql_server(server, username, password, timeout=300):
    """Aguarda o SQL Server ficar disponível"""
    print("⏳ Aguardando SQL Server ficar pronto...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};UID={username};PWD={password};TrustServerCertificate=yes;"
            conn = pyodbc.connect(conn_str, timeout=5)
            conn.close()
            print("✅ SQL Server está pronto!")
            return True
        except Exception as e:
            print(f"⏳ Aguardando... ({int(time.time() - start_time)}s)")
            time.sleep(5)
    
    print("❌ Timeout aguardando SQL Server")
    return False

def restore_database(server, username, password, backup_path):
    """Restaura o banco de dados do backup"""
    try:
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};UID={username};PWD={password};TrustServerCertificate=yes;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print("📋 Listando arquivos do backup...")
        cursor.execute(f"RESTORE FILELISTONLY FROM DISK = '{backup_path}'")
        files = cursor.fetchall()
        
        print("📁 Arquivos encontrados no backup:")
        for file_info in files:
            print(f"  - {file_info[0]} ({file_info[1]})")
        
        # Determina os nomes lógicos dos arquivos
        data_file = None
        log_file = None
        
        for file_info in files:
            if file_info[1] == 'D':  # Data file
                data_file = file_info[0]
            elif file_info[1] == 'L':  # Log file
                log_file = file_info[0]
        
        if not data_file or not log_file:
            print("❌ Não foi possível identificar os arquivos do banco")
            return False
        
        print(f"🗄️ Arquivo de dados: {data_file}")
        print(f"📝 Arquivo de log: {log_file}")
        
        # Restaura o banco
        print("🔄 Restaurando banco REB_BI_IA...")
        restore_sql = f"""
        RESTORE DATABASE [REB_BI_IA] 
        FROM DISK = '{backup_path}'
        WITH 
          MOVE '{data_file}' TO '/var/opt/mssql/data/REB_BI_IA.mdf',
          MOVE '{log_file}' TO '/var/opt/mssql/data/REB_BI_IA_Log.ldf',
          REPLACE,
          STATS = 10
        """
        
        cursor.execute(restore_sql)
        conn.commit()
        
        print("✅ Backup REB_BI_IA restaurado com sucesso!")
        
        # Verifica se o banco foi restaurado
        print("🔍 Verificando banco restaurado...")
        cursor.execute("""
        SELECT name, database_id, create_date 
        FROM sys.databases 
        WHERE name = 'REB_BI_IA'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Banco encontrado: {result[0]} (ID: {result[1]})")
            print(f"📅 Criado em: {result[2]}")
        else:
            print("❌ Banco não encontrado após restauração")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {e}")
        return False

def main():
    server = "localhost"
    username = "sa"
    password = "Gabi123!"
    backup_path = "/backup/REB_BI_IA.bak"
    
    print("🚀 Iniciando restauração do backup REB_BI_IA...")
    
    # Verifica se o arquivo de backup existe
    if not os.path.exists(backup_path):
        print(f"❌ Arquivo de backup não encontrado: {backup_path}")
        sys.exit(1)
    
    print(f"📁 Arquivo de backup encontrado: {backup_path}")
    print(f"📊 Tamanho: {os.path.getsize(backup_path) / (1024*1024*1024):.2f} GB")
    
    # Aguarda SQL Server ficar pronto
    if not wait_for_sql_server(server, username, password):
        sys.exit(1)
    
    # Restaura o banco
    if restore_database(server, username, password, backup_path):
        print("🎉 Banco REB_BI_IA está disponível em: localhost:1433")
        print("📊 Usuário: sa | Senha: Gabi123!")
    else:
        print("❌ Falha na restauração do backup")
        sys.exit(1)

if __name__ == "__main__":
    main()
