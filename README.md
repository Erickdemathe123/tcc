# AgroBanana

Sistema web de apoio à decisão para gestão e monitoramento de bananais.

**Stack:** Python · Flask · SQLAlchemy · PostgreSQL · Bootstrap 5

---

## Desenvolvimento local (com Docker)

### Pré-requisitos
- Docker Desktop instalado

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas configurações (SECRET_KEY, e-mail, etc.)
```

### 2. Subir os containers

```bash
docker compose up --build
```

O sistema estará disponível em `http://localhost:5000`.

### 3. Parar

```bash
docker compose down
```

---

## Desenvolvimento local (sem Docker)

### Pré-requisitos
- Python 3.11+
- PostgreSQL instalado e rodando (ou use SQLite para testes rápidos)

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 2. Instalar dependências
pip install -r requirements-dev.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env

# 4. Criar banco e rodar migrações
flask db upgrade

# 5. Iniciar servidor de desenvolvimento
flask run
```

---

## Testes

```bash
# Rodar todos os testes com relatório de cobertura
pytest

# Ver cobertura no navegador
coverage html
open htmlcov/index.html
```

### Metas de cobertura
| Camada | Meta |
|---|---|
| `app/services/` | ≥ 90% |
| `app/models/` | ≥ 80% |
| `app/routes/` | ≥ 60% |
| **Backend total** | **≥ 75%** |

---

## Deploy em produção (VPS / Hostinger)

### Pré-requisitos no servidor
- Ubuntu 22.04+
- Docker e Docker Compose instalados
- Domínio apontando para o IP do servidor

### 1. Conectar ao servidor

```bash
ssh usuario@IP_DO_SERVIDOR
```

### 2. Clonar o repositório

```bash
mkdir -p /opt/agrobanana && cd /opt/agrobanana
git clone https://github.com/SEU_USUARIO/agrobanana .
```

### 3. Configurar variáveis de produção

```bash
cp .env.example .env
nano .env
# Preencha: SECRET_KEY (forte!), DATABASE_URL, configurações de e-mail
```

### 4. Subir em produção

```bash
docker compose up -d
```

### 5. Verificar

```bash
docker compose ps
docker compose logs web
```

O sistema estará disponível na porta `5000`. Configure um Nginx como proxy reverso para HTTPS.

---

## CI/CD (GitHub Actions)

O pipeline `.github/workflows/ci.yml` executa automaticamente a cada push:

| Etapa | O que faz |
|---|---|
| **Lint** | `flake8` verifica o estilo do código |
| **Segurança** | `bandit` identifica vulnerabilidades |
| **Testes** | `pytest` com cobertura (SQLite in-memory) |
| **Migrações** | `flask db upgrade` contra PostgreSQL real |
| **Docker Build** | Valida que a imagem constrói sem erros |
| **Push imagem** | Publica em `ghcr.io` (somente branch master) |
| **Deploy** | SSH no servidor → `docker compose up -d` |

### Configurar secrets no GitHub

Em `Settings → Secrets and variables → Actions`, adicione:

| Secret | Valor |
|---|---|
| `VPS_HOST` | IP ou domínio do servidor |
| `VPS_USER` | Usuário SSH (ex.: `ubuntu`) |
| `VPS_SSH_KEY` | Chave SSH privada (conteúdo do `id_rsa`) |
| `SONAR_TOKEN` | Token do SonarCloud (opcional) |

---

## Estrutura do projeto

```
app/
├── models/       # Entidades ORM (SQLAlchemy)
├── routes/       # Controllers HTTP (Flask Blueprints)
├── services/     # Regras de negócio (indicadores, alertas, diagnóstico)
├── templates/    # Templates Jinja2
└── extensions.py # Instâncias Flask-SQLAlchemy, Login, Mail

tests/
├── conftest.py          # Fixtures compartilhadas
├── test_indicadores.py  # Testes dos indicadores econômicos
├── test_alertas.py      # Testes das 8 regras de alerta
├── test_diagnostico.py  # Testes do diagnóstico situacional
├── test_models.py       # Testes dos modelos SQLAlchemy
└── test_routes.py       # Testes das rotas HTTP
```

---

## Licença

Projeto acadêmico — TCC Engenharia de Software, Católica SC.
