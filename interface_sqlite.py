"""
Interface gráfica adaptada para SQLite
Integra com o sistema existente mantendo TTKthemes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from database import DatabaseManager
from auth_sqlite import AuthManager
from relatorios_sqlite import RelatorioManager
from logger_config import get_auditoria

class SeguroAppSQLite:
    """Interface gráfica principal adaptada para SQLite"""
    
    def __init__(self, root, usuario_manager):
        self.root = root
        self.root.title("Sistema de Seguros - SQLite")
        self.root.geometry("1000x700")
        
        # Gerenciadores
        self.db = DatabaseManager()
        self.auth = AuthManager()
        self.relatorios = RelatorioManager()
        self.auditoria = get_auditoria()
        
        # Configurar interface
        self.setup_interface()
        
    def setup_interface(self):
        """Configura a interface principal"""
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Clientes
        self.tab_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clientes, text="Clientes")
        self.setup_clientes_tab()
        
        # Aba de Relatórios
        self.tab_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_relatorios, text="Relatórios")
        self.setup_relatorios_tab()
        
    def setup_clientes_tab(self):
        """Configura aba de clientes"""
        # Frame para cadastro
        frame_cadastro = ttk.LabelFrame(self.tab_clientes, text="Cadastrar Cliente", padding=10)
        frame_cadastro.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos do cliente
        ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.nome_entry = ttk.Entry(frame_cadastro, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_cadastro, text="CPF:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.cpf_entry = ttk.Entry(frame_cadastro, width=20)
        self.cpf_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_cadastro, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_entry = ttk.Entry(frame_cadastro, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_cadastro, text="Telefone:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.telefone_entry = ttk.Entry(frame_cadastro, width=20)
        self.telefone_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(frame_cadastro)
        frame_botoes.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(frame_botoes, text="Cadastrar", command=self.cadastrar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Buscar", command=self.buscar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        
        # Lista de clientes
        frame_lista = ttk.LabelFrame(self.tab_clientes, text="Lista de Clientes", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview para clientes
        colunas = ("ID", "Nome", "CPF", "Email", "Telefone")
        self.tree_clientes = ttk.Treeview(frame_lista, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Carregar clientes
        self.carregar_clientes()
        
    def setup_relatorios_tab(self):
        """Configura aba de relatórios"""
        # Frame para seleção de relatório
        frame_selecao = ttk.LabelFrame(self.tab_relatorios, text="Selecionar Relatório", padding=10)
        frame_selecao.pack(fill=tk.X, padx=10, pady=5)
        
        # Combo para tipos de relatório
        ttk.Label(frame_selecao, text="Tipo de Relatório:").pack(side=tk.LEFT, padx=5)
        self.combo_relatorio = ttk.Combobox(frame_selecao, values=[
            "Receita Mensal", "Top Clientes", "Sinistros por Status", 
            "Apólices Ativas", "Sinistros Recentes"
        ], state="readonly", width=20)
        self.combo_relatorio.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_selecao, text="Gerar Relatório", command=self.gerar_relatorio).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_selecao, text="Exportar CSV", command=self.exportar_relatorio).pack(side=tk.LEFT, padx=5)
        
        # Frame para parâmetros
        self.frame_parametros = ttk.Frame(frame_selecao)
        self.frame_parametros.pack(fill=tk.X, pady=5)
        
        # Área de resultados
        frame_resultados = ttk.LabelFrame(self.tab_relatorios, text="Resultados", padding=10)
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text widget para resultados
        self.text_resultados = tk.Text(frame_resultados, height=20, width=80)
        scrollbar_text = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_text.set)
        
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Dados do relatório atual
        self.relatorio_atual = None
        
    def cadastrar_cliente(self):
        """Cadastra novo cliente"""
        try:
            dados = {
                'nome': self.nome_entry.get(),
                'cpf': self.cpf_entry.get(),
                'data_nascimento': '01/01/1990',  # Padrão
                'endereco': 'Endereço não informado',
                'telefone': self.telefone_entry.get(),
                'email': self.email_entry.get()
            }
            
            if not dados['nome'] or not dados['cpf']:
                messagebox.showerror("Erro", "Nome e CPF são obrigatórios!")
                return
            
            cliente_id = self.db.criar_cliente(dados, 1)  # user_id = 1 (admin)
            if cliente_id:
                messagebox.showinfo("Sucesso", f"Cliente cadastrado com ID: {cliente_id}")
                self.limpar_campos()
                self.carregar_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar cliente!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")
    
    def buscar_cliente(self):
        """Busca cliente por CPF"""
        cpf = self.cpf_entry.get()
        if not cpf:
            messagebox.showwarning("Aviso", "Digite um CPF para buscar!")
            return
        
        cliente = self.db.obter_cliente_por_cpf(cpf)
        if cliente:
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, cliente['nome'])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, cliente['email'])
            self.telefone_entry.delete(0, tk.END)
            self.telefone_entry.insert(0, cliente['telefone'])
        else:
            messagebox.showinfo("Informação", "Cliente não encontrado!")
    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
    
    def carregar_clientes(self):
        """Carrega lista de clientes"""
        try:
            # Limpar treeview
            for item in self.tree_clientes.get_children():
                self.tree_clientes.delete(item)
            
            clientes = self.db.listar_clientes()
            for cliente in clientes:
                self.tree_clientes.insert("", tk.END, values=(
                    cliente['id'],
                    cliente['nome'],
                    cliente['cpf'],
                    cliente['email'],
                    cliente['telefone']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes: {e}")
    
    def gerar_relatorio(self):
        """Gera relatório selecionado"""
        tipo = self.combo_relatorio.get()
        if not tipo:
            messagebox.showwarning("Aviso", "Selecione um tipo de relatório!")
            return
        
        try:
            # Limpar parâmetros anteriores
            for widget in self.frame_parametros.winfo_children():
                widget.destroy()
            
            # Configurar parâmetros baseado no tipo
            if tipo == "Receita Mensal":
                ttk.Label(self.frame_parametros, text="Mês:").pack(side=tk.LEFT, padx=5)
                self.entry_mes = ttk.Entry(self.frame_parametros, width=5)
                self.entry_mes.pack(side=tk.LEFT, padx=5)
                self.entry_mes.insert(0, "1")
                
                ttk.Label(self.frame_parametros, text="Ano:").pack(side=tk.LEFT, padx=5)
                self.entry_ano = ttk.Entry(self.frame_parametros, width=8)
                self.entry_ano.pack(side=tk.LEFT, padx=5)
                self.entry_ano.insert(0, "2024")
                
            elif tipo == "Sinistros Recentes":
                ttk.Label(self.frame_parametros, text="Dias:").pack(side=tk.LEFT, padx=5)
                self.entry_dias = ttk.Entry(self.frame_parametros, width=5)
                self.entry_dias.pack(side=tk.LEFT, padx=5)
                self.entry_dias.insert(0, "30")
            
            # Gerar relatório
            if tipo == "Receita Mensal":
                mes = int(self.entry_mes.get())
                ano = int(self.entry_ano.get())
                self.relatorio_atual = self.relatorios.gerar_receita_mensal(mes, ano)
            elif tipo == "Top Clientes":
                self.relatorio_atual = self.relatorios.gerar_top_clientes(5)
            elif tipo == "Sinistros por Status":
                self.relatorio_atual = self.relatorios.gerar_sinistros_por_status()
            elif tipo == "Apólices Ativas":
                self.relatorio_atual = self.relatorios.gerar_relatorio_apolices_ativas()
            elif tipo == "Sinistros Recentes":
                dias = int(self.entry_dias.get())
                self.relatorio_atual = self.relatorios.gerar_relatorio_sinistros_recentes(dias)
            
            # Exibir resultados
            self.exibir_relatorio()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def exibir_relatorio(self):
        """Exibe relatório no text widget"""
        if not self.relatorio_atual:
            return
        
        self.text_resultados.delete(1.0, tk.END)
        
        # Formatação baseada no tipo de relatório
        if 'receita_total' in self.relatorio_atual:
            self.text_resultados.insert(tk.END, f"RECEITA MENSAL - {self.relatorio_atual['mes']:02d}/{self.relatorio_atual['ano']}\n")
            self.text_resultados.insert(tk.END, "=" * 50 + "\n")
            self.text_resultados.insert(tk.END, f"Receita Total: R$ {self.relatorio_atual['receita_total']:,.2f}\n")
            self.text_resultados.insert(tk.END, f"Quantidade de Apólices: {self.relatorio_atual['quantidade_apolices']}\n\n")
            
            if self.relatorio_atual['detalhes']:
                self.text_resultados.insert(tk.END, "DETALHES:\n")
                for item in self.relatorio_atual['detalhes']:
                    self.text_resultados.insert(tk.END, f"Apólice: {item['numero']} | Cliente: {item['cliente']} | Prêmio: R$ {item['premio']:,.2f}\n")
        
        elif 'clientes' in self.relatorio_atual:
            self.text_resultados.insert(tk.END, f"TOP {self.relatorio_atual['limite']} CLIENTES\n")
            self.text_resultados.insert(tk.END, "=" * 50 + "\n")
            for i, cliente in enumerate(self.relatorio_atual['clientes'], 1):
                self.text_resultados.insert(tk.END, f"{i}. {cliente['nome']} - CPF: {cliente['cpf']}\n")
                self.text_resultados.insert(tk.END, f"   Total Segurado: R$ {cliente['total_segurado']:,.2f}\n")
                self.text_resultados.insert(tk.END, f"   Número de Apólices: {cliente['num_apolices']}\n\n")
        
        elif 'por_status' in self.relatorio_atual:
            self.text_resultados.insert(tk.END, "SINISTROS POR STATUS\n")
            self.text_resultados.insert(tk.END, "=" * 50 + "\n")
            self.text_resultados.insert(tk.END, f"Total de Sinistros: {self.relatorio_atual['total_sinistros']}\n")
            self.text_resultados.insert(tk.END, f"Total de Prejuízo: R$ {self.relatorio_atual['total_prejuizo']:,.2f}\n\n")
            
            for stat in self.relatorio_atual['por_status']:
                self.text_resultados.insert(tk.END, f"Status: {stat['status']}\n")
                self.text_resultados.insert(tk.END, f"  Quantidade: {stat['quantidade']}\n")
                self.text_resultados.insert(tk.END, f"  Total Prejuízo: R$ {stat['total_prejuizo']:,.2f}\n\n")
    
    def exportar_relatorio(self):
        """Exporta relatório para CSV"""
        if not self.relatorio_atual:
            messagebox.showwarning("Aviso", "Gere um relatório primeiro!")
            return
        
        try:
            tipo = self.combo_relatorio.get().lower().replace(" ", "_")
            caminho = self.relatorios.exportar_csv(self.relatorio_atual, tipo)
            messagebox.showinfo("Sucesso", f"Relatório exportado para: {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

def main():
    """Função principal para interface gráfica"""
    root = ThemedTk(theme="adapta")
    app = SeguroAppSQLite(root, None)
    root.mainloop()

if __name__ == "__main__":
    main()
