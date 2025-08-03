# Sistema de Controle de Tempo - Desafio IABS

Sistema web desenvolvido em Django para controle e registro de tempo de trabalho em tarefas. Este projeto foi desenvolvido como parte do desafio técnico da IABS.

## Objetivo

Aplicação web simples que permite aos usuários:
- Cadastrar tarefas com descrições
- Registrar tempo de trabalho dedicado a cada tarefa
- Visualizar e filtrar registros de tempo por diversos critérios
- Gerenciar dados de forma segura com isolamento por usuário

## Funcionalidades

### ✅ Cadastro de Tarefas
- **Usuário responsável**: Relacionamento com modelo User do Django
- **Data de criação**: Timestamp automático de criação
- **Descrição**: Texto descritivo da tarefa

### ✅ Registro de Tempo de Trabalho
- **Tarefa**: Relacionamento com tarefa específica
- **Data do registro**: Data em que o trabalho foi realizado
- **Tempo trabalhado**: Duração do trabalho realizado
- **Descrição do trabalho**: Descrição opcional do que foi feito

### ✅ Sistema de Listagem e Filtragem
- **Lista de tarefas**: Visualização completa das tarefas do usuário
- **Lista de registros de tempo**: Visualização com filtros avançados
- **Filtros disponíveis**: Por tarefa, data (intervalo), descrição, usuário
- **Navegação intuitiva**: Clique na tarefa para ver seus registros

### ✅ Autenticação e Segurança
- Sistema completo de login/registro/logout
- Isolamento de dados por usuário
- Validação de modelos e formulários
- Proteção CSRF e outras práticas de segurança Django

## Tecnologias Utilizadas

- **Python 3.12**
- **Django 5.2.4**
- **SQLite** (banco de dados)
- **Bootstrap 5.3** (interface)
- **Docker & Docker Compose** (containerização)
- **python-dotenv** (gerenciamento de variáveis de ambiente)

## Pré-requisitos

### Para execução local:
- Python 3.12+
- pip (gerenciador de pacotes Python)

### Para execução com Docker:
- Docker
- Docker Compose

## Configuração do Ambiente

### Execução Local (Desenvolvimento)

1. **Clone o repositório:**
```bash
git clone https://github.com/Biankowski/iabs
cd iabs
```

2. **Crie e ative um ambiente virtual:**
```bash
# No Linux/Mac
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
   - O arquivo `.env` já está configurado para desenvolvimento
   - ⚠️ **ATENÇÃO**: Este arquivo contém credenciais e está incluído apenas para facilitar os testes

5. **Execute as migrações:**
```bash
cd desafio_iabs
python manage.py migrate
```

6. **Crie um superusuário (opcional):**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento:**
```bash
python manage.py runserver
```

8. **Acesse a aplicação:**
   - Aplicação: http://localhost:8000
   - Admin Django: http://localhost:8000/admin

### Execução com Docker

1. **Clone o repositório:**
```bash
git clone https://github.com/Biankowski/iabs
cd iabs
```

2. **Execute com Docker Compose:**
```bash
docker-compose up -d --build
```

3. **Acesse a aplicação:**
   - Aplicação: http://localhost:8000
   - Admin Django: http://localhost:8000/admin
   - **Usuário admin criado automaticamente**: `admin` / `admin123`

## Estrutura do Projeto

```
iabs/
├── desafio_iabs/                 # Projeto Django principal
│   ├── desafio_iabs/            # Configurações do projeto
│   │   ├── settings.py          # Configurações Django
│   │   ├── urls.py              # URLs principais
│   │   └── ...
│   ├── timetracker/             # App principal
│   │   ├── models.py            # Modelos (Task, TimeEntry)
│   │   ├── views.py             # Views da aplicação
│   │   ├── forms.py             # Formulários Django
│   │   ├── urls.py              # URLs do app
│   │   ├── admin.py             # Configuração do admin
│   │   ├── tests.py             # Testes automatizados
│   │   └── templates/           # Templates HTML
│   ├── manage.py                # Script de gerenciamento Django
│   └── db.sqlite3               # Banco de dados SQLite
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Configuração Docker
├── docker-compose.yml           # Orquestração Docker
├── entrypoint.sh               # Script de inicialização Docker
├── .env                        # Variáveis de ambiente
└── README.md                   # Este arquivo
```

## Executando Testes

### Testes Locais:
```bash
cd desafio_iabs
python manage.py test
```

## Como Usar a Aplicação

1. **Registro/Login:**
   - Acesse a aplicação e crie uma conta ou faça login
   - Cada usuário só vê suas próprias tarefas e registros

2. **Criando Tarefas:**
   - Vá para "Tarefas" no menu
   - Clique em "Nova Tarefa"
   - Preencha a descrição e salve

3. **Registrando Tempo:**
   - Clique em uma tarefa para ver seus registros
   - Clique em "Novo Registro"
   - Preencha data, duração e descrição do trabalho

4. **Filtrando Registros:**
   - Use os filtros por tarefa, data ou descrição
   - Combine múltiplos filtros para buscas específicas

## Segurança

⚠️ **IMPORTANTE**: Este projeto inclui um arquivo `.env` com credenciais para facilitar os testes. **EM PRODUÇÃO**:

- Adicione `.env` ao `.gitignore`
- Configure variáveis de ambiente no servidor
- Use serviços de gerenciamento seguro de segredos
- Gere uma `SECRET_KEY` forte e única
