# AgroBanana
link:https://erickdemathe.pythonanywhere.com/auth/login
> Sistema web de apoio à decisão para gestão e monitoramento de bananais.

**TCC — Engenharia de Software · Católica SC · 2025/2026**

---

## Contexto e Motivação

A bananicultura é uma das atividades agrícolas mais expressivas do Brasil, que figura entre os maiores produtores mundiais da fruta. Apesar disso, produtores de pequeno e médio porte enfrentam dificuldades para gerenciar informações produtivas e tomar decisões baseadas em dados — muitas vezes dependendo apenas da experiência empírica e de anotações em papel.

O **AgroBanana** foi desenvolvido como projeto de conclusão de curso para preencher essa lacuna: oferecer uma ferramenta acessível, digital e orientada por dados que auxilie o produtor a acompanhar cada talhão de sua propriedade, identificar problemas precocemente e tomar decisões mais embasadas sobre manejo, custos e colheita.

---

## Problema

Produtores rurais de banana frequentemente:

- Não registram sistematicamente as operações de manejo (adubação, controle de pragas, ensacamento etc.)
- Desconhecem o custo real por caixa produzida
- Detectam pragas e doenças tardiamente, quando o prejuízo já é alto
- Não possuem histórico de colheitas para comparar safras e projetar receitas
- Tomam decisões de investimento sem base em indicadores produtivos e econômicos

---

## Solução

O AgroBanana centraliza o ciclo de vida produtivo de um bananal em uma plataforma web, organizada em torno de **propriedades → talhões → registros**. O sistema processa os dados inseridos e aplica regras agronômicas para gerar alertas automáticos e classificar a situação de cada talhão, transformando dados brutos em informação acionável.

---

## Funcionalidades

### Gestão da Propriedade
- Cadastro de múltiplas propriedades por usuário
- Controle de talhões com área (ha), variedade de banana e data de plantio
- Visão consolidada dos indicadores de cada propriedade

### Registro de Manejos
Registro histórico de 15 tipos de operações agronômicas:
Plantio de Mudas, Retirada de Mudas, Adubação, Irrigação, Desbrotar/Desbaste, Desfolha, Amarração/Escoramento, Ensacamento, Passar Herbicida, Inseticida, Fungicida, Nematicida, Adubo Líquido, Tratamento Fitossanitário e Outros.

### Monitoramento de Ocorrências
- Registro de pragas e doenças com nível de severidade (Leve / Moderada / Grave)
- Base de conhecimento integrada com recomendações agronômicas para as principais ameaças da bananicultura (Sigatoka, Mal-do-Panamá, Moko, Broca-do-rizoma, Ácaros, entre outras)
- Histórico de evolução por talhão

### Colheitas e Custos
- Lançamento de colheitas com quantidade (caixas), peso e preço de venda
- Registro de custos por categoria (insumos, mão de obra, equipamentos etc.)
- Cálculo automático de receita e lucro estimado

### Indicadores de Desempenho
Calculados automaticamente a partir dos registros:

| Indicador | Descrição |
|---|---|
| Produtividade (cx/ha) | Caixas colhidas por hectare |
| Produtividade (kg/ha) | Kg colhidos por hectare |
| Custo por caixa (R$) | Custo total ÷ caixas produzidas |
| Custo por hectare (R$) | Custo total ÷ área do talhão |
| Lucro estimado (R$) | Receita total − Custo total |
| Distribuição de custos | Gasto por categoria de insumo |

### Engine de Alertas
8 regras agronômicas avaliadas automaticamente:
- Talhão sem manejo há mais de 30 ou 60 dias
- Alta incidência de pragas (≥ 3 ocorrências em 30 dias)
- Ocorrência grave recente
- Custo total acima do limiar definido
- Previsão de colheita próxima (≥ 9 meses desde a última)
- Ausência total de registros de colheita, manejo ou ocorrências

### Diagnóstico Situacional
Cada talhão recebe uma classificação automática com base em pontuação ponderada dos indicadores:

| Situação | Critério |
|---|---|
| ✅ Normal | Produtividade boa, custo adequado, manejos em dia |
| ⚠️ Atenção | Algum indicador fora da faixa ideal |
| 🔴 Crítico | Produtividade baixa, custo alto ou manejos muito atrasados |

### Relatórios
- Relatório consolidado por propriedade
- Relatório detalhado por talhão (histórico completo)
- Exportável para impressão

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11 · Flask · SQLAlchemy · Flask-Login · Flask-Mail |
| Banco de dados | PostgreSQL (produção) · SQLite (testes) |
| Frontend | Bootstrap 5 · Bootstrap Icons · Jinja2 |
| Testes | pytest · pytest-cov |
| CI/CD | GitHub Actions |
| Containerização | Docker · Docker Compose |

---

## Arquitetura

```
app/
├── models/       # Entidades ORM: Usuario, Propriedade, Talhao, Manejo,
│                 #   Ocorrencia, Colheita, Custo
├── routes/       # Controllers HTTP (Flask Blueprints)
├── services/     # Regras de negócio desacopladas da camada HTTP
│   ├── indicadores.py   # Cálculo de KPIs produtivos e econômicos
│   ├── alertas.py       # Engine de 8 regras de alerta agronômico
│   └── diagnostico.py   # Classificação: normal / atenção / crítico
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
- PostgreSQL instalado e rodando

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

---

## Deploy em produção (VPS / Hostinger)

### Pré-requisitos no servidor
- Ubuntu 22.04+
- Docker e Docker Compose instalados

```bash
# 1. Conectar ao servidor
ssh usuario@IP_DO_SERVIDOR

# 2. Clonar o repositório
mkdir -p /opt/agrobanana && cd /opt/agrobanana
git clone https://github.com/Erickdemathe123/tcc .

# 3. Configurar variáveis de produção
cp .env.example .env
nano .env  # preencha SECRET_KEY, DATABASE_URL, e-mail

# 4. Subir em produção
docker compose up -d

# 5. Verificar
docker compose ps
docker compose logs web
```

---

## Licença

Projeto acadêmico — TCC Engenharia de Software, Católica SC.
