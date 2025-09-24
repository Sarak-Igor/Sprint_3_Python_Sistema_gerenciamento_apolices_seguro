"""
Exceções customizadas do sistema de seguros
"""

class SistemaSegurosException(Exception):
    """Exceção base do sistema de seguros"""
    pass

class CpfInvalidoError(SistemaSegurosException):
    """Exceção para CPF inválido"""
    def __init__(self, cpf: str, motivo: str = ""):
        self.cpf = cpf
        self.motivo = motivo
        super().__init__(f"CPF inválido: {cpf}. {motivo}")

class EmailInvalidoError(SistemaSegurosException):
    """Exceção para email inválido"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email inválido: {email}")

class DataInvalidaError(SistemaSegurosException):
    """Exceção para data inválida"""
    def __init__(self, data: str, motivo: str = ""):
        self.data = data
        self.motivo = motivo
        super().__init__(f"Data inválida: {data}. {motivo}")

class ClienteNaoEncontradoError(SistemaSegurosException):
    """Exceção para cliente não encontrado"""
    def __init__(self, cpf: str):
        self.cpf = cpf
        super().__init__(f"Cliente com CPF {cpf} não encontrado")

class ClienteJaExisteError(SistemaSegurosException):
    """Exceção para cliente já existente"""
    def __init__(self, cpf: str):
        self.cpf = cpf
        super().__init__(f"Cliente com CPF {cpf} já existe")

class SeguroNaoEncontradoError(SistemaSegurosException):
    """Exceção para seguro não encontrado"""
    def __init__(self, seguro_id: str):
        self.seguro_id = seguro_id
        super().__init__(f"Seguro com ID {seguro_id} não encontrado")

class ApoliceNaoEncontradaError(SistemaSegurosException):
    """Exceção para apólice não encontrada"""
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Apólice {numero} não encontrada")

class ApoliceJaExisteError(SistemaSegurosException):
    """Exceção para apólice já existente"""
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Apólice {numero} já existe")

class ApoliceCanceladaError(SistemaSegurosException):
    """Exceção para operação em apólice cancelada"""
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Operação não permitida: Apólice {numero} está cancelada")

class ApoliceVencidaError(SistemaSegurosException):
    """Exceção para operação em apólice vencida"""
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Operação não permitida: Apólice {numero} está vencida")

class SinistroNaoEncontradoError(SistemaSegurosException):
    """Exceção para sinistro não encontrado"""
    def __init__(self, sinistro_id: str):
        self.sinistro_id = sinistro_id
        super().__init__(f"Sinistro com ID {sinistro_id} não encontrado")

class DataForaVigenciaError(SistemaSegurosException):
    """Exceção para data fora da vigência"""
    def __init__(self, data: str, data_inicio: str, data_fim: str):
        self.data = data
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        super().__init__(f"Data {data} fora da vigência ({data_inicio} a {data_fim})")

class ValorInvalidoError(SistemaSegurosException):
    """Exceção para valor inválido"""
    def __init__(self, valor: str, campo: str = ""):
        self.valor = valor
        self.campo = campo
        super().__init__(f"Valor inválido para {campo}: {valor}")

class UsuarioNaoEncontradoError(SistemaSegurosException):
    """Exceção para usuário não encontrado"""
    def __init__(self, usuario: str):
        self.usuario = usuario
        super().__init__(f"Usuário {usuario} não encontrado")

class UsuarioJaExisteError(SistemaSegurosException):
    """Exceção para usuário já existente"""
    def __init__(self, usuario: str):
        self.usuario = usuario
        super().__init__(f"Usuário {usuario} já existe")

class SenhaInvalidaError(SistemaSegurosException):
    """Exceção para senha inválida"""
    def __init__(self):
        super().__init__("Senha inválida")

class PermissaoNegadaError(SistemaSegurosException):
    """Exceção para permissão negada"""
    def __init__(self, operacao: str, perfil_necessario: str = "admin"):
        self.operacao = operacao
        self.perfil_necessario = perfil_necessario
        super().__init__(f"Permissão negada para operação '{operacao}'. Perfil necessário: {perfil_necessario}")

class UsuarioNaoAutenticadoError(SistemaSegurosException):
    """Exceção para usuário não autenticado"""
    def __init__(self):
        super().__init__("Usuário não autenticado. Faça login primeiro.")

class BancoDadosError(SistemaSegurosException):
    """Exceção para erro de banco de dados"""
    def __init__(self, operacao: str, detalhes: str = ""):
        self.operacao = operacao
        self.detalhes = detalhes
        super().__init__(f"Erro de banco de dados na operação '{operacao}'. {detalhes}")

class ArquivoNaoEncontradoError(SistemaSegurosException):
    """Exceção para arquivo não encontrado"""
    def __init__(self, arquivo: str):
        self.arquivo = arquivo
        super().__init__(f"Arquivo não encontrado: {arquivo}")

class FormatoArquivoError(SistemaSegurosException):
    """Exceção para formato de arquivo inválido"""
    def __init__(self, arquivo: str, formato_esperado: str = "JSON"):
        self.arquivo = arquivo
        self.formato_esperado = formato_esperado
        super().__init__(f"Formato inválido do arquivo {arquivo}. Formato esperado: {formato_esperado}")

class RelatorioError(SistemaSegurosException):
    """Exceção para erro em relatório"""
    def __init__(self, relatorio: str, detalhes: str = ""):
        self.relatorio = relatorio
        self.detalhes = detalhes
        super().__init__(f"Erro ao gerar relatório '{relatorio}'. {detalhes}")

class ExportacaoError(SistemaSegurosException):
    """Exceção para erro na exportação"""
    def __init__(self, formato: str, detalhes: str = ""):
        self.formato = formato
        self.detalhes = detalhes
        super().__init__(f"Erro ao exportar para {formato}. {detalhes}")
