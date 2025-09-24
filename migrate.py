"""
Script de Migração One-Shot
Converte dados dos arquivos JSON para SQLite
"""

import json
import os
import sys
from datetime import datetime
from database import DatabaseManager
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migrate.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Migrator:
    def __init__(self):
        self.db = DatabaseManager()
        self.migration_stats = {
            'clientes': 0,
            'seguros': 0,
            'apolices': 0,
            'sinistros': 0,
            'usuarios': 0
        }
    
    def migrar_usuarios(self):
        """Migra usuários do JSON para SQLite"""
        logger.info("Iniciando migração de usuários...")
        
        # Criar usuário admin padrão se não existir
        admin_created = self.db.criar_usuario('admin', 'password', 'admin')
        if admin_created:
            self.migration_stats['usuarios'] += 1
            logger.info("Usuário admin criado")
        
        # Migrar usuários do JSON se existir
        if os.path.exists('usuarios.json'):
            try:
                with open('usuarios.json', 'r', encoding='utf-8') as f:
                    usuarios_data = json.load(f)
                
                for usuario, (senha, tipo) in usuarios_data.items():
                    if usuario != 'admin':  # Admin já foi criado
                        perfil = 'admin' if tipo == 'administrador' else 'comum'
                        if self.db.criar_usuario(usuario, senha, perfil):
                            self.migration_stats['usuarios'] += 1
                            logger.info(f"Usuário {usuario} migrado")
            except Exception as e:
                logger.error(f"Erro ao migrar usuários: {e}")
        else:
            logger.info("Arquivo usuarios.json não encontrado, usando apenas usuário admin padrão")
    
    def migrar_clientes(self):
        """Migra clientes do JSON para SQLite"""
        logger.info("Iniciando migração de clientes...")
        
        if not os.path.exists('clientes.json'):
            logger.warning("Arquivo clientes.json não encontrado")
            return
        
        try:
            with open('clientes.json', 'r', encoding='utf-8') as f:
                clientes_data = json.load(f)
            
            for cliente_data in clientes_data:
                # Converter dados do formato JSON para o formato esperado pelo DAL
                cliente_dict = {
                    'nome': cliente_data.get('nome', ''),
                    'cpf': cliente_data.get('cpf', ''),
                    'data_nascimento': cliente_data.get('data_nascimento', ''),
                    'endereco': cliente_data.get('endereco', ''),
                    'telefone': cliente_data.get('telefone', ''),
                    'email': cliente_data.get('email', '')
                }
                
                cliente_id = self.db.criar_cliente(cliente_dict, 1)  # user_id = 1 (admin)
                if cliente_id:
                    self.migration_stats['clientes'] += 1
                    logger.info(f"Cliente {cliente_dict['nome']} migrado com ID {cliente_id}")
                else:
                    logger.warning(f"Falha ao migrar cliente {cliente_dict['nome']}")
        
        except Exception as e:
            logger.error(f"Erro ao migrar clientes: {e}")
    
    def migrar_seguros(self):
        """Migra seguros do JSON para SQLite"""
        logger.info("Iniciando migração de seguros...")
        
        if not os.path.exists('seguros.json'):
            logger.warning("Arquivo seguros.json não encontrado")
            return
        
        try:
            with open('seguros.json', 'r', encoding='utf-8') as f:
                seguros_data = json.load(f)
            
            for seguro_data in seguros_data:
                # Preparar dados do seguro
                seguro_dict = {
                    'id': seguro_data.get('id', ''),
                    'tipo': seguro_data.get('tipo', ''),
                    'valor_cobertura': seguro_data.get('valor_cobertura', 0),
                    'data_inicio': seguro_data.get('data_inicio', ''),
                    'data_fim': seguro_data.get('data_fim', ''),
                    'status': seguro_data.get('status', 'ativo')
                }
                
                # Adicionar campos específicos por tipo
                if seguro_dict['tipo'] == 'Automóvel':
                    seguro_dict.update({
                        'marca': seguro_data.get('marca', ''),
                        'modelo': seguro_data.get('modelo', ''),
                        'ano': seguro_data.get('ano', 0),
                        'placa': seguro_data.get('placa', ''),
                        'estado_conservacao': seguro_data.get('estado_conservacao', ''),
                        'uso_veiculo': seguro_data.get('uso_veiculo', ''),
                        'num_condutores': seguro_data.get('num_condutores', 0)
                    })
                elif seguro_dict['tipo'] == 'Residencial':
                    seguro_dict.update({
                        'endereco_imovel': seguro_data.get('endereco_imovel', ''),
                        'area': seguro_data.get('area', 0),
                        'valor_venal': seguro_data.get('valor_venal', 0),
                        'tipo_construcao': seguro_data.get('tipo_construcao', '')
                    })
                elif seguro_dict['tipo'] == 'Vida':
                    seguro_dict.update({
                        'beneficiarios': seguro_data.get('beneficiarios', []),
                        'tipos_cobertura': seguro_data.get('tipos_cobertura', [])
                    })
                
                if self.db.criar_seguro(seguro_dict, 1):  # user_id = 1 (admin)
                    self.migration_stats['seguros'] += 1
                    logger.info(f"Seguro {seguro_dict['id']} migrado")
                else:
                    logger.warning(f"Falha ao migrar seguro {seguro_dict['id']}")
        
        except Exception as e:
            logger.error(f"Erro ao migrar seguros: {e}")
    
    def migrar_apolices(self):
        """Migra apólices do JSON para SQLite"""
        logger.info("Iniciando migração de apólices...")
        
        if not os.path.exists('apolices.json'):
            logger.warning("Arquivo apolices.json não encontrado")
            return
        
        try:
            with open('apolices.json', 'r', encoding='utf-8') as f:
                apolices_data = json.load(f)
            
            for apolice_data in apolices_data:
                # Buscar cliente_id pelo CPF
                cliente = self.db.obter_cliente_por_cpf(apolice_data.get('cliente_cpf', ''))
                if not cliente:
                    logger.warning(f"Cliente com CPF {apolice_data.get('cliente_cpf')} não encontrado para apólice {apolice_data.get('numero')}")
                    continue
                
                # Buscar seguro_id
                seguro = self.db.obter_seguro_por_id(apolice_data.get('seguro_id', ''))
                if not seguro:
                    logger.warning(f"Seguro com ID {apolice_data.get('seguro_id')} não encontrado para apólice {apolice_data.get('numero')}")
                    continue
                
                apolice_dict = {
                    'numero': apolice_data.get('numero', ''),
                    'cliente_id': cliente['id'],
                    'seguro_id': apolice_data.get('seguro_id', ''),
                    'status': apolice_data.get('status', 'ativa'),
                    'premio': seguro.get('valor_cobertura', 0) * 0.1,  # 10% do valor da cobertura
                    'valor_segurado': seguro.get('valor_cobertura', 0),
                    'data_vencimento': seguro.get('data_fim', '')
                }
                
                if self.db.criar_apolice(apolice_dict, 1):  # user_id = 1 (admin)
                    self.migration_stats['apolices'] += 1
                    logger.info(f"Apólice {apolice_dict['numero']} migrada")
                else:
                    logger.warning(f"Falha ao migrar apólice {apolice_dict['numero']}")
        
        except Exception as e:
            logger.error(f"Erro ao migrar apólices: {e}")
    
    def migrar_sinistros(self):
        """Migra sinistros do JSON para SQLite"""
        logger.info("Iniciando migração de sinistros...")
        
        if not os.path.exists('sinistros.json'):
            logger.warning("Arquivo sinistros.json não encontrado")
            return
        
        try:
            with open('sinistros.json', 'r', encoding='utf-8') as f:
                sinistros_data = json.load(f)
            
            for sinistro_data in sinistros_data:
                # Para migrar sinistros, precisamos encontrar a apólice correspondente
                # Como não temos referência direta, vamos buscar por padrões ou usar dados disponíveis
                sinistro_dict = {
                    'id': sinistro_data.get('id', ''),
                    'apolice_id': 1,  # Assumir primeira apólice por enquanto
                    'data_ocorrencia': sinistro_data.get('data_ocorrencia', ''),
                    'descricao': sinistro_data.get('descricao', ''),
                    'valor_prejuizo': sinistro_data.get('valor_prejuizo', 0),
                    'status': sinistro_data.get('status', 'aberto'),
                    'valor_indenizacao': sinistro_data.get('valor_indenizacao'),
                    'observacoes': sinistro_data.get('observacoes', '')
                }
                
                if self.db.criar_sinistro(sinistro_dict, 1):  # user_id = 1 (admin)
                    self.migration_stats['sinistros'] += 1
                    logger.info(f"Sinistro {sinistro_dict['id']} migrado")
                else:
                    logger.warning(f"Falha ao migrar sinistro {sinistro_dict['id']}")
        
        except Exception as e:
            logger.error(f"Erro ao migrar sinistros: {e}")
    
    def executar_migracao(self):
        """Executa a migração completa"""
        logger.info("=== INICIANDO MIGRAÇÃO DE DADOS ===")
        logger.info(f"Timestamp: {datetime.now()}")
        
        try:
            # Executar migrações em ordem
            self.migrar_usuarios()
            self.migrar_clientes()
            self.migrar_seguros()
            self.migrar_apolices()
            self.migrar_sinistros()
            
            # Relatório final
            logger.info("=== MIGRAÇÃO CONCLUÍDA ===")
            logger.info("Estatísticas da migração:")
            for entidade, quantidade in self.migration_stats.items():
                logger.info(f"  {entidade.capitalize()}: {quantidade} registros")
            
            total = sum(self.migration_stats.values())
            logger.info(f"Total de registros migrados: {total}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a migração: {e}")
            return False

def main():
    """Função principal do script de migração"""
    print("=== SCRIPT DE MIGRAÇÃO JSON -> SQLite ===")
    print("Este script irá migrar todos os dados dos arquivos JSON para o banco SQLite.")
    
    resposta = input("Deseja continuar? (s/N): ").strip().lower()
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Migração cancelada.")
        return
    
    migrator = Migrator()
    sucesso = migrator.executar_migracao()
    
    if sucesso:
        print("\n✅ Migração concluída com sucesso!")
        print("Os dados foram migrados para o arquivo 'seguradora.db'")
        print("Logs detalhados foram salvos em 'migrate.log'")
    else:
        print("\n❌ Migração falhou!")
        print("Verifique os logs em 'migrate.log' para mais detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()
