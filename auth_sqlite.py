"""
Sistema de autenticação integrado com SQLite
"""

import hashlib
from typing import Optional, Dict
from database import DatabaseManager
from exceptions import (
    UsuarioNaoEncontradoError, 
    SenhaInvalidaError, 
    UsuarioNaoAutenticadoError,
    PermissaoNegadaError
)
from logger_config import get_auditoria

class AuthManager:
    """Gerenciador de autenticação e autorização"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.auditoria = get_auditoria()
        self.usuario_atual: Optional[Dict] = None
    
    def hash_password(self, password: str) -> str:
        """Gera hash SHA-256 da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, nome_usuario: str, senha: str) -> bool:
        """
        Realiza login do usuário
        
        Args:
            nome_usuario: Nome do usuário
            senha: Senha em texto plano
            
        Returns:
            bool: True se login bem-sucedido, False caso contrário
        """
        try:
            # Validar credenciais
            user_data = self.db.validar_login(nome_usuario, senha)
            
            if user_data:
                self.usuario_atual = user_data
                self.auditoria.log_login(nome_usuario, True)
                return True
            else:
                self.auditoria.log_login(nome_usuario, False)
                return False
                
        except Exception as e:
            self.auditoria.log_error(f"Erro durante login: {e}")
            return False
    
    def logout(self) -> bool:
        """
        Realiza logout do usuário atual
        
        Returns:
            bool: True se logout bem-sucedido
        """
        if self.usuario_atual:
            usuario = self.usuario_atual['nome_usuario']
            self.auditoria.log_logout(usuario)
            self.usuario_atual = None
            return True
        return False
    
    def is_authenticated(self) -> bool:
        """
        Verifica se há usuário autenticado
        
        Returns:
            bool: True se usuário está autenticado
        """
        return self.usuario_atual is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Retorna dados do usuário atual
        
        Returns:
            Dict com dados do usuário ou None se não autenticado
        """
        return self.usuario_atual
    
    def get_current_user_id(self) -> Optional[int]:
        """
        Retorna ID do usuário atual
        
        Returns:
            int ID do usuário ou None se não autenticado
        """
        return self.usuario_atual['id'] if self.usuario_atual else None
    
    def get_current_user_name(self) -> Optional[str]:
        """
        Retorna nome do usuário atual
        
        Returns:
            str nome do usuário ou None se não autenticado
        """
        return self.usuario_atual['nome_usuario'] if self.usuario_atual else None
    
    def is_admin(self) -> bool:
        """
        Verifica se o usuário atual é administrador
        
        Returns:
            bool: True se usuário é admin
            
        Raises:
            UsuarioNaoAutenticadoError: Se não há usuário autenticado
        """
        if not self.is_authenticated():
            raise UsuarioNaoAutenticadoError()
        
        return self.usuario_atual['perfil'] == 'admin'
    
    def require_auth(self):
        """
        Verifica se usuário está autenticado
        
        Raises:
            UsuarioNaoAutenticadoError: Se não há usuário autenticado
        """
        if not self.is_authenticated():
            raise UsuarioNaoAutenticadoError()
    
    def require_admin(self):
        """
        Verifica se usuário é administrador
        
        Raises:
            UsuarioNaoAutenticadoError: Se não há usuário autenticado
            PermissaoNegadaError: Se usuário não é admin
        """
        self.require_auth()
        if not self.is_admin():
            raise PermissaoNegadaError("operacao_admin", "admin")
    
    def criar_usuario(self, nome_usuario: str, senha: str, perfil: str) -> bool:
        """
        Cria um novo usuário (apenas para admins)
        
        Args:
            nome_usuario: Nome do usuário
            senha: Senha em texto plano
            perfil: Perfil do usuário ('admin' ou 'comum')
            
        Returns:
            bool: True se usuário criado com sucesso
            
        Raises:
            PermissaoNegadaError: Se usuário não é admin
        """
        self.require_admin()
        
        try:
            sucesso = self.db.criar_usuario(nome_usuario, senha, perfil)
            if sucesso:
                self.auditoria.log_criacao("usuario", nome_usuario, self.get_current_user_name())
            return sucesso
        except Exception as e:
            self.auditoria.log_error(f"Erro ao criar usuário {nome_usuario}: {e}")
            return False
    
    def alterar_senha(self, senha_atual: str, nova_senha: str) -> bool:
        """
        Altera senha do usuário atual
        
        Args:
            senha_atual: Senha atual
            nova_senha: Nova senha
            
        Returns:
            bool: True se senha alterada com sucesso
        """
        self.require_auth()
        
        try:
            # Verificar senha atual
            if not self.db.validar_login(self.get_current_user_name(), senha_atual):
                raise SenhaInvalidaError()
            
            # Atualizar senha no banco
            nova_senha_hash = self.hash_password(nova_senha)
            with self.db.get_connection() as conn:
                conn.execute(
                    "UPDATE usuarios SET senha_hash = ? WHERE id = ?",
                    (nova_senha_hash, self.get_current_user_id())
                )
                conn.commit()
            
            self.auditoria.log_atualizacao("usuario", str(self.get_current_user_id()), 
                                         self.get_current_user_name(), "Alteração de senha")
            return True
            
        except SenhaInvalidaError:
            raise
        except Exception as e:
            self.auditoria.log_error(f"Erro ao alterar senha: {e}")
            return False
    
    def obter_dados_usuario(self) -> Optional[Dict]:
        """
        Obtém dados completos do usuário atual
        
        Returns:
            Dict com dados do usuário ou None se não autenticado
        """
        if not self.is_authenticated():
            return None
        
        try:
            return self.db.obter_usuario_por_id(self.get_current_user_id())
        except Exception as e:
            self.auditoria.log_error(f"Erro ao obter dados do usuário: {e}")
            return None
    
    def verificar_permissao(self, operacao: str, perfil_necessario: str = "admin") -> bool:
        """
        Verifica se usuário tem permissão para operação
        
        Args:
            operacao: Nome da operação
            perfil_necessario: Perfil necessário ('admin' ou 'comum')
            
        Returns:
            bool: True se tem permissão
        """
        if not self.is_authenticated():
            return False
        
        if perfil_necessario == "admin":
            return self.is_admin()
        else:
            return True  # Usuários comuns podem fazer operações básicas
    
    def log_operacao(self, operacao: str, entidade: str, entidade_id: str, detalhes: str = ""):
        """
        Registra operação do usuário atual
        
        Args:
            operacao: Nome da operação
            entidade: Entidade afetada
            entidade_id: ID da entidade
            detalhes: Detalhes adicionais
        """
        if self.is_authenticated():
            self.auditoria.log_operacao(operacao, entidade, entidade_id, 
                                      self.get_current_user_name(), detalhes)
