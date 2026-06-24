# AgroBanana — Documento de Arquitetura e Visão Geral do TCC

**Aluno:** Erick Demathe  
**Instituição:** Católica SC  
**Projeto:** Sistema de Apoio à Decisão para Gestão de Bananais  
**URL de produção:** http://163.176.188.38:5000  
**Repositório:** https://github.com/Erickdemathe123/tcc  

---

## 1. Visão Geral do Sistema

O **AgroBanana** é uma aplicação web de apoio à decisão voltada para produtores rurais de banana. O sistema permite o cadastro e monitoramento de propriedades e talhões, registro de manejos, colheitas, custos e ocorrências de pragas/doenças, gerando automaticamente alertas, indicadores de desempenho e recomendações técnicas.

---

## 2. Diagrama C4 — Nível 1: Contexto do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                      CONTEXTO DO SISTEMA                        │
└─────────────────────────────────────────────────────────────────┘

        ┌──────────────────┐
        │  Produtor Rural  │
        │                  │
        │ - Registra       │
        │   atividades     │
        │ - Consulta       │
        │   relatórios     │
        │ - Recebe alertas │
        └────────┬─────────┘
                 │  Acessa via navegador (HTTP)
                 ▼
   ┌─────────────────────────────────┐
   │                                 │
   │   AgroBanana                    │
   │   Sistema Inteligente de        │
   │   Gestão de Bananais            │
   │                                 │
   │   [Aplicação Web Flask/Python]  │
   │                                 │
   │   - Cadastro de propriedades    │
   │   - Monitoramento de talhões    │
   │   - Alertas automáticos         │
   │   - Diagnóstico situacional     │
   │   - Indicadores e relatórios    │
   │                                 │
   └──────────────┬──────────────────┘
                  │  SMTP (TLS 587)
                  ▼
   ┌──────────────────────────────────┐
   │  Serviços Externos               │
   │                                  │
   │  - Gmail SMTP                    │
   │    (envio de e-mails de          │
   │     recuperação de senha)        │
   └──────────────────────────────────┘
```

---

## 3. Diagrama C4 — Nível 2: Containers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CONTAINERS                                    │
└─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐        ┌──────────────────────────────────────────────┐
  │  Navegador  │        │          Aplicação Web Flask                 │
  │  do Usuário │──────▶│                                              │
  │             │ HTTP   │  [Python 3.11 + Flask 3.x]                  │
  │  Chrome /   │        │  [Gunicorn WSGI — 2 workers]                │
  │  Firefox /  │        │  [Jinja2 Templates + Bootstrap 5]           │
  │  Edge       │        │                                              │
  └─────────────┘        │  Responsável por:                           │
                         │  - Renderizar páginas HTML                  │
                         │  - Processar formulários                    │
                         │  - Autenticar usuários                      │
                         │  - Executar serviços de análise             │
                         │  - Gerar alertas e recomendações            │
                         │                                              │
                         └─────────────────┬────────────────────────────┘
                                           │  SQLAlchemy ORM
                                           │  (psycopg2)
                                           ▼
                         ┌────────────────────────────────────────────┐
                         │          Banco de Dados                    │
                         │                                            │
                         │  [PostgreSQL 15]                           │
                         │  [Docker container — porta 5432]           │
                         │                                            │
                         │  Tabelas:                                  │
                         │  - usuarios                                │
                         │  - propriedades                            │
                         │  - talhoes                                 │
                         │  - talhao_variedades                       │
                         │  - manejos                                 │
                         │  - ocorrencias                             │
                         │  - colheitas / colheita_itens              │
                         │  - custos                                  │
                         └────────────────────────────────────────────┘

                         ┌────────────────────────────────────────────┐
                         │          Servidor de E-mail                │
                         │                                            │
                         │  [Gmail SMTP — smtp.gmail.com:587]        │
                         │                                            │
                         │  - Recuperação de senha                   │
                         │  - Token com expiração (1h)               │
                         └────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │                    Infraestrutura                               │
  │                                                                 │
  │  Oracle Cloud Free Tier — VM Ubuntu 22.04 (São Paulo)          │
  │  CPU: ARM Ampere A1 — RAM: 24 GB — Disco: 47 GB               │
  │  IP Público: 163.176.188.38                                    │
  │  Docker + Docker Compose (orquestração dos containers)         │
  └─────────────────────────────────────────────────────────────────┘
```

---

## 4. Diagrama C4 — Nível 3: Componentes Internos da Aplicação

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPONENTES — Aplicação Flask                        │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │                        MÓDULO DE ROTAS (Blueprints)                  │
  │                                                                      │
  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐               │
  │  │  auth.py    │  │ dashboard.py │  │propriedades  │               │
  │  │             │  │              │  │    .py       │               │
  │  │ - Login     │  │ - KPIs gerais│  │              │               │
  │  │ - Registro  │  │ - Alertas    │  │ - CRUD       │               │
  │  │ - Logout    │  │   recentes   │  │   fazendas   │               │
  │  │ - Reset     │  │ - Gráficos   │  │              │               │
  │  │   senha     │  │              │  │              │               │
  │  └─────────────┘  └──────────────┘  └──────────────┘               │
  │                                                                      │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
  │  │talhoes   │  │manejos   │  │ocorrencias│  │colheitas │           │
  │  │  .py     │  │  .py     │  │   .py     │  │  .py     │           │
  │  │          │  │          │  │           │  │          │           │
  │  │ - CRUD   │  │ - CRUD   │  │ - CRUD    │  │ - CRUD   │           │
  │  │   talhões│  │   manejos│  │   pragas/ │  │   colhei-│           │
  │  │ - Área   │  │ - Tipos  │  │   doenças │  │   tas    │           │
  │  │ - Plantio│  │ - Datas  │  │ - Severi- │  │ - Itens  │           │
  │  │          │  │          │  │   dade    │  │   multi- │           │
  │  │          │  │          │  │           │  │   varie- │           │
  │  │          │  │          │  │           │  │   dade   │           │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
  │                                                                      │
  │  ┌──────────────────────┐  ┌────────────────────────────────┐      │
  │  │  custos.py           │  │  relatorios.py                 │      │
  │  │                      │  │                                │      │
  │  │  - CRUD custos       │  │  - Relatório financeiro        │      │
  │  │  - Categorias        │  │  - Relatório de produção       │      │
  │  │  - Totais por período│  │  - Histórico de ocorrências    │      │
  │  └──────────────────────┘  └────────────────────────────────┘      │
  └──────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │                        CAMADA DE SERVIÇOS                           │
  │                                                                      │
  │  ┌───────────────────────────────────────────────────────────────┐  │
  │  │  services/indicadores.py                                      │  │
  │  │                                                               │  │
  │  │  Calcula KPIs por talhão:                                    │  │
  │  │  - Produtividade (cx/ha)           - Receita total           │  │
  │  │  - Custo por caixa (R$/cx)         - Lucro estimado          │  │
  │  │  - Margem de lucro (%)             - Dias desde último manejo│  │
  │  └───────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ┌───────────────────────────────────────────────────────────────┐  │
  │  │  services/alertas.py — 8 regras de negócio                   │  │
  │  │                                                               │  │
  │  │  Regra 1: Sem manejo registrado (warning)                    │  │
  │  │  Regra 2: Manejo > 60 dias (danger)                          │  │
  │  │  Regra 3: Alta incidência de pragas — 3+ em 30 dias (danger) │  │
  │  │  Regra 4: Ocorrência grave recente — < 60 dias (danger)      │  │
  │  │  Regra 5: Custo total elevado > R$ 5.000 (warning)           │  │
  │  │  Regra 6: Reincidência de praga/doença (warning)             │  │
  │  │  Regra 7: Previsão de colheita — > 270 dias sem colher (info)│  │
  │  │  Regra 8: Prejuízo estimado — custos > receita (danger)      │  │
  │  └───────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ┌───────────────────────────────────────────────────────────────┐  │
  │  │  services/diagnostico.py — Sistema de pontuação              │  │
  │  │                                                               │  │
  │  │  classificar_talhao():                                       │  │
  │  │  - Pontuação 0–10 por critério                               │  │
  │  │  - Situação: normal / atenção / crítico                      │  │
  │  │  - Motivos positivos e negativos                             │  │
  │  │                                                               │  │
  │  │  gerar_recomendacoes():                                      │  │
  │  │  - Prioridade: urgente / alta / média / info                 │  │
  │  │  - Ordenadas por urgência                                    │  │
  │  └───────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │                        CAMADA DE MODELOS (SQLAlchemy ORM)           │
  │                                                                      │
  │  Usuario ──┐                                                        │
  │            ├── Propriedade ──── Talhao ──┬── TalhaoVariedade        │
  │            │                             ├── Manejo                 │
  │            │                             ├── Ocorrencia             │
  │            │                             ├── Colheita ── ColheitaItem│
  │            │                             └── Custo                  │
  └──────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │                        SEGURANÇA & AUTENTICAÇÃO                     │
  │                                                                      │
  │  - Flask-Login: sessões de usuário + @login_required               │
  │  - Werkzeug: hashing de senhas (PBKDF2-SHA256)                     │
  │  - itsdangerous: token de reset com expiração (URLSafeTimedSerializer)│
  │  - CSRF: WTF_CSRF_ENABLED em produção                              │
  │  - Isolamento por usuário: queries filtradas por usuario_id         │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Diagrama de Infraestrutura e CI/CD

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PIPELINE CI/CD                                  │
└─────────────────────────────────────────────────────────────────────────┘

  Desenvolvedor
      │
      │  git push → GitHub (master)
      ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │               GitHub Actions (.github/workflows/ci.yml)          │
  │                                                                  │
  │  Stage 1 — Lint          Stage 2 — Testes                       │
  │  ┌──────────────────┐    ┌───────────────────────────────────┐  │
  │  │ flake8 (estilo)  │    │ pytest + pytest-cov               │  │
  │  │ bandit (segurança│    │ SQLite in-memory                  │  │
  │  └──────────────────┘    │ 115 testes / 61% cobertura total  │  │
  │                          │ 100% cobertura na camada services  │  │
  │                          └───────────────────────────────────┘  │
  │                                                                  │
  │  Stage 3 — Migrations     Stage 4 — Docker Build               │
  │  ┌──────────────────────┐  ┌──────────────────────────────┐    │
  │  │ PostgreSQL service   │  │ Build imagem Docker          │    │
  │  │ flask db upgrade     │  │ Push → ghcr.io               │    │
  │  │ (validação real)     │  └──────────────────────────────┘    │
  │  └──────────────────────┘                                       │
  │                                                                  │
  │  Stage 5 — Deploy                                               │
  │  ┌──────────────────────────────────────────────────────────┐   │
  │  │ SSH → Oracle Cloud VPS                                   │   │
  │  │ git pull + docker compose up -d --build                  │   │
  │  └──────────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │               Oracle Cloud Free Tier VPS                         │
  │               Ubuntu 22.04 — São Paulo — 163.176.188.38          │
  │                                                                  │
  │   ┌──────────────────────────────────────────────────────────┐  │
  │   │  Docker Compose                                          │  │
  │   │                                                          │  │
  │   │  ┌─────────────────────┐   ┌──────────────────────────┐ │  │
  │   │  │  agrobanana-web     │   │  agrobanana-db           │ │  │
  │   │  │  Python 3.11-slim   │──▶│  PostgreSQL 15-alpine    │ │  │
  │   │  │  Gunicorn :5000     │   │  Volume persistente       │ │  │
  │   │  │  flask db upgrade   │   │  Healthcheck             │ │  │
  │   │  └─────────────────────┘   └──────────────────────────┘ │  │
  │   └──────────────────────────────────────────────────────────┘  │
  │                                                                  │
  │   Firewall (iptables + Oracle Security List):                   │
  │   - Porta 22  (SSH)                                             │
  │   - Porta 80  (HTTP)                                            │
  │   - Porta 443 (HTTPS)                                           │
  │   - Porta 5000 (Gunicorn/Flask)                                 │
  └──────────────────────────────────────────────────────────────────┘
```

---

## 6. Stack Tecnológica Completa

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Linguagem | Python | 3.11 |
| Framework Web | Flask | 3.x |
| ORM | SQLAlchemy + Flask-SQLAlchemy | 3.x |
| Migrations | Flask-Migrate (Alembic) | — |
| Autenticação | Flask-Login | — |
| Hashing de senhas | Werkzeug (PBKDF2-SHA256) | — |
| Tokens de reset | itsdangerous | — |
| E-mail | Flask-Mail + Gmail SMTP | — |
| Templates | Jinja2 + Bootstrap 5 | — |
| Ícones | Bootstrap Icons | — |
| Banco de dados | PostgreSQL | 15 |
| Servidor WSGI | Gunicorn | 26.x |
| Containerização | Docker + Docker Compose | 29.x |
| CI/CD | GitHub Actions | — |
| Hospedagem | Oracle Cloud Free Tier | Ubuntu 22.04 |
| Testes | pytest + pytest-cov | 8.x / 5.x |
| Análise estática | flake8 + bandit | — |

---

## 7. Funcionalidades Implementadas

### 7.1 Autenticação e Usuários
- Registro com validação de senha (mínimo 6 caracteres)
- Login com sessão persistente (Flask-Login)
- Recuperação de senha por e-mail com token temporário (1h)
- Logout com limpeza de sessão
- Proteção de todas as rotas com `@login_required`
- Isolamento total de dados por usuário

### 7.2 Propriedades
- Cadastro de fazendas/propriedades com área, localização e produtor
- Listagem com indicadores resumidos por propriedade
- Edição e exclusão (cascade para talhões)

### 7.3 Talhões
- Cadastro com área (ha), data de plantio e variedades (múltiplas)
- Página de detalhes com todos os registros do talhão
- 16 variedades catalogadas (Nanica, Prata, Grand Naine, etc.)

### 7.4 Manejos
- 9 tipos: Capina, Adubação, Irrigação, Poda, Tratamento Fitossanitário, Desbaste, Ensacamento, Colheita de Mudas, Outros
- Registro de responsável e descrição
- Histórico cronológico por talhão

### 7.5 Ocorrências de Pragas e Doenças
- 11 pragas/doenças catalogadas com fichas técnicas completas
- Níveis de severidade: Leve, Moderada, Grave
- Recomendações técnicas específicas por praga e severidade
- Área afetada (ha) e tratamento aplicado

### 7.6 Colheitas
- Registro por talhão com múltiplos itens (multi-variedade)
- Campos: variedade, quantidade de caixas, peso/caixa, preço/caixa
- Cálculo automático de receita total e peso total
- Destinos: Mercado Local, CEASA, Supermercado, Cooperativa, Exportação

### 7.7 Custos
- 5 categorias: Mão de Obra, Insumos, Maquinário, Transporte, Outros
- Registro por talhão com data e descrição
- Histórico completo com totais

### 7.8 Dashboard
- KPIs agregados da propriedade selecionada
- Alertas ativos com classificação por severidade
- Diagnóstico situacional dos talhões (normal/atenção/crítico)
- Recomendações priorizadas

### 7.9 Relatórios
- Relatório financeiro (receitas vs custos vs margem)
- Relatório de produção (produtividade por talhão)
- Histórico de ocorrências com filtros

---

## 8. Cobertura de Testes

| Módulo | Testes | Cobertura |
|--------|--------|-----------|
| `services/indicadores.py` | 28 | 100% |
| `services/alertas.py` | 22 | 100% |
| `services/diagnostico.py` | 20 | 89% |
| `models/*.py` | 30 | ~85% |
| `routes/auth.py` | 15 | ~70% |
| **Total** | **115** | **61%** |

---

## 9. Modelo de Dados (Entidade-Relacionamento)

```
usuarios
  id | nome | email | senha_hash | created_at
  │
  └── propriedades
        id | usuario_id (FK) | nome | localizacao | area_total_ha | produtor_nome | created_at
        │
        └── talhoes
              id | propriedade_id (FK) | nome | area_ha | data_plantio | created_at
              │
              ├── talhao_variedades
              │     id | talhao_id (FK) | variedade
              │
              ├── manejos
              │     id | talhao_id (FK) | tipo | data_manejo | descricao | responsavel | created_at
              │
              ├── ocorrencias
              │     id | talhao_id (FK) | tipo | nome | data_ocorrencia | severidade
              │         | area_afetada_ha | tratamento_aplicado | created_at
              │
              ├── colheitas
              │     id | talhao_id (FK) | data_colheita | destino | created_at
              │     │
              │     └── colheita_itens
              │           id | colheita_id (FK) | variedade | quantidade_caixas
              │               | peso_por_caixa | preco_por_caixa
              │
              └── custos
                    id | talhao_id (FK) | data_custo | categoria | descricao | valor | created_at
```

---

## 10. Requisitos do Curso Atendidos

| Requisito | Status |
|-----------|--------|
| Banco de dados relacional (não SQLite) | ✅ PostgreSQL 15 |
| Deploy em servidor público | ✅ Oracle Cloud — 163.176.188.38:5000 |
| Containerização | ✅ Docker + Docker Compose |
| CI/CD pipeline | ✅ GitHub Actions (5 stages) |
| Cobertura de testes ≥ 75% (camada de serviços) | ✅ 100% nos services |
| Análise estática de código | ✅ flake8 + bandit |
| Documentação RFC | ✅ RFC_AgroBanana.md |
| Autenticação segura | ✅ Flask-Login + PBKDF2 |
