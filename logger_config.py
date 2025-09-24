"""
Configuração centralizada de logging e auditoria
"""

import logging
import os
from datetime import datetime
from typing import Optional

class AuditoriaLogger:
    """Logger centralizado para auditoria e logs do sistema"""
    
    def __init__(self, log_file: str = "auditoria.log"):
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        """Configura o logger com handlers para console e arquivo"""
        # Criar diretório de logs se não existir
        os.makedirs(os.path.dirname(self.log_file) if os.path.dirname(self.log_file) else ".", exist_ok=True)
        
        # Configurar logger principal
        self.logger = logging.getLogger('sistema_seguros')
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicação de handlers
        if self.logger.handlers:
            return
        
        # Formato padrão para logs
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - User: %(user)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para arquivo
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Adicionar handlers ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_info(self, message: str, user: str = "Sistema"):
        """Registra log de informação"""
        self.logger.info(message, extra={'user': user})
    
    def log_warning(self, message: str, user: str = "Sistema"):
        """Registra log de aviso"""
        self.logger.warning(message, extra={'user': user})
    
    def log_error(self, message: str, user: str = "Sistema"):
        """Registra log de erro"""
        self.logger.error(message, extra={'user': user})
    
    def log_critical(self, message: str, user: str = "Sistema"):
        """Registra log crítico"""
        self.logger.critical(message, extra={'user': user})
    
    def log_operacao(self, operacao: str, entidade: str, entidade_id: str, user: str, detalhes: str = ""):
        """Registra operação específica do sistema"""
        message = f"Operação: {operacao} | Entidade: {entidade} | ID: {entidade_id}"
        if detalhes:
            message += f" | Detalhes: {detalhes}"
        self.log_info(message, user)
    
    def log_login(self, user: str, sucesso: bool):
        """Registra tentativa de login"""
        status = "SUCESSO" if sucesso else "FALHA"
        self.log_info(f"Login {status} para usuário: {user}", user)
    
    def log_logout(self, user: str):
        """Registra logout"""
        self.log_info(f"Logout do usuário: {user}", user)
    
    def log_criacao(self, entidade: str, entidade_id: str, user: str, detalhes: str = ""):
        """Registra criação de entidade"""
        self.log_operacao("CREATE", entidade, entidade_id, user, detalhes)
    
    def log_atualizacao(self, entidade: str, entidade_id: str, user: str, detalhes: str = ""):
        """Registra atualização de entidade"""
        self.log_operacao("UPDATE", entidade, entidade_id, user, detalhes)
    
    def log_exclusao(self, entidade: str, entidade_id: str, user: str, detalhes: str = ""):
        """Registra exclusão de entidade"""
        self.log_operacao("DELETE", entidade, entidade_id, user, detalhes)
    
    def log_consulta(self, entidade: str, filtros: str, user: str):
        """Registra consulta/consulta"""
        self.log_operacao("SELECT", entidade, "N/A", user, f"Filtros: {filtros}")
    
    def log_relatorio(self, relatorio: str, user: str, parametros: str = ""):
        """Registra geração de relatório"""
        self.log_operacao("REPORT", "relatorio", relatorio, user, f"Parâmetros: {parametros}")

# Instância global do logger
auditoria = AuditoriaLogger()

def get_auditoria() -> AuditoriaLogger:
    """Retorna a instância global do logger de auditoria"""
    return auditoria
