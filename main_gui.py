"""
Ponto de entrada principal para interface gráfica
Mantém compatibilidade com TTKthemes e interface existente
"""

import sys
import os
from tkinter import messagebox
from ttkthemes import ThemedTk
from login import LoginWindow

def main():
    """Função principal que inicia o sistema com interface gráfica"""
    try:
        # Verificar se é primeira execução (migração necessária)
        if not os.path.exists("seguradora.db"):
            resposta = messagebox.askyesno(
                "Primeira Execução", 
                "Este é o primeiro uso do sistema.\n\n"
                "Deseja migrar os dados dos arquivos JSON para o novo banco SQLite?\n\n"
                "Isso irá:\n"
                "- Criar o banco de dados SQLite\n"
                "- Migrar todos os dados existentes\n"
                "- Manter os arquivos JSON como backup"
            )
            
            if resposta:
                # Executar migração
                import subprocess
                try:
                    result = subprocess.run([sys.executable, "migrate.py"], 
                                          capture_output=True, text=True, check=True)
                    messagebox.showinfo("Migração", "Dados migrados com sucesso!")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Erro na Migração", 
                                       f"Erro ao migrar dados:\n{e.stderr}")
                    return
                except FileNotFoundError:
                    messagebox.showerror("Erro", "Arquivo migrate.py não encontrado!")
                    return
            else:
                messagebox.showinfo("Informação", 
                                  "Migração cancelada.\n"
                                  "O sistema será iniciado com banco vazio.")
        
        # Iniciar interface gráfica
        login_window = LoginWindow()
        login_window.executar()
        
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
