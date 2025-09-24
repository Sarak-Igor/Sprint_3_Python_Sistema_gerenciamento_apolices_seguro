"""
Teste da interface gráfica
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_dependencies():
    """Testa se as dependências estão instaladas"""
    print("🔍 Testando dependências...")
    
    try:
        import ttkthemes
        print("✅ ttkthemes instalado")
    except ImportError:
        print("❌ ttkthemes não encontrado")
        return False
    
    try:
        import pandas
        print("✅ pandas instalado")
    except ImportError:
        print("❌ pandas não encontrado")
        return False
    
    try:
        from database import DatabaseManager
        print("✅ database.py encontrado")
    except ImportError:
        print("❌ database.py não encontrado")
        return False
    
    try:
        from auth_sqlite import AuthManager
        print("✅ auth_sqlite.py encontrado")
    except ImportError:
        print("❌ auth_sqlite.py não encontrado")
        return False
    
    try:
        from relatorios_sqlite import RelatorioManager
        print("✅ relatorios_sqlite.py encontrado")
    except ImportError:
        print("❌ relatorios_sqlite.py não encontrado")
        return False
    
    return True

def test_database():
    """Testa conexão com banco de dados"""
    print("\n🔍 Testando banco de dados...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✅ Banco conectado. Tabelas: {len(tables)}")
            return True
    except Exception as e:
        print(f"❌ Erro no banco: {e}")
        return False

def test_gui_creation():
    """Testa criação da interface gráfica"""
    print("\n🔍 Testando criação da interface...")
    
    try:
        from interface_sqlite import SeguroAppSQLite
        from ttkthemes import ThemedTk
        
        # Criar janela de teste
        root = ThemedTk(theme="adapta")
        root.withdraw()  # Esconder janela
        
        app = SeguroAppSQLite(root, None)
        print("✅ Interface criada com sucesso")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("    TESTE DA INTERFACE GRÁFICA")
    print("=" * 60)
    
    testes = [
        ("Dependências", test_dependencies),
        ("Banco de Dados", test_database),
        ("Interface Gráfica", test_gui_creation)
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
        print("🎉 INTERFACE GRÁFICA PRONTA!")
        print("\nPara iniciar a interface gráfica:")
        print("1. Execute: python migrate.py (primeira vez)")
        print("2. Execute: python main_gui.py")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("Instale as dependências: pip install -r requirements.txt")
    
    return sucessos == total

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
