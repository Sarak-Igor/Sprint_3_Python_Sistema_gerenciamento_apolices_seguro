**Sprint:** 3 - Sistema de Registros e Gerenciamento de Seguros com SQLite

## 📋 Informações do Projeto

**Integrantes:**
1. **Lucca Phelipe Masini** - RM 564121 
2. **Luis Fernando de Oliveira Salgado** - RM 561401 
3. **Igor Paixão Sarak** - RM 563726 
4. **Bernardo Braga Perobeli** - RM 562468


## 🎯 Objetivos da Sprint

Esta sprint implementa um sistema robusto de gerenciamento de seguros com as seguintes melhorias:

- ✅ **Migração para SQLite**: Substituição dos arquivos JSON por banco de dados SQLite
- ✅ **Sistema de Auditoria**: Logs completos de todas as operações
- ✅ **Autenticação Segura**: Sistema de login com hash de senhas
- ✅ **Tratamento de Erros**: Exceções customizadas e tratamento robusto
- ✅ **Relatórios Avançados**: Queries SQL complexas para análise de dados
- ✅ **Interface Dupla**: CLI intuitiva e GUI moderna com TTKthemes

## 🛠️ Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 📦 Instalação

1. **Clone o repositório** (se aplicável):
```bash
git clone <url-do-repositorio>
cd sistema-seguros-sprint3
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute a migração** (primeira vez apenas):
```bash
python migrate.py
```

## 🚀 Como Iniciar a Aplicação

### Interface Gráfica (Recomendada)
```bash
python main_gui.py
```

### Interface de Linha de Comando
```bash
python main.py
```

## 📊 Estrutura do Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas principais:

- **usuarios**: Gerenciamento de usuários e permissões
- **clientes**: Dados dos clientes
- **seguros**: Tipos de seguros (Automóvel, Residencial, Vida)
- **apolices**: Apólices emitidas
- **sinistros**: Registro de sinistros
- **auditoria**: Logs de todas as operações

## 📁 Estrutura de Arquivos

```
sistema-seguros/
├── main.py                 # Ponto de entrada CLI
├── main_gui.py            # Ponto de entrada GUI
├── cli_sqlite.py          # Interface CLI
├── interface_sqlite.py    # Interface GUI
├── database.py            # Camada de acesso a dados (DAL)
├── auth_sqlite.py         # Sistema de autenticação
├── relatorios_sqlite.py   # Módulo de relatórios
├── logger_config.py       # Configuração de logs
├── exceptions.py          # Exceções customizadas
├── migrate.py            # Script de migração JSON → SQLite
├── schema.sql            # Schema do banco de dados
├── login.py              # Sistema de login
├── cadastro_usuario_window.py  # Janela de cadastro
├── usuarios_window.py    # Janela de usuários
├── cliente.py            # Classe Cliente
├── apolice.py            # Classe Apólice
├── seguro.py             # Classes de Seguro
├── sinistro.py           # Classe Sinistro
├── test_sistema.py       # Testes do sistema
├── test_gui.py          # Testes da interface gráfica
├── requirements.txt      # Dependências Python
├── seguradora.db         # Banco de dados SQLite
├── auditoria.log         # Logs de auditoria
├── export/               # Diretório para relatórios exportados
├── backup_json/          # Backup dos arquivos JSON originais
└── README.md             # Este arquivo
```

## 🔐 Sistema de Autenticação

### Usuário Padrão
- **Usuário:** admin
- **Senha:** password
- **Perfil:** administrador

### Perfis de Usuário
- **admin**: Acesso completo ao sistema
- **comum**: Acesso limitado às funcionalidades básicas

## 📈 Funcionalidades Implementadas

### 1. Gerenciamento de Clientes
- ✅ Cadastro de clientes com validação completa
- ✅ Busca por CPF
- ✅ Listagem de clientes
- ✅ Validação de CPF, email e dados

### 2. Sistema de Relatórios
- ✅ **Receita Mensal**: Análise de receita por mês/ano
- ✅ **Top Clientes**: Clientes com maior valor segurado
- ✅ **Sinistros por Status**: Estatísticas de sinistros
- ✅ **Apólices Ativas**: Lista de apólices em vigor
- ✅ **Sinistros Recentes**: Sinistros dos últimos dias
- ✅ **Exportação CSV**: Todos os relatórios podem ser exportados

### 3. Sistema de Auditoria
- ✅ Logs de todas as operações
- ✅ Rastreabilidade completa
- ✅ Registro de usuário e timestamp
- ✅ Logs salvos em `auditoria.log`

### 4. Tratamento de Erros
- ✅ Exceções customizadas para cada tipo de erro
- ✅ Mensagens de erro amigáveis
- ✅ Validação robusta de dados
- ✅ Confirmações para operações críticas

## 🎮 Como Usar

### 1. Primeiro Acesso
```bash
# Executar migração (apenas primeira vez)
python migrate.py

# Iniciar sistema
python main_gui.py  # ou python main.py
```

### 2. Login
- Use as credenciais padrão: `admin` / `password`
- O sistema solicitará login a cada execução

### 3. Navegação

#### Interface Gráfica (GUI)
- Use as abas para navegar (Clientes, Relatórios)
- Preencha formulários e clique em botões
- Visualize dados em listas organizadas

#### Interface Terminal (CLI)
- Use os números para navegar pelos menus
- Digite dados quando solicitado
- Confirme operações críticas quando solicitado

### 4. Relatórios
- Acesse "5. Relatórios" no menu principal (CLI) ou aba "Relatórios" (GUI)
- Escolha o tipo de relatório desejado
- Configure parâmetros quando necessário
- Exporte para CSV se desejado

## 📊 Exemplos de Uso

### Cadastrar Cliente (CLI)
```
1. Menu Principal → 1. Gerenciar Clientes → 1. Cadastrar Cliente
2. Preencha os dados solicitados
3. Confirme a operação
```

### Cadastrar Cliente (GUI)
```
1. Aba "Clientes"
2. Preencha o formulário
3. Clique em "Cadastrar"
```

### Gerar Relatório de Receita (CLI)
```
1. Menu Principal → 5. Relatórios → 1. Receita Mensal
2. Digite o mês (1-12)
3. Digite o ano
4. Visualize o relatório
5. Exporte para CSV se desejado
```

### Gerar Relatório de Receita (GUI)
```
1. Aba "Relatórios"
2. Selecione "Receita Mensal"
3. Configure mês e ano
4. Clique em "Gerar Relatório"
5. Clique em "Exportar CSV" se desejado
```

## 🔍 Logs e Auditoria

### Localização dos Logs
- **Arquivo:** `auditoria.log`
- **Formato:** `YYYY-MM-DD HH:MM:SS - LEVEL - User: USER - MESSAGE`

### Exemplo de Log
```
2024-01-15 14:30:25 - INFO - User: admin - Operação: CREATE | Entidade: cliente | ID: 1
2024-01-15 14:31:10 - INFO - User: admin - Login SUCESSO para usuário: admin
```

## 📤 Exportação de Dados

### Localização dos Exports
- **Diretório:** `./export/`
- **Formato:** CSV com timestamp
- **Exemplo:** `receita_mensal_20240115_143025.csv`

### Tipos de Exportação
- Receita Mensal
- Top Clientes
- Sinistros por Status
- Apólices Ativas
- Sinistros Recentes

## 🛡️ Segurança

### Medidas Implementadas
- ✅ Senhas com hash SHA-256
- ✅ Validação de permissões por perfil
- ✅ Logs de auditoria completos
- ✅ Validação rigorosa de dados
- ✅ Tratamento de exceções

### Boas Práticas
- Altere a senha padrão do admin
- Monitore os logs de auditoria
- Faça backup regular do banco de dados
- Use perfis apropriados para cada usuário

## 🐛 Solução de Problemas

### Erro de Banco de Dados
```bash
# Verificar se o arquivo seguradora.db existe
ls -la seguradora.db

# Se não existir, executar migração
python migrate.py
```

### Erro de Permissão
- Verifique se o usuário tem perfil adequado
- Use usuário admin para operações administrativas

### Erro de Login
- Verifique usuário e senha
- Usuário padrão: admin / password

### Testar Sistema
```bash
# Testar sistema completo
python test_sistema.py

# Testar interface gráfica
python test_gui.py
```

## 🎨 Interface Gráfica (GUI)

### Características
- **Tema**: TTKthemes "adapta" moderno
- **Cores**: Azul Hierapolis (#007bff)
- **Layout**: Responsivo e intuitivo
- **Navegação**: Por abas (Clientes, Relatórios)

### Funcionalidades GUI
- ✅ Formulários visuais para cadastro
- ✅ Listas organizadas para visualização
- ✅ Relatórios com formatação rica
- ✅ Exportação com um clique
- ✅ Validação em tempo real

## 💻 Interface Terminal (CLI)

### Características
- **Navegação**: Por menus numerados
- **Velocidade**: Navegação rápida por teclado
- **Eficiência**: Menos recursos utilizados
- **Flexibilidade**: Ideal para automação

### Funcionalidades CLI
- ✅ Menus organizados e claros
- ✅ Confirmações de segurança
- ✅ Validação de dados
- ✅ Relatórios formatados
- ✅ Exportação automática

## 📝 Logs de Desenvolvimento

### Migração Realizada
- ✅ Criação do schema SQLite
- ✅ Implementação da DAL (Data Access Layer)
- ✅ Script de migração JSON → SQLite
- ✅ Sistema de autenticação com hash
- ✅ Logs de auditoria centralizados
- ✅ Exceções customizadas
- ✅ Relatórios com queries SQL
- ✅ Interface CLI melhorada
- ✅ Interface GUI moderna

### Melhorias Implementadas
- **Confiabilidade**: Banco de dados SQLite com transações
- **Rastreabilidade**: Logs completos de auditoria
- **Usabilidade**: Duas interfaces (CLI e GUI)
- **Segurança**: Autenticação e autorização
- **Manutenibilidade**: Código modular e documentado

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `auditoria.log`
2. Execute os testes: `python test_sistema.py`
3. Consulte este README
4. Execute `python migrate.py` se necessário
5. Verifique as permissões de arquivo

## 🎉 Conclusão

O sistema foi completamente migrado para SQLite com todas as funcionalidades solicitadas no planejamento. O código está modular, documentado e pronto para uso em produção.

**Status:** ✅ Concluído com sucesso!

### Funcionalidades Finais
- ✅ **Duas interfaces** (CLI e GUI)
- ✅ **Banco SQLite** robusto
- ✅ **Sistema de auditoria** completo
- ✅ **Relatórios avançados** com exportação
- ✅ **Segurança** com autenticação
- ✅ **Tratamento de erros** robusto
- ✅ **Código limpo** e organizado

**O sistema está pronto para uso em produção!** 🚀

