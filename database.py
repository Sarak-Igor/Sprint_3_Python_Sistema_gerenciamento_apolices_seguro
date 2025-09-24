"""
Camada de Acesso a Dados (DAL - Data Access Layer)
Responsável por todas as operações de banco de dados
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

# Configurar logger
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "seguradora.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados criando as tabelas se não existirem"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                with open('schema.sql', 'r', encoding='utf-8') as f:
                    schema = f.read()
                conn.executescript(schema)
                conn.commit()
            logger.info("Banco de dados inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def hash_password(self, password: str) -> str:
        """Gera hash SHA-256 da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ========== OPERAÇÕES DE USUÁRIOS ==========
    
    def criar_usuario(self, nome_usuario: str, senha: str, perfil: str) -> bool:
        """Cria um novo usuário no banco"""
        try:
            senha_hash = self.hash_password(senha)
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO usuarios (nome_usuario, senha_hash, perfil)
                    VALUES (?, ?, ?)
                """, (nome_usuario, senha_hash, perfil))
                conn.commit()
            logger.info(f"Usuário {nome_usuario} criado com sucesso")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Usuário {nome_usuario} já existe")
            return False
        except Exception as e:
            logger.error(f"Erro ao criar usuário {nome_usuario}: {e}")
            return False
    
    def validar_login(self, nome_usuario: str, senha: str) -> Optional[Dict]:
        """Valida login e retorna dados do usuário se válido"""
        try:
            senha_hash = self.hash_password(senha)
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, nome_usuario, perfil FROM usuarios 
                    WHERE nome_usuario = ? AND senha_hash = ? AND ativo = 1
                """, (nome_usuario, senha_hash))
                user = cursor.fetchone()
                if user:
                    logger.info(f"Login bem-sucedido para usuário {nome_usuario}")
                    return {
                        'id': user[0],
                        'nome_usuario': user[1],
                        'perfil': user[2]
                    }
                else:
                    logger.warning(f"Tentativa de login falhada para usuário {nome_usuario}")
                    return None
        except Exception as e:
            logger.error(f"Erro ao validar login: {e}")
            return None
    
    def obter_usuario_por_id(self, user_id: int) -> Optional[Dict]:
        """Obtém dados de um usuário por ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, nome_usuario, perfil FROM usuarios 
                    WHERE id = ? AND ativo = 1
                """, (user_id,))
                user = cursor.fetchone()
                if user:
                    return {
                        'id': user[0],
                        'nome_usuario': user[1],
                        'perfil': user[2]
                    }
                return None
        except Exception as e:
            logger.error(f"Erro ao obter usuário {user_id}: {e}")
            return None
    
    # ========== OPERAÇÕES DE CLIENTES ==========
    
    def criar_cliente(self, cliente_data: Dict, user_id: int) -> Optional[int]:
        """Cria um novo cliente"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO clientes (nome, cpf, data_nascimento, endereco, telefone, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    cliente_data['nome'],
                    cliente_data['cpf'],
                    cliente_data['data_nascimento'],
                    cliente_data['endereco'],
                    cliente_data['telefone'],
                    cliente_data['email']
                ))
                cliente_id = cursor.lastrowid
                conn.commit()
                
                # Log de auditoria
                self.log_auditoria(user_id, 'CREATE', 'cliente', str(cliente_id), None, json.dumps(cliente_data))
                
                logger.info(f"Cliente {cliente_data['nome']} criado com ID {cliente_id}")
                return cliente_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Erro de integridade ao criar cliente: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao criar cliente: {e}")
            return None
    
    def obter_cliente_por_cpf(self, cpf: str) -> Optional[Dict]:
        """Busca cliente por CPF"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, data_cadastro
                    FROM clientes WHERE cpf = ? AND ativo = 1
                """, (cpf,))
                cliente = cursor.fetchone()
                if cliente:
                    return {
                        'id': cliente[0],
                        'nome': cliente[1],
                        'cpf': cliente[2],
                        'data_nascimento': cliente[3],
                        'endereco': cliente[4],
                        'telefone': cliente[5],
                        'email': cliente[6],
                        'data_cadastro': cliente[7]
                    }
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por CPF {cpf}: {e}")
            return None
    
    def listar_clientes(self) -> List[Dict]:
        """Lista todos os clientes ativos"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, data_cadastro
                    FROM clientes WHERE ativo = 1 ORDER BY nome
                """)
                clientes = []
                for row in cursor.fetchall():
                    clientes.append({
                        'id': row[0],
                        'nome': row[1],
                        'cpf': row[2],
                        'data_nascimento': row[3],
                        'endereco': row[4],
                        'telefone': row[5],
                        'email': row[6],
                        'data_cadastro': row[7]
                    })
                return clientes
        except Exception as e:
            logger.error(f"Erro ao listar clientes: {e}")
            return []
    
    # ========== OPERAÇÕES DE SEGUROS ==========
    
    def criar_seguro(self, seguro_data: Dict, user_id: int) -> Optional[str]:
        """Cria um novo seguro"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO seguros (id, tipo, valor_cobertura, data_inicio, data_fim, status,
                                       marca, modelo, ano, placa, estado_conservacao, uso_veiculo, num_condutores,
                                       endereco_imovel, area, valor_venal, tipo_construcao,
                                       beneficiarios, tipos_cobertura)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    seguro_data['id'],
                    seguro_data['tipo'],
                    seguro_data['valor_cobertura'],
                    seguro_data['data_inicio'],
                    seguro_data['data_fim'],
                    seguro_data.get('status', 'ativo'),
                    seguro_data.get('marca'),
                    seguro_data.get('modelo'),
                    seguro_data.get('ano'),
                    seguro_data.get('placa'),
                    seguro_data.get('estado_conservacao'),
                    seguro_data.get('uso_veiculo'),
                    seguro_data.get('num_condutores'),
                    seguro_data.get('endereco_imovel'),
                    seguro_data.get('area'),
                    seguro_data.get('valor_venal'),
                    seguro_data.get('tipo_construcao'),
                    json.dumps(seguro_data.get('beneficiarios', [])),
                    json.dumps(seguro_data.get('tipos_cobertura', []))
                ))
                conn.commit()
                
                # Log de auditoria
                self.log_auditoria(user_id, 'CREATE', 'seguro', seguro_data['id'], None, json.dumps(seguro_data))
                
                logger.info(f"Seguro {seguro_data['id']} criado com sucesso")
                return seguro_data['id']
        except Exception as e:
            logger.error(f"Erro ao criar seguro: {e}")
            return None
    
    def obter_seguro_por_id(self, seguro_id: str) -> Optional[Dict]:
        """Busca seguro por ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM seguros WHERE id = ?
                """, (seguro_id,))
                seguro = cursor.fetchone()
                if seguro:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, seguro))
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar seguro {seguro_id}: {e}")
            return None
    
    # ========== OPERAÇÕES DE APÓLICES ==========
    
    def criar_apolice(self, apolice_data: Dict, user_id: int) -> Optional[int]:
        """Cria uma nova apólice"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO apolices (numero, cliente_id, seguro_id, status, premio, valor_segurado, data_vencimento)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    apolice_data['numero'],
                    apolice_data['cliente_id'],
                    apolice_data['seguro_id'],
                    apolice_data.get('status', 'ativa'),
                    apolice_data['premio'],
                    apolice_data['valor_segurado'],
                    apolice_data.get('data_vencimento')
                ))
                apolice_id = cursor.lastrowid
                conn.commit()
                
                # Log de auditoria
                self.log_auditoria(user_id, 'CREATE', 'apolice', str(apolice_id), None, json.dumps(apolice_data))
                
                logger.info(f"Apólice {apolice_data['numero']} criada com ID {apolice_id}")
                return apolice_id
        except Exception as e:
            logger.error(f"Erro ao criar apólice: {e}")
            return None
    
    def obter_apolice_por_numero(self, numero: str) -> Optional[Dict]:
        """Busca apólice por número"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT a.*, c.nome as cliente_nome, c.cpf as cliente_cpf
                    FROM apolices a
                    JOIN clientes c ON a.cliente_id = c.id
                    WHERE a.numero = ?
                """, (numero,))
                apolice = cursor.fetchone()
                if apolice:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, apolice))
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar apólice {numero}: {e}")
            return None
    
    def obter_apolices_por_cliente(self, cliente_id: int) -> List[Dict]:
        """Busca apólices de um cliente"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT a.*, s.tipo as seguro_tipo, s.valor_cobertura
                    FROM apolices a
                    JOIN seguros s ON a.seguro_id = s.id
                    WHERE a.cliente_id = ?
                """, (cliente_id,))
                apolices = []
                for row in cursor.fetchall():
                    columns = [description[0] for description in cursor.description]
                    apolices.append(dict(zip(columns, row)))
                return apolices
        except Exception as e:
            logger.error(f"Erro ao buscar apólices do cliente {cliente_id}: {e}")
            return []
    
    # ========== OPERAÇÕES DE SINISTROS ==========
    
    def criar_sinistro(self, sinistro_data: Dict, user_id: int) -> Optional[str]:
        """Cria um novo sinistro"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO sinistros (id, apolice_id, data_ocorrencia, descricao, valor_prejuizo, status, valor_indenizacao, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sinistro_data['id'],
                    sinistro_data['apolice_id'],
                    sinistro_data['data_ocorrencia'],
                    sinistro_data['descricao'],
                    sinistro_data['valor_prejuizo'],
                    sinistro_data.get('status', 'aberto'),
                    sinistro_data.get('valor_indenizacao'),
                    sinistro_data.get('observacoes')
                ))
                conn.commit()
                
                # Log de auditoria
                self.log_auditoria(user_id, 'CREATE', 'sinistro', sinistro_data['id'], None, json.dumps(sinistro_data))
                
                logger.info(f"Sinistro {sinistro_data['id']} criado com sucesso")
                return sinistro_data['id']
        except Exception as e:
            logger.error(f"Erro ao criar sinistro: {e}")
            return None
    
    def obter_sinistros_por_apolice(self, apolice_id: int) -> List[Dict]:
        """Busca sinistros de uma apólice"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM sinistros WHERE apolice_id = ? ORDER BY data_ocorrencia DESC
                """, (apolice_id,))
                sinistros = []
                for row in cursor.fetchall():
                    columns = [description[0] for description in cursor.description]
                    sinistros.append(dict(zip(columns, row)))
                return sinistros
        except Exception as e:
            logger.error(f"Erro ao buscar sinistros da apólice {apolice_id}: {e}")
            return []
    
    # ========== OPERAÇÕES DE RELATÓRIOS ==========
    
    def obter_receita_mensal(self, mes: int, ano: int) -> float:
        """Calcula receita mensal das apólices ativas"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT SUM(premio) FROM apolices 
                    WHERE status = 'ativa' 
                    AND strftime('%m', data_emissao) = ? 
                    AND strftime('%Y', data_emissao) = ?
                """, (f"{mes:02d}", str(ano)))
                result = cursor.fetchone()
                return result[0] if result[0] else 0.0
        except Exception as e:
            logger.error(f"Erro ao calcular receita mensal: {e}")
            return 0.0
    
    def obter_top_clientes(self, limite: int = 5) -> List[Dict]:
        """Obtém top clientes por valor segurado"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT c.nome, c.cpf, SUM(a.valor_segurado) as total_segurado, COUNT(a.id) as num_apolices
                    FROM clientes c
                    JOIN apolices a ON c.id = a.cliente_id
                    WHERE a.status = 'ativa'
                    GROUP BY c.id, c.nome, c.cpf
                    ORDER BY total_segurado DESC
                    LIMIT ?
                """, (limite,))
                clientes = []
                for row in cursor.fetchall():
                    clientes.append({
                        'nome': row[0],
                        'cpf': row[1],
                        'total_segurado': row[2],
                        'num_apolices': row[3]
                    })
                return clientes
        except Exception as e:
            logger.error(f"Erro ao obter top clientes: {e}")
            return []
    
    def obter_sinistros_por_status(self) -> List[Dict]:
        """Obtém estatísticas de sinistros por status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT status, COUNT(*) as quantidade, SUM(valor_prejuizo) as total_prejuizo
                    FROM sinistros
                    GROUP BY status
                    ORDER BY quantidade DESC
                """)
                stats = []
                for row in cursor.fetchall():
                    stats.append({
                        'status': row[0],
                        'quantidade': row[1],
                        'total_prejuizo': row[2] if row[2] else 0.0
                    })
                return stats
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de sinistros: {e}")
            return []
    
    # ========== OPERAÇÕES DE AUDITORIA ==========
    
    def log_auditoria(self, user_id: int, acao: str, entidade: str, entidade_id: str, 
                     dados_anteriores: str, dados_novos: str):
        """Registra log de auditoria"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO auditoria (usuario_id, acao, entidade, entidade_id, dados_anteriores, dados_novos)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, acao, entidade, entidade_id, dados_anteriores, dados_novos))
                conn.commit()
        except Exception as e:
            logger.error(f"Erro ao registrar auditoria: {e}")
    
    def obter_logs_auditoria(self, limite: int = 100) -> List[Dict]:
        """Obtém logs de auditoria"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT a.*, u.nome_usuario
                    FROM auditoria a
                    LEFT JOIN usuarios u ON a.usuario_id = u.id
                    ORDER BY a.timestamp DESC
                    LIMIT ?
                """, (limite,))
                logs = []
                for row in cursor.fetchall():
                    columns = [description[0] for description in cursor.description]
                    logs.append(dict(zip(columns, row)))
                return logs
        except Exception as e:
            logger.error(f"Erro ao obter logs de auditoria: {e}")
            return []
