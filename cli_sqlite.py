"""
Interface CLI melhorada com SQLite
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from database import DatabaseManager
from auth_sqlite import AuthManager
from relatorios_sqlite import RelatorioManager
from exceptions import *
from logger_config import get_auditoria

class SistemaSegurosCLI:
    """Interface CLI do sistema de seguros com SQLite"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.auth = AuthManager()
        self.relatorios = RelatorioManager()
        self.auditoria = get_auditoria()
        self.running = True
    
    def exibir_titulo(self):
        """Exibe título do sistema"""
        print("=" * 60)
        print("    SISTEMA DE GERENCIAMENTO DE SEGUROS - SQLite")
        print("=" * 60)
        print()
    
    def exibir_menu_principal(self):
        """Exibe menu principal"""
        print("\n" + "=" * 40)
        print("           MENU PRINCIPAL")
        print("=" * 40)
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Seguros")
        print("3. Gerenciar Apólices")
        print("4. Gerenciar Sinistros")
        print("5. Relatórios")
        print("6. Gerenciar Usuários")
        print("7. Logs de Auditoria")
        print("0. Sair")
        print("=" * 40)
    
    def exibir_menu_clientes(self):
        """Exibe menu de clientes"""
        print("\n" + "=" * 30)
        print("      GERENCIAR CLIENTES")
        print("=" * 30)
        print("1. Cadastrar Cliente")
        print("2. Buscar Cliente por CPF")
        print("3. Listar Clientes")
        print("0. Voltar")
        print("=" * 30)
    
    def exibir_menu_seguros(self):
        """Exibe menu de seguros"""
        print("\n" + "=" * 30)
        print("      GERENCIAR SEGUROS")
        print("=" * 30)
        print("1. Criar Seguro Automóvel")
        print("2. Criar Seguro Residencial")
        print("3. Criar Seguro Vida")
        print("4. Buscar Seguro por ID")
        print("0. Voltar")
        print("=" * 30)
    
    def exibir_menu_apolices(self):
        """Exibe menu de apólices"""
        print("\n" + "=" * 30)
        print("      GERENCIAR APÓLICES")
        print("=" * 30)
        print("1. Emitir Apólice")
        print("2. Buscar Apólice por Número")
        print("3. Listar Apólices de Cliente")
        print("4. Cancelar Apólice")
        print("0. Voltar")
        print("=" * 30)
    
    def exibir_menu_sinistros(self):
        """Exibe menu de sinistros"""
        print("\n" + "=" * 30)
        print("      GERENCIAR SINISTROS")
        print("=" * 30)
        print("1. Registrar Sinistro")
        print("2. Buscar Sinistros por Apólice")
        print("3. Atualizar Status Sinistro")
        print("0. Voltar")
        print("=" * 30)
    
    def exibir_menu_relatorios(self):
        """Exibe menu de relatórios"""
        print("\n" + "=" * 30)
        print("         RELATÓRIOS")
        print("=" * 30)
        print("1. Receita Mensal")
        print("2. Top Clientes")
        print("3. Sinistros por Status")
        print("4. Apólices Ativas")
        print("5. Sinistros Recentes")
        print("0. Voltar")
        print("=" * 30)
    
    def exibir_menu_usuarios(self):
        """Exibe menu de usuários"""
        print("\n" + "=" * 30)
        print("      GERENCIAR USUÁRIOS")
        print("=" * 30)
        print("1. Criar Usuário")
        print("2. Alterar Senha")
        print("3. Listar Usuários")
        print("0. Voltar")
        print("=" * 30)
    
    def confirmar_operacao(self, mensagem: str) -> bool:
        """Solicita confirmação do usuário"""
        resposta = input(f"{mensagem} [s/N]: ").strip().lower()
        return resposta in ['s', 'sim', 'y', 'yes']
    
    def solicitar_dados_cliente(self) -> Optional[Dict]:
        """Solicita dados do cliente"""
        try:
            print("\n--- DADOS DO CLIENTE ---")
            nome = input("Nome completo: ").strip()
            if not nome:
                raise ValueError("Nome é obrigatório")
            
            cpf = input("CPF (apenas números): ").strip()
            if not cpf:
                raise ValueError("CPF é obrigatório")
            
            data_nasc = input("Data de nascimento (DD/MM/AAAA): ").strip()
            if not data_nasc:
                raise ValueError("Data de nascimento é obrigatória")
            
            endereco = input("Endereço completo: ").strip()
            if not endereco:
                raise ValueError("Endereço é obrigatório")
            
            telefone = input("Telefone: ").strip()
            if not telefone:
                raise ValueError("Telefone é obrigatório")
            
            email = input("Email: ").strip()
            if not email:
                raise ValueError("Email é obrigatório")
            
            return {
                'nome': nome,
                'cpf': cpf,
                'data_nascimento': data_nasc,
                'endereco': endereco,
                'telefone': telefone,
                'email': email
            }
            
        except ValueError as e:
            print(f"❌ Erro: {e}")
            return None
    
    def cadastrar_cliente(self):
        """Cadastra novo cliente"""
        try:
            dados = self.solicitar_dados_cliente()
            if not dados:
                return
            
            if not self.confirmar_operacao("Deseja cadastrar este cliente?"):
                print("Operação cancelada.")
                return
            
            cliente_id = self.db.criar_cliente(dados, self.auth.get_current_user_id())
            if cliente_id:
                print(f"✅ Cliente cadastrado com sucesso! ID: {cliente_id}")
                self.auth.log_operacao("CREATE", "cliente", str(cliente_id), f"Nome: {dados['nome']}")
            else:
                print("❌ Erro ao cadastrar cliente.")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def buscar_cliente_por_cpf(self):
        """Busca cliente por CPF"""
        try:
            cpf = input("Digite o CPF (apenas números): ").strip()
            if not cpf:
                print("❌ CPF é obrigatório.")
                return
            
            cliente = self.db.obter_cliente_por_cpf(cpf)
            if cliente:
                print("\n--- DADOS DO CLIENTE ---")
                print(f"Nome: {cliente['nome']}")
                print(f"CPF: {cliente['cpf']}")
                print(f"Data de Nascimento: {cliente['data_nascimento']}")
                print(f"Endereço: {cliente['endereco']}")
                print(f"Telefone: {cliente['telefone']}")
                print(f"Email: {cliente['email']}")
                print(f"Data de Cadastro: {cliente['data_cadastro']}")
                
                self.auth.log_operacao("SELECT", "cliente", cpf, "Busca por CPF")
            else:
                print("❌ Cliente não encontrado.")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        try:
            clientes = self.db.listar_clientes()
            if not clientes:
                print("❌ Nenhum cliente cadastrado.")
                return
            
            print(f"\n--- LISTA DE CLIENTES ({len(clientes)} encontrados) ---")
            for i, cliente in enumerate(clientes, 1):
                print(f"{i}. {cliente['nome']} - CPF: {cliente['cpf']}")
            
            self.auth.log_operacao("SELECT", "cliente", "ALL", "Listagem completa")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def gerenciar_clientes(self):
        """Gerencia operações de clientes"""
        while True:
            self.exibir_menu_clientes()
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.buscar_cliente_por_cpf()
            elif opcao == "3":
                self.listar_clientes()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida.")
            
            input("\nPressione Enter para continuar...")
    
    def gerenciar_relatorios(self):
        """Gerencia relatórios"""
        while True:
            self.exibir_menu_relatorios()
            opcao = input("Escolha uma opção: ").strip()
            
            try:
                if opcao == "1":  # Receita Mensal
                    mes = int(input("Digite o mês (1-12): "))
                    ano = int(input("Digite o ano: "))
                    dados = self.relatorios.gerar_receita_mensal(mes, ano)
                    self.exibir_relatorio_receita_mensal(dados)
                
                elif opcao == "2":  # Top Clientes
                    limite = int(input("Digite o número de clientes (padrão 5): ") or "5")
                    dados = self.relatorios.gerar_top_clientes(limite)
                    self.exibir_relatorio_top_clientes(dados)
                
                elif opcao == "3":  # Sinistros por Status
                    dados = self.relatorios.gerar_sinistros_por_status()
                    self.exibir_relatorio_sinistros_status(dados)
                
                elif opcao == "4":  # Apólices Ativas
                    dados = self.relatorios.gerar_relatorio_apolices_ativas()
                    self.exibir_relatorio_apolices_ativas(dados)
                
                elif opcao == "5":  # Sinistros Recentes
                    dias = int(input("Digite o número de dias (padrão 30): ") or "30")
                    dados = self.relatorios.gerar_relatorio_sinistros_recentes(dias)
                    self.exibir_relatorio_sinistros_recentes(dados)
                
                elif opcao == "0":
                    break
                else:
                    print("❌ Opção inválida.")
                
            except ValueError as e:
                print(f"❌ Erro: {e}")
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
            
            input("\nPressione Enter para continuar...")
    
    def exibir_relatorio_receita_mensal(self, dados: Dict):
        """Exibe relatório de receita mensal"""
        print(f"\n--- RECEITA MENSAL - {dados['mes']:02d}/{dados['ano']} ---")
        print(f"Receita Total: R$ {dados['receita_total']:,.2f}")
        print(f"Quantidade de Apólices: {dados['quantidade_apolices']}")
        print(f"Data de Geração: {dados['data_geracao']}")
        
        if dados['detalhes']:
            print("\n--- DETALHES ---")
            for item in dados['detalhes']:
                print(f"Apólice: {item['numero']} | Cliente: {item['cliente']} | Prêmio: R$ {item['premio']:,.2f}")
        
        if self.confirmar_operacao("Deseja exportar para CSV?"):
            try:
                caminho = self.relatorios.exportar_csv(dados, "receita_mensal")
                print(f"✅ Relatório exportado para: {caminho}")
            except Exception as e:
                print(f"❌ Erro ao exportar: {e}")
    
    def exibir_relatorio_top_clientes(self, dados: Dict):
        """Exibe relatório de top clientes"""
        print(f"\n--- TOP {dados['limite']} CLIENTES ---")
        print(f"Total de Clientes: {dados['total_clientes']}")
        print(f"Data de Geração: {dados['data_geracao']}")
        
        if dados['clientes']:
            print("\n--- RANKING ---")
            for i, cliente in enumerate(dados['clientes'], 1):
                print(f"{i}. {cliente['nome']} - CPF: {cliente['cpf']}")
                print(f"   Total Segurado: R$ {cliente['total_segurado']:,.2f}")
                print(f"   Número de Apólices: {cliente['num_apolices']}")
                print()
        
        if self.confirmar_operacao("Deseja exportar para CSV?"):
            try:
                caminho = self.relatorios.exportar_csv(dados, "top_clientes")
                print(f"✅ Relatório exportado para: {caminho}")
            except Exception as e:
                print(f"❌ Erro ao exportar: {e}")
    
    def exibir_relatorio_sinistros_status(self, dados: Dict):
        """Exibe relatório de sinistros por status"""
        print(f"\n--- SINISTROS POR STATUS ---")
        print(f"Total de Sinistros: {dados['total_sinistros']}")
        print(f"Total de Prejuízo: R$ {dados['total_prejuizo']:,.2f}")
        print(f"Data de Geração: {dados['data_geracao']}")
        
        if dados['por_status']:
            print("\n--- POR STATUS ---")
            for stat in dados['por_status']:
                print(f"Status: {stat['status']}")
                print(f"  Quantidade: {stat['quantidade']}")
                print(f"  Total Prejuízo: R$ {stat['total_prejuizo']:,.2f}")
                print()
        
        if self.confirmar_operacao("Deseja exportar para CSV?"):
            try:
                caminho = self.relatorios.exportar_csv(dados, "sinistros_status")
                print(f"✅ Relatório exportado para: {caminho}")
            except Exception as e:
                print(f"❌ Erro ao exportar: {e}")
    
    def exibir_relatorio_apolices_ativas(self, dados: Dict):
        """Exibe relatório de apólices ativas"""
        print(f"\n--- APÓLICES ATIVAS ---")
        print(f"Total de Apólices: {dados['total_apolices']}")
        print(f"Data de Geração: {dados['data_geracao']}")
        
        if dados['apolices']:
            print("\n--- LISTA DE APÓLICES ---")
            for apolice in dados['apolices'][:10]:  # Mostrar apenas as primeiras 10
                print(f"Apólice: {apolice['numero']} | Cliente: {apolice['cliente_nome']}")
                print(f"  Tipo: {apolice['seguro_tipo']} | Valor: R$ {apolice['valor_segurado']:,.2f}")
                print(f"  Prêmio: R$ {apolice['premio']:,.2f} | Vencimento: {apolice['data_vencimento']}")
                print()
            
            if len(dados['apolices']) > 10:
                print(f"... e mais {len(dados['apolices']) - 10} apólices")
        
        if self.confirmar_operacao("Deseja exportar para CSV?"):
            try:
                caminho = self.relatorios.exportar_csv(dados, "apolices_ativas")
                print(f"✅ Relatório exportado para: {caminho}")
            except Exception as e:
                print(f"❌ Erro ao exportar: {e}")
    
    def exibir_relatorio_sinistros_recentes(self, dados: Dict):
        """Exibe relatório de sinistros recentes"""
        print(f"\n--- SINISTROS RECENTES (Últimos {dados['periodo_dias']} dias) ---")
        print(f"Total de Sinistros: {dados['total_sinistros']}")
        print(f"Data de Geração: {dados['data_geracao']}")
        
        if dados['sinistros']:
            print("\n--- LISTA DE SINISTROS ---")
            for sinistro in dados['sinistros'][:10]:  # Mostrar apenas os primeiros 10
                print(f"ID: {sinistro['id']} | Data: {sinistro['data_ocorrencia']}")
                print(f"  Descrição: {sinistro['descricao']}")
                print(f"  Valor Prejuízo: R$ {sinistro['valor_prejuizo']:,.2f}")
                print(f"  Status: {sinistro['status']} | Apólice: {sinistro['apolice_numero']}")
                print(f"  Cliente: {sinistro['cliente_nome']}")
                print()
            
            if len(dados['sinistros']) > 10:
                print(f"... e mais {len(dados['sinistros']) - 10} sinistros")
        
        if self.confirmar_operacao("Deseja exportar para CSV?"):
            try:
                caminho = self.relatorios.exportar_csv(dados, "sinistros_recentes")
                print(f"✅ Relatório exportado para: {caminho}")
            except Exception as e:
                print(f"❌ Erro ao exportar: {e}")
    
    def fazer_login(self) -> bool:
        """Realiza login do usuário"""
        print("\n--- LOGIN ---")
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()
        
        if self.auth.login(usuario, senha):
            print(f"✅ Login realizado com sucesso! Bem-vindo, {usuario}!")
            return True
        else:
            print("❌ Usuário ou senha inválidos.")
            return False
    
    def executar(self):
        """Executa o sistema"""
        self.exibir_titulo()
        
        # Fazer login
        while not self.auth.is_authenticated():
            if not self.fazer_login():
                if not self.confirmar_operacao("Deseja tentar novamente?"):
                    print("Sistema encerrado.")
                    return
        
        # Menu principal
        while self.running:
            try:
                self.exibir_menu_principal()
                opcao = input("Escolha uma opção: ").strip()
                
                if opcao == "1":
                    self.gerenciar_clientes()
                elif opcao == "2":
                    print("⚠️ Funcionalidade em desenvolvimento...")
                elif opcao == "3":
                    print("⚠️ Funcionalidade em desenvolvimento...")
                elif opcao == "4":
                    print("⚠️ Funcionalidade em desenvolvimento...")
                elif opcao == "5":
                    self.gerenciar_relatorios()
                elif opcao == "6":
                    print("⚠️ Funcionalidade em desenvolvimento...")
                elif opcao == "7":
                    print("⚠️ Funcionalidade em desenvolvimento...")
                elif opcao == "0":
                    if self.confirmar_operacao("Deseja realmente sair?"):
                        self.auth.logout()
                        print("👋 Até logo!")
                        break
                else:
                    print("❌ Opção inválida.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Sistema encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                self.auditoria.log_error(f"Erro inesperado na CLI: {e}")

def main():
    """Função principal"""
    try:
        sistema = SistemaSegurosCLI()
        sistema.executar()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
