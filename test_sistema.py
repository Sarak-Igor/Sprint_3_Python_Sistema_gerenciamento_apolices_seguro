"""
Script de teste para validar o sistema
"""

import os
import sys
from database import DatabaseManager
from auth_sqlite import AuthManager
from relatorios_sqlite import RelatorioManager

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    try:
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✅ Banco conectado. Tabelas encontradas: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_authentication():
    """Testa sistema de autenticação"""
    print("\n🔍 Testando sistema de autenticação...")
    try:
        auth = AuthManager()
        
        # Teste de login com credenciais padrão
        if auth.login("admin", "password"):
            print("✅ Login admin bem-sucedido")
            
            # Teste de permissões
            if auth.is_admin():
                print("✅ Permissões de admin verificadas")
            else:
                print("❌ Permissões de admin não funcionando")
                return False
            
            # Teste de logout
            if auth.logout():
                print("✅ Logout bem-sucedido")
            else:
                print("❌ Logout falhou")
                return False
        else:
            print("❌ Login admin falhou")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return False

def test_reports():
    """Testa sistema de relatórios"""
    print("\n🔍 Testando sistema de relatórios...")
    try:
        relatorios = RelatorioManager()
        
        # Teste de relatórios disponíveis
        relatorios_disponiveis = relatorios.listar_relatorios_disponiveis()
        print(f"✅ Relatórios disponíveis: {len(relatorios_disponiveis)}")
        for rel in relatorios_disponiveis:
            print(f"   - {rel['nome']}: {rel['descricao']}")
        
        # Teste de relatório de sinistros por status (não requer dados)
        try:
            dados = relatorios.gerar_sinistros_por_status()
            print("✅ Relatório de sinistros por status funcionando")
        except Exception as e:
            print(f"⚠️ Relatório de sinistros: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erro nos relatórios: {e}")
        return False

def test_file_structure():
    """Testa estrutura de arquivos"""
    print("\n🔍 Testando estrutura de arquivos...")
    
    arquivos_necessarios = [
        "main.py",
        "cli_sqlite.py", 
        "database.py",
        "auth_sqlite.py",
        "relatorios_sqlite.py",
        "logger_config.py",
        "exceptions.py",
        "migrate.py",
        "schema.sql",
        "requirements.txt",
        "README.md"
    ]
    
    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            arquivos_faltando.append(arquivo)
        else:
            print(f"✅ {arquivo}")
    
    if arquivos_faltando:
        print(f"❌ Arquivos faltando: {arquivos_faltando}")
        return False
    
    print("✅ Todos os arquivos necessários estão presentes")
    return True

def test_directories():
    """Testa criação de diretórios"""
    print("\n🔍 Testando diretórios...")
    
    diretorios = ["export"]
    
    for diretorio in diretorios:
        if os.path.exists(diretorio):
            print(f"✅ Diretório {diretorio} existe")
        else:
            print(f"⚠️ Diretório {diretorio} será criado automaticamente")
    
    return True

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("    TESTE DO SISTEMA DE SEGUROS - SQLite")
    print("=" * 60)
    
    testes = [
        ("Estrutura de Arquivos", test_file_structure),
        ("Diretórios", test_directories),
        ("Conexão com Banco", test_database_connection),
        ("Sistema de Autenticação", test_authentication),
        ("Sistema de Relatórios", test_reports)
    ]
    
    resultados = []
    
    for nome, teste in testes:
        print(f"\n{'='*20} {nome} {'='*20}")
        try:
            resultado = teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            resultados.append((nome, False))
    
    # Relatório final
    print("\n" + "=" * 60)
    print("           RELATÓRIO FINAL")
    print("=" * 60)
    
    sucessos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
    
    print(f"\nResultado: {sucessos}/{total} testes passaram")
    
    if sucessos == total:
        print("🎉 SISTEMA PRONTO PARA USO!")
        print("\nPara iniciar o sistema:")
        print("1. Execute: python migrate.py (primeira vez)")
        print("2. Execute: python main.py")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("Verifique os erros acima antes de usar o sistema")
    
    return sucessos == total

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
