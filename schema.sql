-- Schema do Sistema de Seguros
-- Criado para migração de JSON para SQLite

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('admin', 'comum')),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
);

-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
);

-- Tabela de Seguros
CREATE TABLE IF NOT EXISTS seguros (
    id TEXT PRIMARY KEY,
    tipo TEXT NOT NULL CHECK (tipo IN ('Automóvel', 'Residencial', 'Vida')),
    valor_cobertura REAL NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status TEXT DEFAULT 'ativo' CHECK (status IN ('ativo', 'cancelado', 'vencido')),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Campos específicos para Seguro Automóvel
    marca TEXT,
    modelo TEXT,
    ano INTEGER,
    placa TEXT,
    estado_conservacao TEXT,
    uso_veiculo TEXT,
    num_condutores INTEGER,
    
    -- Campos específicos para Seguro Residencial
    endereco_imovel TEXT,
    area REAL,
    valor_venal REAL,
    tipo_construcao TEXT,
    
    -- Campos específicos para Seguro Vida
    beneficiarios TEXT, -- JSON string
    tipos_cobertura TEXT -- JSON string
);

-- Tabela de Apólices
CREATE TABLE IF NOT EXISTS apolices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    cliente_id INTEGER NOT NULL,
    seguro_id TEXT NOT NULL,
    status TEXT DEFAULT 'ativa' CHECK (status IN ('ativa', 'cancelada', 'vencida')),
    premio REAL NOT NULL,
    valor_segurado REAL NOT NULL,
    data_emissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_vencimento DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (seguro_id) REFERENCES seguros(id)
);

-- Tabela de Sinistros
CREATE TABLE IF NOT EXISTS sinistros (
    id TEXT PRIMARY KEY,
    apolice_id INTEGER NOT NULL,
    data_ocorrencia DATE NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descricao TEXT NOT NULL,
    valor_prejuizo REAL NOT NULL,
    status TEXT DEFAULT 'aberto' CHECK (status IN ('aberto', 'em_analise', 'aprovado', 'negado', 'fechado')),
    valor_indenizacao REAL,
    observacoes TEXT,
    FOREIGN KEY (apolice_id) REFERENCES apolices(id)
);

-- Tabela de Auditoria/Logs
CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    acao TEXT NOT NULL,
    entidade TEXT NOT NULL,
    entidade_id TEXT,
    dados_anteriores TEXT, -- JSON
    dados_novos TEXT, -- JSON
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_clientes_cpf ON clientes(cpf);
CREATE INDEX IF NOT EXISTS idx_apolices_numero ON apolices(numero);
CREATE INDEX IF NOT EXISTS idx_apolices_cliente ON apolices(cliente_id);
CREATE INDEX IF NOT EXISTS idx_sinistros_apolice ON sinistros(apolice_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria(usuario_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_timestamp ON auditoria(timestamp);

-- Inserir usuário admin padrão
INSERT OR IGNORE INTO usuarios (nome_usuario, senha_hash, perfil) 
VALUES ('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'admin');
-- Senha: password (hash SHA-256)
