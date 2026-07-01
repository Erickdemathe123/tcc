# RFC: Request for Comments — AgroBanana
**Engenharia de Software – Católica SC**

---

## Identificação

| Campo | Valor |
|---|---|
| **Título do Projeto** | AgroBanana — Sistema Web de Apoio à Decisão para Gestão e Monitoramento de Bananais |
| **Linha de Projeto (Direction)** | Web |
| **Autor** | Erick |
| **Data da Proposta** | 22/06/2026 |
| **Versão** | 1.0 |

---

## 1. Visão do Produto e Impacto (O Problema)

### 1.1 Contexto e Problema

A bananicultura é uma das atividades agrícolas mais expressivas do Brasil. O país é o quinto maior produtor mundial, com produção anual superior a 6,7 milhões de toneladas e mais de 500 mil produtores, a maioria de pequeno e médio porte (IBGE, 2022). A bananeira é cultivada em todos os estados brasileiros e representa fonte de renda fundamental para agricultores familiares.

Apesar de sua importância econômica, a gestão técnica e financeira das propriedades bananicultoras ainda é feita de forma informal pela maioria dos produtores: anotações em cadernos, planilhas desorganizadas ou simplesmente memória oral. Isso gera consequências diretas:

- **Falta de rastreabilidade:** o produtor não sabe com precisão qual talhão deu mais lucro, qual teve maior incidência de pragas ou qual manejo foi realizado e quando.
- **Decisões tardias:** sem alertas automáticos, pragas e doenças evoluem sem intervenção a tempo, e custos crescem sem que o produtor perceba a tendência.
- **Ineficiência econômica:** sem indicadores como custo por caixa ou produtividade por hectare, é impossível comparar talhões e identificar onde estão as ineficiências.
- **Ausência de diagnóstico situacional:** o produtor não tem como saber, de forma objetiva, se um talhão está em situação normal, de atenção ou crítica sem análise técnica especializada.

**Como o problema é resolvido atualmente:**

A maioria dos produtores depende de visitas esporádicas de técnicos agrícolas ou engenheiros agrônomos para obter uma avaliação do estado da lavoura. Entre visitas, o controle é feito manualmente (cadernos, memória) ou não é feito. Software agrícola existente tende a ser genérico, caro ou voltado para grandes propriedades.

**Limitações das soluções atuais:**

- Ferramentas caras e complexas demais para pequenos produtores.
- Soluções genéricas que não contemplam as especificidades da bananicultura (ciclo da bananeira, pragas específicas como Sigatoka-negra e Mal-do-Panamá, manejo por talhão).
- Ausência de geração automática de diagnóstico e recomendações acionáveis.

---

### 1.2 Origem da Demanda e Evidências

#### Contexto Acadêmico e Técnico

O projeto foi concebido como resposta a um problema real observado na literatura técnica e em relatos de produtores: a lacuna entre o conhecimento agronômico disponível e a capacidade do pequeno produtor de aplicá-lo no dia a dia, sem suporte de ferramentas acessíveis.

#### Evidência de Interesse

A demanda por digitalização do campo está documentada em diversas fontes:

- Relatórios da Embrapa Mandioca e Fruticultura apontam a Sigatoka-negra como a principal causa de perdas na bananicultura, com prejuízos estimados de 30–50% da produção quando não há monitoramento adequado.
- Levantamentos do SENAR e do SEBRAE sobre agricultura digital mostram que menos de 10% dos pequenos produtores rurais utilizam qualquer ferramenta digital para gestão da propriedade.
- A Política Nacional de Agricultura Digital (Decreto nº 10.329/2020) reconhece a necessidade de democratizar ferramentas de gestão para o produtor rural.

---

### 1.3 Análise de Soluções Existentes (Benchmark)

| Solução | Público-alvo | Funcionalidades Principais | Limitações |
|---|---|---|---|
| **AgroNote** | Produtores rurais em geral | Caderno digital de campo, tarefas | Sem indicadores, sem alertas, sem diagnóstico |
| **Aegro** | Médios e grandes produtores | ERP rural completo, financeiro, estoque | Caro, complexo, não especializado em banana |
| **Agrotools** | Grandes empresas do agro | Monitoramento remoto via satélite | Inacessível para pequenos produtores, sem gestão de talhão |
| **Planilha Excel/Google** | Qualquer produtor | Livre, familiar | Sem automação, sem alertas, sem diagnóstico integrado |
| **Embrapa Campo Futuro** | Produtores em geral | Comparativo econômico de safras | Não oferece gestão contínua, sem módulo de pragas |

#### Comparação Detalhada

| Critério | AgroNote | Aegro | Planilha | **AgroBanana** |
|---|---|---|---|---|
| Especializado em banana | Não | Não | Não | **Sim** |
| Alertas automáticos por regras | Não | Parcial | Não | **Sim (8 regras)** |
| Diagnóstico situacional | Não | Não | Não | **Sim (normal/atenção/crítico)** |
| Recomendações acionáveis | Não | Não | Não | **Sim (priorizadas)** |
| Custo acessível | Sim | Não | Sim | **Sim (gratuito)** |
| Gestão por talhão | Básico | Sim | Manual | **Sim** |
| Base de pragas/doenças integrada | Não | Não | Não | **Sim (10 pragas/doenças)** |

#### Diferencial do Projeto

O AgroBanana preenche uma lacuna específica: **não existe solução acessível, especializada em bananicultura, que combine gestão de talhões, alertas automáticos baseados em regras agronômicas e diagnóstico situacional com recomendações acionáveis.** O sistema foi projetado para o produtor que não tem formação técnica em agronomia mas precisa tomar decisões informadas no dia a dia.

---

### 1.4 Público-Alvo

**Perfil primário:** Produtor rural de banana de pequeno e médio porte com pelo menos uma propriedade e múltiplos talhões. Pode ter entre 30 e 60 anos, com nível básico a intermediário de familiaridade com tecnologia (uso de smartphone e aplicativos simples).

**Perfil secundário:** Técnico agrícola ou engenheiro agrônomo que acompanha múltiplos produtores e quer registrar ocorrências e monitorar propriedades de forma centralizada.

**Contexto de uso:** O sistema é acessado via navegador web, principalmente em computador ou tablet na sede da propriedade ou no escritório. O usuário registra dados após as atividades de campo (ao final do dia ou da semana) e consulta o dashboard para orientar as decisões da próxima semana.

**Nível de conhecimento técnico esperado:** Básico. O sistema não exige conhecimento de agronomia para uso — as recomendações são geradas automaticamente com base nos dados inseridos.

---

### 1.5 Objetivos do Projeto

#### Objetivo Geral

Desenvolver um sistema web de apoio à decisão para gestores de bananais, capaz de transformar dados operacionais de campo (manejos, colheitas, custos, pragas) em indicadores, alertas e diagnósticos que orientem decisões agronômicas e econômicas com base em regras técnicas.

#### Objetivos Específicos

1. Implementar módulo de cadastro de propriedades e talhões com suporte a múltiplas variedades de banana.
2. Implementar módulos de registro de manejos, ocorrências fitossanitárias, colheitas e custos por talhão.
3. Calcular automaticamente indicadores econômicos e agronômicos: produtividade (cx/ha e kg/ha), custo/ha, custo/caixa e lucro estimado.
4. Implementar engine de alertas automáticos com 8 regras agronômicas (manejo atrasado, pragas recorrentes, prejuízo estimado, queda de produtividade, entre outras).
5. Implementar sistema de diagnóstico por pontuação ponderada que classifica cada talhão como Normal, Atenção ou Crítico com justificativas detalhadas.
6. Gerar recomendações acionáveis priorizadas por urgência para orientar as decisões do produtor.
7. Prover autenticação segura com suporte a múltiplos usuários e recuperação de senha por e-mail.

---

### 1.6 Métricas de Sucesso (KPIs)

| Métrica | Meta |
|---|---|
| Tempo de resposta da aplicação | < 500 ms para 95% das requisições |
| Cobertura dos modelos de dados | Todos os módulos com persistência funcional |
| Regras de alerta implementadas | 8 regras ativas e testadas |
| Variedades de banana suportadas | 16 variedades cadastradas |
| Pragas/doenças com recomendações | 10 pragas/doenças com recomendações por severidade |
| Diagnóstico situacional | Classificação automática em 3 níveis: Normal, Atenção, Crítico |
| Segurança da autenticação | Hash de senha com Werkzeug (bcrypt), token de reset com expiração |

---

## 2. Engenharia de Requisitos

### 2.1 Personas

#### Persona 1 — João, o Produtor de Médio Porte

- **Idade:** 47 anos
- **Contexto:** Proprietário de 3 propriedades no interior de Santa Catarina, com cerca de 15 ha cultivados com banana Prata e Nanica.
- **Objetivos:** Saber quais talhões estão dando mais lucro, antecipar problemas fitossanitários antes que causem perdas grandes.
- **Dificuldades:** Não tem tempo para fazer contas detalhadas; esquece datas de manejos; descobre pragas tarde demais.

#### Persona 2 — Carla, a Técnica Agrícola

- **Idade:** 34 anos
- **Contexto:** Técnica de campo que assessora 8 produtores na região. Visita cada um a cada 15–30 dias.
- **Objetivos:** Acompanhar o histórico de cada propriedade entre visitas e orientar os produtores com dados concretos.
- **Dificuldades:** Cada produtor guarda informações de jeito diferente; difícil saber o que aconteceu desde a última visita.

#### Persona 3 — Pedro, o Produtor Iniciante

- **Idade:** 28 anos
- **Contexto:** Herdou 5 ha do pai e está começando na bananicultura. Tem bom domínio de celular e internet.
- **Objetivos:** Aprender a gestionar a propriedade e evitar os erros mais comuns.
- **Dificuldades:** Não tem experiência agronômica; não sabe reconhecer pragas nem quando intervir.

---

### 2.2 Casos de Uso Principais

1. **Autenticação:** Cadastro, login, logout e recuperação de senha por e-mail com token temporário.
2. **Gestão de Propriedades:** Cadastrar, editar e remover propriedades com nome, localização e área total.
3. **Gestão de Talhões:** Cadastrar talhões vinculados a uma propriedade, com área, variedades, data de plantio.
4. **Registro de Manejos:** Registrar atividades de campo por talhão (tipo de manejo, data, descrição).
5. **Registro de Ocorrências:** Registrar pragas e doenças com tipo, severidade (Leve/Moderada/Grave), área afetada e tratamento.
6. **Registro de Colheitas:** Registrar colheitas com data, quantidade de caixas, peso e valor recebido.
7. **Registro de Custos:** Registrar custos por categoria (insumos, mão de obra, equipamentos etc.).
8. **Consultar Dashboard:** Visualizar indicadores consolidados, alertas ativos e diagnóstico situacional da propriedade.
9. **Consultar Diagnóstico:** Ver classificação de cada talhão (Normal/Atenção/Crítico) com motivos detalhados.
10. **Consultar Recomendações:** Ver lista priorizada de ações recomendadas com base nos dados registrados.
11. **Gerar Relatórios:** Acessar relatório completo por talhão com histórico, indicadores e gráficos.

---

### 2.3 Requisitos Funcionais (RF)

| ID | Descrição |
|---|---|
| RF01 | O sistema deve permitir que o usuário crie uma conta com nome, e-mail e senha. |
| RF02 | O sistema deve permitir que o usuário realize login com e-mail e senha. |
| RF03 | O sistema deve permitir que o usuário recupere a senha via link enviado por e-mail. |
| RF04 | O sistema deve permitir que o usuário cadastre uma ou mais propriedades com nome, localização e área total. |
| RF05 | O sistema deve permitir que o usuário cadastre talhões por propriedade, informando área, variedade(s) e data de plantio. |
| RF06 | O sistema deve permitir que o usuário registre manejos por talhão com data e tipo de atividade. |
| RF07 | O sistema deve permitir que o usuário registre ocorrências de pragas e doenças por talhão com tipo, nome, severidade, área afetada e tratamento. |
| RF08 | O sistema deve permitir que o usuário registre colheitas por talhão com data, quantidade de caixas, peso total e valor recebido. |
| RF09 | O sistema deve permitir que o usuário registre custos por talhão com data, categoria e valor. |
| RF10 | O sistema deve calcular automaticamente indicadores por talhão: produtividade (cx/ha e kg/ha), custo/ha, custo/caixa e lucro estimado. |
| RF11 | O sistema deve gerar alertas automáticos com base em 8 regras agronômicas definidas. |
| RF12 | O sistema deve classificar cada talhão com diagnóstico situacional (Normal, Atenção ou Crítico) com justificativas. |
| RF13 | O sistema deve gerar recomendações acionáveis priorizadas (urgente, alta, média) para cada talhão. |
| RF14 | O sistema deve exibir um dashboard com visão consolidada de indicadores, alertas e diagnóstico da propriedade. |
| RF15 | O sistema deve exibir recomendações de tratamento por praga/doença e severidade ao registrar uma ocorrência. |
| RF16 | O sistema deve permitir que o usuário visualize histórico de produção e custos por mês em formato gráfico. |
| RF17 | O sistema deve exibir ranking dos talhões por produtividade e ranking das pragas mais recorrentes. |

---

### 2.4 Requisitos Não Funcionais (RNF)

| ID | Descrição |
|---|---|
| RNF01 | O sistema deve responder às requisições em menos de 500 ms em condições normais de carga. |
| RNF02 | O sistema deve utilizar hash de senha com salt via Werkzeug (PBKDF2-SHA256) — nunca armazenar senhas em texto plano. |
| RNF03 | O sistema deve proteger todas as rotas autenticadas com verificação de sessão via Flask-Login. |
| RNF04 | Tokens de recuperação de senha devem ter expiração configurável (padrão: 1 hora). |
| RNF05 | O sistema deve ser responsivo e funcional em telas de desktop, tablet e smartphone. |
| RNF06 | O sistema deve isolar os dados por usuário — um usuário não pode acessar propriedades de outro. |
| RNF07 | O banco de dados deve ser gerenciado via migrations (Flask-Migrate/Alembic) para evolução controlada do schema. |
| RNF08 | O sistema deve utilizar o padrão MVC com separação clara entre modelos, rotas e templates. |

---

### 2.5 Regras de Negócio

| ID | Regra |
|---|---|
| RN01 | Somente usuários autenticados podem acessar qualquer módulo além do login e cadastro. |
| RN02 | Um usuário só pode visualizar e editar propriedades vinculadas à sua conta. |
| RN03 | Talhões só podem existir vinculados a uma propriedade. Ao excluir uma propriedade, todos os seus talhões e registros são excluídos em cascata. |
| RN04 | A classificação diagnóstica usa sistema de pontuação ponderada: produtividade crítica (+2 pts), custo alto (+2 pts), ocorrência grave (+2 pts), prejuízo (+2 pts); pontuação ≥ 4 = Crítico, ≥ 2 = Atenção, < 2 = Normal. |
| RN05 | Um talhão é alertado como "sem manejo" após 30 dias (atenção) ou 60 dias (crítico) sem registro. |
| RN06 | A previsão de colheita é gerada automaticamente quando se passam 270 dias (9 meses) desde a última colheita registrada. |
| RN07 | Alta incidência de pragas é configurada como ≥ 3 ocorrências nos últimos 30 dias. |
| RN08 | Queda de produtividade é alertada quando a última colheita está abaixo de 80% da média das colheitas anteriores. |

---

### 2.6 Fora do Escopo

- Integração com sensores IoT ou estações meteorológicas.
- Módulo de comunicação entre produtores ou marketplace.
- Aplicativo nativo para iOS ou Android (apenas web responsiva).
- Integração com ERPs externos ou sistemas de notas fiscais.
- Georreferenciamento e mapas de talhões.
- Módulo de compras de insumos ou negociação de preços.
- Inteligência Artificial preditiva (o sistema usa regras explícitas, não modelos de ML).

---

## 3. Fluxos e Comportamento do Sistema

### 3.1 Fluxo Principal do Usuário

```
[Acesso] → [Login / Cadastro]
              ↓
         [Dashboard da Propriedade]
              ↓
    ┌─────────────────────────────┐
    │   Alertas Ativos            │
    │   Diagnóstico por Talhão    │
    │   Indicadores Consolidados  │
    └─────────────────────────────┘
              ↓
    [Selecionar Talhão]
              ↓
    ┌──────────────────────────────────────┐
    │  Registrar Manejo                    │
    │  Registrar Ocorrência (+ Recomend.)  │
    │  Registrar Colheita                  │
    │  Registrar Custo                     │
    └──────────────────────────────────────┘
              ↓
    [Atualização Automática de Indicadores]
              ↓
    [Novo Diagnóstico e Alertas Calculados]
```

O fluxo principal parte do login, leva ao dashboard da propriedade — que já apresenta o estado atual com alertas e diagnósticos — e permite navegar para qualquer talhão para registrar dados ou consultar o histórico.

### 3.2 Fluxos Alternativos

**Recuperação de Senha:**
```
[Login] → [Esqueci minha senha]
               ↓
         [Informa e-mail]
               ↓
         [Token enviado por e-mail (validade: 1h)]
               ↓
         [Acessa link] → [Nova Senha]
               ↓
         [Redireciona para Login]
```

**Ocorrência com Recomendação:**
```
[Registrar Ocorrência]
         ↓
[Sistema identifica praga/doença e severidade]
         ↓
[Exibe automaticamente recomendações de tratamento]
         ↓
[Produtor consulta e registra o tratamento aplicado]
```

**Alerta Crítico:**
```
[Dados registrados disparam regra agronômica]
         ↓
[Alerta do tipo "danger" gerado para o talhão]
         ↓
[Aparece em destaque no Dashboard]
         ↓
[Recomendação de prioridade "urgente" gerada]
```

---

## 4. Mockups e Experiência do Usuário (UX)

### 4.1 Fluxo de Navegação

```
[Login]
   └─→ [Dashboard da Propriedade]
             ├─→ [Lista de Propriedades] → [Nova Propriedade]
             ├─→ [Talhão: Detalhe]
             │       ├─→ [Manejos] → [Novo Manejo]
             │       ├─→ [Ocorrências] → [Nova Ocorrência + Recomendações]
             │       ├─→ [Colheitas] → [Nova Colheita]
             │       ├─→ [Custos] → [Novo Custo]
             │       └─→ [Diagnóstico do Talhão]
             ├─→ [Relatórios]
             └─→ [Configurações da Conta]
```

### 4.2 Wireframes das Telas Principais

#### Tela 1 — Dashboard da Propriedade

```
┌──────────────────────────────────────────────────────────┐
│  AgroBanana          [Propriedade: Fazenda Esperança ▼]  │
├──────────────────────────────────────────────────────────┤
│  ALERTAS ATIVOS                                          │
│  ⚠️  Talhão A — sem manejo há 45 dias        [warning]  │
│  🐛  Talhão B — 4 ocorrências em 30 dias     [danger]   │
│  📉  Talhão C — queda de 25% na produção     [warning]  │
├──────────────────────────────────────────────────────────┤
│  INDICADORES DA PROPRIEDADE                              │
│  Total Caixas: 1.240 cx   Receita: R$ 18.600            │
│  Custo Total: R$ 12.800   Lucro: R$ 5.800               │
│  Produtividade média: 147 cx/ha                         │
├──────────────────────────────────────────────────────────┤
│  DIAGNÓSTICO POR TALHÃO                                  │
│  ● Talhão A  [Atenção]   │  ● Talhão D  [Normal]       │
│  ● Talhão B  [Crítico]   │  ● Talhão E  [Normal]       │
│  ● Talhão C  [Atenção]   │                              │
├──────────────────────────────────────────────────────────┤
│  RECOMENDAÇÕES PRIORIZADAS                               │
│  🔴 URGENTE: Intervenção no Talhão B — situação crítica │
│  🟠 ALTA: Realizar manejo no Talhão A (45 dias sem)     │
│  🟡 MÉDIA: Monitorar pragas no Talhão C                 │
└──────────────────────────────────────────────────────────┘
```

#### Tela 2 — Detalhe do Talhão

```
┌────────────────────────────────────────────────────────┐
│  Talhão B — Setor Norte    [Atenção ⚠️]   [Editar]    │
│  Área: 3,5 ha | Variedade: Nanica | Plantio: 03/2024  │
├────────────────────────────────────────────────────────┤
│  INDICADORES DO TALHÃO                                 │
│  Produtividade: 98 cx/ha   Custo/caixa: R$ 14,20      │
│  Receita: R$ 6.200         Custo: R$ 5.800             │
│  Lucro estimado: R$ 400    Colheitas: 3                │
├──────────┬───────────┬─────────────┬──────────────────┤
│  Manejos │ Ocorrênc. │  Colheitas  │  Custos          │
│  [+ Novo]│  [+ Nova] │  [+ Nova]   │  [+ Novo]        │
├──────────┴───────────┴─────────────┴──────────────────┤
│  DIAGNÓSTICO DETALHADO                                 │
│  ✅ Custo por caixa adequado: R$ 14,20                 │
│  ⚠️  Produtividade intermediária: 98 cx/ha             │
│  ❌ 4 ocorrências de pragas nos últimos 30 dias        │
│  ⚠️  Sem manejo há 45 dias                            │
├────────────────────────────────────────────────────────┤
│  HISTÓRICO (gráfico de barras)                         │
│  Produção mensal ▓▓▓▒▒▓▓▒                             │
│  Custos mensais  ▒▒▒▒▒▒▓▒                             │
└────────────────────────────────────────────────────────┘
```

#### Tela 3 — Registro de Ocorrência (com Recomendações)

```
┌────────────────────────────────────────────────────────┐
│  Nova Ocorrência — Talhão B                            │
├────────────────────────────────────────────────────────┤
│  Tipo:        [Doença ▼]                               │
│  Nome:        [Sigatoka-negra ▼]                       │
│  Data:        [____/____/______]                       │
│  Severidade:  [Leve] [Moderada ●] [Grave]              │
│  Área afetada: [____] ha                               │
│  Tratamento aplicado: [__________________________]     │
├────────────────────────────────────────────────────────┤
│  💡 RECOMENDAÇÕES PARA SIGATOKA-NEGRA — MODERADA       │
│  Agente: Fungo Mycosphaerella fijiensis                │
│  • Aplicar fungicida sistêmico (propiconazol) em       │
│    alternância com protetores.                         │
│  • Realizar desfolha completa das folhas muito afet.   │
│  • Melhorar drenagem e espaçamento entre plantas.      │
│  • Reavaliar em 15 dias e repetir se necessário.       │
├────────────────────────────────────────────────────────┤
│                    [Cancelar]  [Salvar Ocorrência]     │
└────────────────────────────────────────────────────────┘
```

### 4.3 Fluxo de Interação — Registro de Colheita

1. Usuário acessa o talhão desejado no dashboard.
2. Clica em "Nova Colheita" na aba de colheitas.
3. Preenche: data, quantidade de caixas, peso estimado por caixa e valor recebido por caixa.
4. Salva. O sistema recalcula automaticamente: receita total, produtividade (cx/ha), custo/caixa e lucro estimado.
5. O diagnóstico e os alertas são atualizados imediatamente na próxima visualização do dashboard.

---

## 5. Arquitetura do Sistema

### 5.1 Diagrama C4

#### Nível 1 — Contexto

```
                        ┌─────────────────────────┐
                        │                         │
   [Produtor Rural] ───▶│      AgroBanana          │◀─── [Técnico Agrícola]
                        │  (Sistema Web de Apoio  │
   [Engenheiro       ──▶│   à Decisão)            │
    Agrônomo]           │                         │
                        └────────────┬────────────┘
                                     │
                              ┌──────▼──────┐
                              │  Servidor   │
                              │  de E-mail  │
                              │  (SMTP)     │
                              └─────────────┘
```

O AgroBanana é um sistema web acessado por navegador. Interage com um servidor de e-mail externo apenas para envio de tokens de recuperação de senha. Não há integrações com sistemas externos além disso.

#### Nível 2 — Containers

```
┌──────────────────────────────────────────────────────────────┐
│                        AgroBanana                            │
│                                                              │
│   [Navegador Web]                                            │
│   HTML + Jinja2 + Bootstrap 5 + Chart.js                     │
│          │ HTTP/HTTPS                                         │
│          ▼                                                    │
│   [Aplicação Flask (Python)]                                 │
│   Rotas MVC / Services / Models                              │
│          │ SQLAlchemy ORM                                     │
│          ▼                                                    │
│   [Banco de Dados SQLite / PostgreSQL]                       │
│   Esquema relacional gerenciado por Alembic Migrations        │
│                                                              │
│          │ Flask-Mail + SMTP                                  │
│          ▼                                                    │
│   [Servidor SMTP Externo]                                    │
│   Envio de e-mails (reset de senha)                          │
└──────────────────────────────────────────────────────────────┘
```

#### Nível 3 — Componentes (Aplicação Flask)

```
app/
├── routes/          ← Controllers (HTTP handlers)
│   ├── auth.py         Login, cadastro, reset de senha
│   ├── propriedades.py CRUD de propriedades
│   ├── talhoes.py      CRUD de talhões e variedades
│   ├── manejos.py      CRUD de manejos
│   ├── ocorrencias.py  CRUD de ocorrências + recomendações
│   ├── colheitas.py    CRUD de colheitas
│   ├── custos.py       CRUD de custos
│   ├── dashboard.py    Dashboard consolidado
│   └── relatorios.py   Relatórios por talhão
│
├── models/          ← Entidades ORM (SQLAlchemy)
│   ├── usuario.py      Autenticação, hash de senha, token reset
│   ├── propriedade.py  Dados da propriedade rural
│   ├── talhao.py       Talhão com variedades múltiplas
│   ├── manejo.py       Registro de manejos
│   ├── ocorrencia.py   Pragas/doenças com recomendações embutidas
│   ├── colheita.py     Colheitas e receita
│   └── custo.py        Custos por categoria
│
└── services/        ← Regras de negócio e lógica agronômica
    ├── indicadores.py  Cálculo de KPIs por talhão e propriedade
    ├── alertas.py      Engine de alertas (8 regras)
    └── diagnostico.py  Classificação situacional + recomendações
```

---

### 5.2 Modelo de Dados

#### Esquema Relacional

```
usuarios
  id (PK)
  nome
  email (unique)
  senha_hash
  created_at

propriedades
  id (PK)
  usuario_id (FK → usuarios.id)
  nome
  localizacao
  area_total_ha
  produtor_nome
  created_at

talhoes
  id (PK)
  propriedade_id (FK → propriedades.id)
  nome
  area_ha
  data_plantio
  created_at

talhao_variedades
  id (PK)
  talhao_id (FK → talhoes.id)
  variedade

manejos
  id (PK)
  talhao_id (FK → talhoes.id)
  tipo_manejo
  data_manejo
  descricao
  created_at

ocorrencias
  id (PK)
  talhao_id (FK → talhoes.id)
  tipo             (Praga | Doença)
  nome
  data_ocorrencia
  severidade       (Leve | Moderada | Grave)
  area_afetada_ha
  tratamento_aplicado
  created_at

colheitas
  id (PK)
  talhao_id (FK → talhoes.id)
  data_colheita
  quantidade_caixas
  peso_por_caixa_kg
  valor_caixa
  created_at
  [peso_total: calculado]
  [receita_total: calculada]

custos
  id (PK)
  talhao_id (FK → talhoes.id)
  data_custo
  categoria
  descricao
  valor
  created_at
```

**Relações de exclusão em cascata:**
`propriedade → talhoes → (manejos, ocorrencias, colheitas, custos, talhao_variedades)`

---

### 5.3 Principais Componentes

| Componente | Responsabilidade |
|---|---|
| **Engine de Alertas** (`services/alertas.py`) | Avalia 8 regras agronômicas sobre os dados de cada talhão e gera alertas classificados por severidade (danger/warning/info). |
| **Engine de Diagnóstico** (`services/diagnostico.py`) | Sistema de pontuação ponderada que classifica talhões em Normal, Atenção ou Crítico com motivos e recomendações priorizadas. |
| **Módulo de Indicadores** (`services/indicadores.py`) | Calcula todos os KPIs econômicos e agronômicos a partir dos dados brutos: produtividade, custo/caixa, lucro, histórico mensal, ranking de talhões. |
| **Base de Recomendações** (`models/ocorrencia.py`) | Dicionário técnico com recomendações de tratamento para 10 pragas/doenças, em 3 níveis de severidade, baseado em literatura agronômica. |
| **Autenticação** (`models/usuario.py`, `routes/auth.py`) | Login com hash seguro, sessão via Flask-Login e recuperação de senha com token temporário assinado. |

---

### 5.4 Stack Tecnológica

| Tecnologia | Versão | Justificativa |
|---|---|---|
| **Python** | 3.10+ | Linguagem principal com ampla biblioteca para aplicações web e processamento de dados. |
| **Flask** | 3.x | Microframework leve, ideal para projetos acadêmicos com controle total da estrutura. Curva de aprendizado adequada ao TCC. |
| **SQLAlchemy** | 2.x | ORM maduro que abstrai o banco de dados e permite migrar de SQLite (desenvolvimento) para PostgreSQL (produção) sem alteração de código. |
| **Flask-Migrate (Alembic)** | 4.x | Gerencia evoluções do schema de forma controlada e rastreável via migrations. |
| **Flask-Login** | 0.6+ | Gerência de sessão e proteção de rotas autenticadas de forma simples e segura. |
| **Werkzeug** | 3.x | Hash de senha com PBKDF2-SHA256 e salt — padrão de segurança recomendado. |
| **itsdangerous** | 2.x | Geração e validação de tokens assinados com expiração para reset de senha. |
| **Jinja2** | 3.x | Sistema de templates integrado ao Flask, permite renderização server-side sem dependência de frameworks JavaScript. |
| **Bootstrap 5** | 5.3 | Framework CSS responsivo com componentes prontos (alertas, badges, cards) que aceleram o desenvolvimento da interface. |
| **Chart.js** | 4.x | Biblioteca JavaScript para gráficos de histórico de produção e custos. |
| **SQLite** | built-in | Banco de dados para desenvolvimento. Sem dependência de infraestrutura adicional. |

---

## 6. Segurança e Privacidade

### 6.1 Proteções Implementadas

| Ameaça (OWASP) | Medida Adotada |
|---|---|
| **Injeção (A01)** | Todas as queries usam SQLAlchemy ORM com parâmetros vinculados — sem SQL dinâmico. |
| **Autenticação Quebrada (A07)** | Hash de senha com PBKDF2-SHA256 + salt via Werkzeug. Tokens de reset com expiração de 1 hora. |
| **Controle de Acesso (A01)** | Decorator `@login_required` em todas as rotas protegidas. Verificação de propriedade por `usuario_id` em cada query. |
| **XSS (A03)** | Jinja2 escapa automaticamente a saída de variáveis em templates. |
| **CSRF** | Flask-WTF com validação de token CSRF nos formulários. |
| **Exposição de Dados** | Senhas nunca armazenadas em texto plano. Tokens de reset não são reutilizáveis. |

### 6.2 Privacidade e LGPD

**Dados coletados:**
- Nome e e-mail do usuário (obrigatórios para autenticação).
- Dados operacionais da propriedade (inseridos voluntariamente pelo produtor).

**Armazenamento:**
- Dados armazenados em banco de dados local (SQLite em desenvolvimento, PostgreSQL em produção).
- Senhas armazenadas apenas como hash irreversível.

**Direitos do titular:**
- O usuário pode excluir sua conta e todos os dados associados a qualquer momento.
- Exclusão em cascata garante que ao remover propriedades, todos os dados vinculados são removidos.

**Compartilhamento:**
- Nenhum dado é compartilhado com terceiros.
- O único sistema externo é o servidor SMTP para envio do link de reset de senha.

---

## 7. Planejamento do Projeto

| Marco | Descrição | Status |
|---|---|---|
| M1 | Setup do ambiente, modelagem do banco de dados, estrutura Flask inicial | Concluído |
| M2 | Módulos de autenticação (login, cadastro, reset de senha) | Concluído |
| M3 | CRUD de propriedades e talhões com suporte a múltiplas variedades | Concluído |
| M4 | Módulos de registro: manejos, ocorrências, colheitas, custos | Concluído |
| M5 | Engine de indicadores (produtividade, custo/caixa, lucro estimado) | Concluído |
| M6 | Engine de alertas com 8 regras agronômicas | Concluído |
| M7 | Sistema de diagnóstico situacional e recomendações priorizadas | Concluído |
| M8 | Base de recomendações técnicas por praga/doença e severidade | Concluído |
| M9 | Dashboard consolidado e relatórios por talhão | Concluído |
| M10 | Testes, refinamentos de UX, documentação e entrega do TCC | Em andamento |

---

## 8. Referências

1. IBGE. *Produção Agrícola Municipal (PAM) 2022*. Instituto Brasileiro de Geografia e Estatística, 2022.
2. EMBRAPA Mandioca e Fruticultura. *A cultura da bananeira*. Cruz das Almas, BA: Embrapa, 2021.
3. GASPAROTTO, L.; PEREIRA, J. C. R. (Eds.). *Doenças da bananeira*. Brasília: Embrapa, 2006.
4. Flask Documentation. *Welcome to Flask*. Disponível em: https://flask.palletsprojects.com/
5. SQLAlchemy Documentation. *SQLAlchemy ORM*. Disponível em: https://docs.sqlalchemy.org/
6. OWASP Foundation. *OWASP Top Ten*. Disponível em: https://owasp.org/www-project-top-ten/
7. Brasil. *Lei Geral de Proteção de Dados Pessoais — Lei nº 13.709/2018 (LGPD)*. Brasília, 2018.
8. Brasil. *Política Nacional de Agricultura Digital — Decreto nº 10.329/2020*. Brasília, 2020.
9. Bootstrap. *Bootstrap 5 Documentation*. Disponível em: https://getbootstrap.com/docs/5.3/
10. Chart.js. *Chart.js Documentation*. Disponível em: https://www.chartjs.org/docs/

---

## 9. Apêndices

### Apêndice A — Regras de Alerta Implementadas

| # | Regra | Tipo | Condição |
|---|---|---|---|
| 1 | Manejo atrasado | warning | Sem manejo há mais de 30 dias |
| 2 | Manejo crítico | danger | Sem manejo há mais de 60 dias |
| 3 | Alta incidência de pragas | danger | ≥ 3 ocorrências nos últimos 30 dias |
| 4 | Ocorrência grave recente | danger | Ocorrência "Grave" nos últimos 60 dias |
| 5 | Custo elevado | warning | Custo total > R$ 5.000 |
| 6 | Reincidência de praga/doença | info | Mesmo agente ocorreu > 1 vez |
| 7 | Colheita prevista | info | ≥ 270 dias desde a última colheita |
| 8 | Prejuízo estimado | danger | Receita < Custo total |
| 9 | Queda de produtividade | warning | Última colheita < 80% da média anterior |

### Apêndice B — Pragas e Doenças com Base de Recomendações

| # | Nome | Tipo | Agente |
|---|---|---|---|
| 1 | Sigatoka-negra | Doença | Mycosphaerella fijiensis |
| 2 | Sigatoka-amarela | Doença | Mycosphaerella musicola |
| 3 | Mal-do-Panamá | Doença | Fusarium oxysporum f. sp. cubense |
| 4 | Moko | Doença | Ralstonia solanacearum (Raça 2) |
| 5 | Broca-do-rizoma | Praga | Cosmopolites sordidus |
| 6 | Trips | Praga | Frankliniella parvula |
| 7 | Pulgão | Praga | Pentalonia nigronervosa |
| 8 | Ácaro | Praga | Tetranychus urticae / Aceria guerreronis |
| 9 | Nematoides | Praga | Radopholus similis / Meloidogyne spp. |
| 10 | Antracnose | Doença | Colletotrichum musae |

### Apêndice C — Variedades Suportadas

Prata, Prata-Anã, Pacovan, Nanica, Nanicão, Grand Naine, Cavendish, Banana Maçã, Banana Figo, Banana D'Angola, Banana Terra, BRS Platina, FHIA-18, Tropical, Garantida, Outras.

### Apêndice D — Repositório do Projeto

O código-fonte está disponível no repositório GitHub do projeto (acesso privado durante desenvolvimento do TCC).
