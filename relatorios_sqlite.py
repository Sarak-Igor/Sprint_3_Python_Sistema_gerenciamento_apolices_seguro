"""
Módulo de relatórios com queries SQL complexas
"""

import csv
import os
from datetime import datetime, date
from typing import List, Dict, Optional
from database import DatabaseManager
from exceptions import RelatorioError, ExportacaoError
from logger_config import get_auditoria

class RelatorioManager:
    """Gerenciador de relatórios do sistema"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.auditoria = get_auditoria()
        self.export_dir = "export"
        
        # Criar diretório de exportação se não existir
        os.makedirs(self.export_dir, exist_ok=True)
    
    def gerar_receita_mensal(self, mes: int, ano: int) -> Dict:
        """
        Gera relatório de receita mensal
        
        Args:
            mes: Mês (1-12)
            ano: Ano
            
        Returns:
            Dict com dados da receita mensal
        """
        try:
            receita = self.db.obter_receita_mensal(mes, ano)
            
            # Buscar detalhes das apólices do mês
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT a.numero, c.nome as cliente_nome, a.premio, a.data_emissao
                    FROM apolices a
                    JOIN clientes c ON a.cliente_id = c.id
                    WHERE a.status = 'ativa' 
                    AND strftime('%m', a.data_emissao) = ? 
                    AND strftime('%Y', a.data_emissao) = ?
                    ORDER BY a.data_emissao DESC
                """, (f"{mes:02d}", str(ano)))
                
                detalhes = []
                for row in cursor.fetchall():
                    detalhes.append({
                        'numero': row[0],
                        'cliente': row[1],
                        'premio': row[2],
                        'data_emissao': row[3]
                    })
            
            resultado = {
                'mes': mes,
                'ano': ano,
                'receita_total': receita,
                'quantidade_apolices': len(detalhes),
                'detalhes': detalhes,
                'data_geracao': datetime.now().isoformat()
            }
            
            self.auditoria.log_relatorio("receita_mensal", "Sistema", f"mes={mes}, ano={ano}")
            return resultado
            
        except Exception as e:
            raise RelatorioError("receita_mensal", str(e))
    
    def gerar_top_clientes(self, limite: int = 5) -> Dict:
        """
        Gera relatório dos top clientes por valor segurado
        
        Args:
            limite: Número máximo de clientes a retornar
            
        Returns:
            Dict com dados dos top clientes
        """
        try:
            clientes = self.db.obter_top_clientes(limite)
            
            resultado = {
                'limite': limite,
                'total_clientes': len(clientes),
                'clientes': clientes,
                'data_geracao': datetime.now().isoformat()
            }
            
            self.auditoria.log_relatorio("top_clientes", "Sistema", f"limite={limite}")
            return resultado
            
        except Exception as e:
            raise RelatorioError("top_clientes", str(e))
    
    def gerar_sinistros_por_status(self) -> Dict:
        """
        Gera relatório de sinistros por status
        
        Returns:
            Dict com estatísticas de sinistros
        """
        try:
            stats = self.db.obter_sinistros_por_status()
            
            # Calcular totais
            total_sinistros = sum(s['quantidade'] for s in stats)
            total_prejuizo = sum(s['total_prejuizo'] for s in stats)
            
            resultado = {
                'total_sinistros': total_sinistros,
                'total_prejuizo': total_prejuizo,
                'por_status': stats,
                'data_geracao': datetime.now().isoformat()
            }
            
            self.auditoria.log_relatorio("sinistros_por_status", "Sistema")
            return resultado
            
        except Exception as e:
            raise RelatorioError("sinistros_por_status", str(e))
    
    def gerar_relatorio_apolices_ativas(self) -> Dict:
        """
        Gera relatório de apólices ativas
        
        Returns:
            Dict com dados das apólices ativas
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT a.numero, c.nome as cliente_nome, c.cpf, s.tipo as seguro_tipo,
                           a.valor_segurado, a.premio, a.data_emissao, a.data_vencimento
                    FROM apolices a
                    JOIN clientes c ON a.cliente_id = c.id
                    JOIN seguros s ON a.seguro_id = s.id
                    WHERE a.status = 'ativa'
                    ORDER BY a.data_emissao DESC
                """)
                
                apolices = []
                for row in cursor.fetchall():
                    apolices.append({
                        'numero': row[0],
                        'cliente_nome': row[1],
                        'cliente_cpf': row[2],
                        'seguro_tipo': row[3],
                        'valor_segurado': row[4],
                        'premio': row[5],
                        'data_emissao': row[6],
                        'data_vencimento': row[7]
                    })
            
            resultado = {
                'total_apolices': len(apolices),
                'apolices': apolices,
                'data_geracao': datetime.now().isoformat()
            }
            
            self.auditoria.log_relatorio("apolices_ativas", "Sistema")
            return resultado
            
        except Exception as e:
            raise RelatorioError("apolices_ativas", str(e))
    
    def gerar_relatorio_sinistros_recentes(self, dias: int = 30) -> Dict:
        """
        Gera relatório de sinistros recentes
        
        Args:
            dias: Número de dias para buscar sinistros
            
        Returns:
            Dict com dados dos sinistros recentes
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT s.id, s.data_ocorrencia, s.descricao, s.valor_prejuizo, s.status,
                           a.numero as apolice_numero, c.nome as cliente_nome
                    FROM sinistros s
                    JOIN apolices a ON s.apolice_id = a.id
                    JOIN clientes c ON a.cliente_id = c.id
                    WHERE s.data_ocorrencia >= date('now', '-{} days')
                    ORDER BY s.data_ocorrencia DESC
                """.format(dias))
                
                sinistros = []
                for row in cursor.fetchall():
                    sinistros.append({
                        'id': row[0],
                        'data_ocorrencia': row[1],
                        'descricao': row[2],
                        'valor_prejuizo': row[3],
                        'status': row[4],
                        'apolice_numero': row[5],
                        'cliente_nome': row[6]
                    })
            
            resultado = {
                'periodo_dias': dias,
                'total_sinistros': len(sinistros),
                'sinistros': sinistros,
                'data_geracao': datetime.now().isoformat()
            }
            
            self.auditoria.log_relatorio("sinistros_recentes", "Sistema", f"dias={dias}")
            return resultado
            
        except Exception as e:
            raise RelatorioError("sinistros_recentes", str(e))
    
    def exportar_csv(self, dados: Dict, nome_arquivo: str) -> str:
        """
        Exporta dados para arquivo CSV
        
        Args:
            dados: Dados a serem exportados
            nome_arquivo: Nome do arquivo (sem extensão)
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_completo = f"{nome_arquivo}_{timestamp}.csv"
            caminho = os.path.join(self.export_dir, nome_completo)
            
            # Determinar estrutura baseada no tipo de relatório
            if 'detalhes' in dados:  # Receita mensal
                with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Número', 'Cliente', 'Prêmio', 'Data Emissão'])
                    for item in dados['detalhes']:
                        writer.writerow([item['numero'], item['cliente'], item['premio'], item['data_emissao']])
            
            elif 'clientes' in dados:  # Top clientes
                with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Nome', 'CPF', 'Total Segurado', 'Número de Apólices'])
                    for item in dados['clientes']:
                        writer.writerow([item['nome'], item['cpf'], item['total_segurado'], item['num_apolices']])
            
            elif 'por_status' in dados:  # Sinistros por status
                with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Status', 'Quantidade', 'Total Prejuízo'])
                    for item in dados['por_status']:
                        writer.writerow([item['status'], item['quantidade'], item['total_prejuizo']])
            
            elif 'apolices' in dados:  # Apólices ativas
                with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Número', 'Cliente', 'CPF', 'Tipo Seguro', 'Valor Segurado', 'Prêmio', 'Data Emissão', 'Data Vencimento'])
                    for item in dados['apolices']:
                        writer.writerow([item['numero'], item['cliente_nome'], item['cliente_cpf'], 
                                       item['seguro_tipo'], item['valor_segurado'], item['premio'], 
                                       item['data_emissao'], item['data_vencimento']])
            
            elif 'sinistros' in dados:  # Sinistros recentes
                with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Data Ocorrência', 'Descrição', 'Valor Prejuízo', 'Status', 'Apólice', 'Cliente'])
                    for item in dados['sinistros']:
                        writer.writerow([item['id'], item['data_ocorrencia'], item['descricao'], 
                                       item['valor_prejuizo'], item['status'], item['apolice_numero'], item['cliente_nome']])
            
            self.auditoria.log_info(f"Relatório exportado para CSV: {caminho}")
            return caminho
            
        except Exception as e:
            raise ExportacaoError("CSV", str(e))
    
    def listar_relatorios_disponiveis(self) -> List[Dict]:
        """
        Lista relatórios disponíveis no sistema
        
        Returns:
            Lista de relatórios disponíveis
        """
        return [
            {
                'id': 'receita_mensal',
                'nome': 'Receita Mensal',
                'descricao': 'Receita gerada em um mês específico',
                'parametros': ['mes', 'ano']
            },
            {
                'id': 'top_clientes',
                'nome': 'Top Clientes',
                'descricao': 'Clientes com maior valor segurado',
                'parametros': ['limite']
            },
            {
                'id': 'sinistros_por_status',
                'nome': 'Sinistros por Status',
                'descricao': 'Estatísticas de sinistros agrupados por status',
                'parametros': []
            },
            {
                'id': 'apolices_ativas',
                'nome': 'Apólices Ativas',
                'descricao': 'Lista de todas as apólices ativas',
                'parametros': []
            },
            {
                'id': 'sinistros_recentes',
                'nome': 'Sinistros Recentes',
                'descricao': 'Sinistros dos últimos dias',
                'parametros': ['dias']
            }
        ]
