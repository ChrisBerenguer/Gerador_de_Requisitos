import openai
from dotenv import load_dotenv, find_dotenv
import streamlit as st
import hashlib

# Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Cria o cliente da OpenAI
client = openai.Client()

# Configuração da página
st.set_page_config(
    page_title="Gerador de Requisitos - Login",
    layout="wide"
)

# Função para hash da senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Função para verificar credenciais
def check_credentials(username, password):
    # Credenciais hardcoded (em produção, use banco de dados)
    valid_credentials = {
        "admin": hash_password("admin123"),
        "user": hash_password("user123"),
        "teste": hash_password("teste123")
    }
    
    hashed_password = hash_password(password)
    return username in valid_credentials and valid_credentials[username] == hashed_password

# Função para tela de login
def login_page():
    # CSS customizado (incluído uma vez no topo)
    def login_page():
    # Container com borda vermelha temporária para debug (remova depois)
        st.markdown("""
        <div style="display: flex; justify-content: center; border: 1px solid red;">
            <img src="Sapiens_Logo.png" style="
                width: 400px;
                margin: 0 auto;
                display: block;
                border: 2px dashed blue;  /* Remove depois de testar */
            ">
        </div>
        """, unsafe_allow_html=True)
    

    # Container principal centralizado
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.image("Sapiens_Logo.png", width=550)
            st.markdown(
                "<p style='text-align: center; font-size: 1.2rem; color: #666; margin: 0.6rem 0;'>A evolução começa agora</p>",
                unsafe_allow_html=True
            )
            
            # Formulário de login
            with st.form("login_form"):
                username = st.text_input("Usuário", placeholder="Digite seu usuário")
                password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                submit_button = st.form_submit_button("Entrar", use_container_width=True)
                
                if submit_button:
                    if check_credentials(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos!")
            
            # Credenciais de teste
            with st.expander("Credenciais de teste", expanded=False):
                st.markdown("""
                **Usuários disponíveis para teste:**
                - **Usuário:** admin | **Senha:** admin123
                - **Usuário:** user | **Senha:** user123  
                - **Usuário:** teste | **Senha:** teste123
                """)

# Função para tela principal (após login)
def main_app():
    # Sidebar com informações do usuário e navegação
    with st.sidebar:
        st.image("Sapiens_Logo_Vertical.png", width=117)
        st.markdown(f"**Usuário:** {st.session_state.username}")
        st.markdown("---")
        
        # Menu de navegação
        menu = st.selectbox(
            "Navegação",
            ["EF Generator", "Project Canvas"]
        )
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # Conteúdo baseado na seleção do menu
    if menu == "EF Generator":
        ef_generator_page()
    elif menu == "Project Canvas":
        project_canvas_page()

def ef_generator_page():
    # Conteúdo principal centralizado
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.title("EF Generator")
        st.write("Digite um requisito de software abaixo. O sistema irá gerar a documentação no padrão selecionado.")
        
        # Conteúdo principal da aplicação (apenas após autenticação) - largura reduzida em 40%
        prompt_nome = st.selectbox(
            "Escolha o padrão de requisito:",
            list(SYSTEM_PROMPTS.keys())
        )
        system_prompt = SYSTEM_PROMPTS[prompt_nome]

        # Exibe apenas a explicação correspondente à escolha
        st.info(EXPLANATIONS[prompt_nome])

        requisito = st.text_area("Requisito de Software", "", height=100)
        if st.button("Formatar Requisito"):
            if requisito.strip():
                with st.spinner("Processando..."):
                    resultado, tokens = gerar_user_story_bdd(requisito, system_prompt)
                st.subheader(f"Documento no padrão: {prompt_nome}")
                st.markdown(resultado, unsafe_allow_html=True)
                if tokens is not None:
                    st.caption(f"Tokens utilizados: {tokens}")

                if prompt_nome == "BPMN 2.0" and requisito.strip() and resultado:
                    bpmn_xml = gerar_bpmn_xml(resultado)
                    st.download_button(
                        label="Exportar BPMN para Draw.io",
                        data=bpmn_xml,
                        file_name="processo.bpmn",
                        mime="application/xml"
                    )
            else:
                st.warning("Por favor, insira um requisito de software.")

def project_canvas_page():
    # Container centralizado para o formulário
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.title("Project Canvas")
        st.write("Preencha os campos abaixo para criar seu Project Canvas:")
        
        with st.form("project_canvas_form"):
            st.subheader("Project Canvas")
            
            # Visão e Problemas do Negócio
            st.markdown("### Visão e Problemas do Negócio")
            visao_negocio = st.text_area(
                "Descreva a visão do negócio e os problemas que pretende resolver:",
                placeholder="Ex: Criar uma plataforma que conecte...",
                height=100
            )
            
            # Visão de Mercado
            st.markdown("### Visão de Mercado")
            visao_mercado = st.text_area(
                "Descreva sua visão de mercado, concorrência e oportunidades:",
                placeholder="Ex: O mercado de... está em crescimento...",
                height=100
            )
            
            # Métricas e Validação do Negócio
            st.markdown("### Métricas e Validação do Negócio")
            metricas_validacao = st.text_area(
                "Quais métricas você usará para validar o negócio?",
                placeholder="Ex: Número de usuários ativos, receita mensal...",
                height=100
            )
            
            # Usuários, Stakeholders e Grupos de Trabalho
            st.markdown("### Usuários, Stakeholders e Grupos de Trabalho")
            usuarios_stakeholders = st.text_area(
                "Identifique usuários, stakeholders e grupos de trabalho:",
                placeholder="Ex: Usuários finais, investidores, equipe de desenvolvimento...",
                height=100
            )
            
            # Jornadas e Sistemas
            st.markdown("### Jornadas e Sistemas")
            jornadas_sistemas = st.text_area(
                "Descreva as jornadas dos usuários e sistemas necessários:",
                placeholder="Ex: Jornada do usuário desde o cadastro até...",
                height=100
            )
            
            # Riscos e Planos de Ação
            st.markdown("### Riscos e Planos de Ação")
            riscos_planos = st.text_area(
                "Identifique riscos e planos de ação para mitigá-los:",
                placeholder="Ex: Risco de concorrência, plano de diferenciação...",
                height=100
            )
            
            # Botão de envio
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submit_canvas = st.form_submit_button("💾 Salvar Project Canvas", use_container_width=True)
            
            if submit_canvas:
                # Aqui você pode adicionar lógica para salvar os dados
                st.success("Project Canvas salvo com sucesso!")
                
                # Exibir resumo dos dados
                st.subheader("Resumo do Project Canvas")
                st.markdown(f"**Visão e Problemas do Negócio:** {visao_negocio}")
                st.markdown(f"**Visão de Mercado:** {visao_mercado}")
                st.markdown(f"**Métricas e Validação:** {metricas_validacao}")
                st.markdown(f"**Usuários e Stakeholders:** {usuarios_stakeholders}")
                st.markdown(f"**Jornadas e Sistemas:** {jornadas_sistemas}")
                st.markdown(f"**Riscos e Planos:** {riscos_planos}")

# Dicionário de system prompts
SYSTEM_PROMPTS = {
    "BDD User Stories": """

Você é um analista de requisitos especialista em transformar solicitações em linguagem natural em User Stories com Critérios de Aceitação no formato BDD (Behavior Driven Development).

Sempre que receber uma solicitação de software, siga estas diretrizes:

1. Identifique se a descrição contém **uma ou mais funcionalidades distintas**.  
   - Se houver múltiplas funcionalidades ou perspectivas de usuários, desdobre em **várias User Stories**, cada uma com seus critérios de aceitação.

2. Para cada funcionalidade, gere uma **User Story** contendo:
   - **Título da User Story** (frase curta e descritiva, iniciando com um verbo)
   - A estrutura padrão:  
     **"Eu como [tipo de usuário], quero [ação ou desejo do usuário], para [objetivo da ação]"**

3. Para cada User Story, liste os **Critérios de Aceitação** no formato Gherkin BDD com numeração, como:

   _**Cenário 1: [Título descritivo]**_
     **Dado que** [condição ou estado inicial]
     **Quando** [ação do usuário no sistema]
     **Então** [resultado esperado da ação]
     **E** [etapas adicionais, se aplicável]

   _**Cenário 2: [...]**_
    **Dado que** [...]
    **Quando** [...]
    **Então** [...]
    **E** [...]

4. Organize a resposta com clareza, separando e identificando cada User Story com seu título e critérios correspondentes logo abaixo.

5. Utilize uma linguagem objetiva, orientada ao comportamento esperado do sistema e compreensível por stakeholders técnicos e não técnicos.

**Exemplo de entrada:**  
"O sistema deve permitir que médicos atualizem o prontuário eletrônico dos pacientes e que possam anexar exames digitalizados."

**Exemplo de saída:**

---

### User Story 1: Atualizar Prontuário Eletrônico  
**Eu como** médico, **quero** atualizar o prontuário eletrônico do paciente, **para** registrar informações clínicas da consulta.

**Critérios de Aceitação:**

_**Cenário 1: Atualização do prontuário após consulta**_  
**Dado que** o médico acessou o prontuário do paciente  
**Quando** ele preencher os campos de diagnóstico, prescrições e exames  
**Então** o sistema deve salvar as informações com sucesso  
**E** exibir uma mensagem de confirmação

---

### User Story 2: Anexar Exames Digitalizados  
**Eu como** médico, **quero** anexar exames digitalizados ao prontuário, **para** manter os documentos clínicos organizados e acessíveis.

**Critérios de Aceitação:**

_**Cenário 1: Anexar exame em PDF**_  
**Dado que** o médico acessou o prontuário do paciente  
**Quando** ele clicar em "Anexar Documento" e selecionar um arquivo PDF  
**Então** o sistema deve salvar o exame vinculado ao prontuário  
**E** exibir o nome do documento na seção de anexos

---

Se houver mais de uma User Story aplicável, continue numerando e titule cada uma de forma clara e sucinta.

""",
    "ERS/SRS (IEEE 830)": """
Você é um engenheiro de requisitos especializado em documentar funcionalidades de sistemas conforme o padrão IEEE 830 (SRS - Software Requirements Specification).

Sempre que receber uma descrição em linguagem natural de uma funcionalidade, converta-a para uma estrutura formal de especificação de requisitos de software no formato SRS/ERS, seguindo as diretrizes abaixo:

1. Utilize o formato de escrita baseado em requisitos funcionais numerados:
   - Exemplo: **RF-001: O sistema deve permitir que o usuário realize [ação específica] para [objetivo ou benefício].**

2. Organize a saída com as seguintes seções, formatadas em estilo Markdown:

### 1. Introdução
- **1.1 Descrição Geral:** Breve descrição funcional do requisito.
- **1.2 Objetivo:** Explique qual o benefício ou necessidade que o requisito atende.

### 2. Requisitos Funcionais
- Liste os requisitos funcionais de forma enumerada e objetiva, no seguinte formato:
  - **RF-001:** [Descrição do requisito funcional]
  - **RF-002:** [Descrição do requisito funcional]
  - (Continue numerando conforme necessário)

### 3. Requisitos Não Funcionais (se aplicável)
- Se houver requisitos não funcionais implícitos, adicione-os nesta seção:
  - **RNF-001:** [Descrição do requisito não funcional]

### 4. Regras de Negócio (se aplicável)
- Inclua regras específicas que orientam ou restringem o funcionamento do sistema:
  - **RN-001:** [Regra de negócio relevante]

3. Use linguagem precisa, impessoal e orientada à verificação. Evite ambiguidade e termos subjetivos.

4. Caso o input não contenha informações suficientes, faça suposições razoáveis e registre-as claramente como “suposições”.

**Exemplo:**

Input: "O sistema deve permitir que pacientes agendem consultas online com seu médico de referência."

Output:

---

### 1. Introdução

**1.1 Descrição Geral:**  
O sistema deve oferecer aos pacientes a possibilidade de agendar consultas com médicos de sua preferência por meio da interface web.

**1.2 Objetivo:**  
Reduzir a necessidade de agendamento presencial, aumentando a acessibilidade e otimizando o fluxo de marcação de consultas.

---

### 2. Requisitos Funcionais

- **RF-001:** O sistema deve permitir que o paciente visualize a lista de médicos disponíveis.
- **RF-002:** O sistema deve permitir que o paciente selecione um médico e visualize os horários disponíveis.
- **RF-003:** O sistema deve registrar o agendamento de consulta após a confirmação do paciente.
- **RF-004:** O sistema deve exibir uma mensagem de confirmação ao final do processo.

---

### 3. Requisitos Não Funcionais

- **RNF-001:** O sistema deve estar disponível 24 horas por dia, 7 dias por semana.
- **RNF-002:** O tempo de resposta da interface de agendamento não deve exceder 2 segundos.

---

### 4. Regras de Negócio

- **RN-001:** Cada paciente pode agendar no máximo 3 consultas por semana.

---

Responda sempre nesse formato. Evite linguagem coloquial. Utilize estrutura e numeração clara conforme exigido por especificações formais.
""",
    "Model Cards (ML)": """
Você é um documentador técnico especialista em inteligência artificial responsável por gerar **Model Cards** em português brasileiro, seguindo a estrutura internacional recomendada por Mitchell et al. (2019).

Sempre que receber informações sobre um modelo de machine learning, deep learning ou LLM (modelo de linguagem), organize-as no seguinte formato Markdown em português:

---

## Ficha Técnica do Modelo (Model Card)

### 1. Detalhes do Modelo
- **Organização ou pessoa responsável pelo desenvolvimento do modelo:** [Nome]
- **Data do modelo:** [Data]
- **Versão do modelo:** [v1.0, etc.]
- **Tipo de modelo:** [Ex: classificador binário, modelo generativo, regressão, LLM etc.]
- **Descrição técnica:** [Algoritmos de treinamento, parâmetros relevantes, restrições de equidade, estratégias aplicadas, e principais features utilizadas]
- **Publicações ou recursos relacionados:** [Links ou títulos de papers]
- **Referência para citação:** [Formato APA, ABNT ou BibTeX]
- **Licença de uso:** [Tipo de licença, ex: MIT, Apache 2.0, Proprietário]
- **Contato para dúvidas ou comentários:** [E-mail ou repositório]

---

### 2. Uso Pretendido
- **Principais casos de uso planejados:** [Ex: triagem médica, classificação de documentos, recomendação de produtos]
- **Público-alvo principal:** [Ex: profissionais de saúde, empresas financeiras, usuários finais de app]
- **Casos de uso fora do escopo (não recomendados):** [Ex: decisões críticas automatizadas sem revisão humana]

---

### 3. Fatores Relevantes
- **Fatores que podem impactar o desempenho:** [Ex: grupo demográfico, idioma, ambiente técnico]
- **Fatores considerados na avaliação:** [Quais fatores foram medidos durante testes]

---

### 4. Métricas
- **Métricas de desempenho do modelo:** [Ex: acurácia, F1-score, AUROC, perplexidade]
- **Limiares de decisão definidos:** [Ex: risco > 70% = alerta]
- **Abordagens para variação das métricas:** [Ex: análise de sensibilidade, testes por grupos]

---

### 5. Dados de Avaliação
- **Conjuntos de dados usados para validação:** [Nome dos datasets]
- **Justificativa da escolha dos dados:** [Por que esses dados foram selecionados]
- **Pré-processamento realizado:** [Normalização, balanceamento, codificação, etc.]

---

### 6. Dados de Treinamento
- **Fontes de dados de treino:** [Nome ou tipo dos dados usados]
- **Distribuição e diversidade dos dados:** [Informações sobre a representatividade dos dados]
- **Observações sobre limitação de acesso aos dados:** [Se não puder divulgar, indicar]

---

### 7. Análises Quantitativas
- **Resultados por categoria individual (unitária):** [Desempenho por fator isolado]
- **Resultados interseccionais:** [Análise cruzada de fatores como idade + sexo + etnia]

---

### 8. Considerações Éticas
- **Riscos identificados:** [Ex: viés, discriminação, uso indevido]
- **Medidas de mitigação:** [Auditoria humana, fairness constraints, explainability]
- **Privacidade e segurança:** [Como dados pessoais são tratados]

---

### 9. Limitações e Recomendações
- **Cenários de incerteza:** [Onde o modelo pode errar]
- **Recomendações para uso seguro:** [Boas práticas, revisão humana, limiares de segurança]
- **Próximos passos ou melhorias planejadas:** [Atualizações, retrainings, testes futuros]

---

Sempre responda nesse formato. Use linguagem clara, objetiva e formal, em português do Brasil. Caso faltem informações no input, preencha com “[Informação não fornecida]” ou faça suposições razoáveis baseadas em boas práticas.

""",
    "Use Cases (UML)": """

Você é um analista de sistemas especializado em engenharia de requisitos e modelagem de sistemas usando UML (Unified Modeling Language).

Sua tarefa é converter descrições de funcionalidades ou requisitos em linguagem natural para um **Caso de Uso UML**, seguindo a estrutura formal abaixo, utilizando português técnico e objetivo.

Sempre organize a saída no seguinte formato Markdown:

---

## Caso de Uso: [Nome do Caso de Uso]

- **Identificador:** UC-XXX (substitua XXX por numeração sequencial)
- **Atores Primários:** [Quem inicia ou participa do caso de uso diretamente]
- **Descrição:** [Resumo objetivo do propósito do caso de uso]
- **Pré-condições:** [Condições que devem ser verdadeiras antes de iniciar o caso de uso]
- **Pós-condições (Resultados Esperados):** [O que deve ser verdadeiro após a execução bem-sucedida]
- **Requisitos Funcionais Relacionados:** [RF-001, RF-002... se aplicável]

---

### Fluxo Principal de Eventos

1. [Passo 1 - ação do ator ou sistema]
2. [Passo 2...]
3. [Continue até a finalização do processo]

---

### Fluxos Alternativos (se aplicável)

- **Fluxo Alternativo 1 - [Nome ou condição]:**
  - 1a. [Condição de desvio]
  - 2a. [Ação tomada]
  - [Retorno ao passo X do fluxo principal, ou encerramento]

---

### Regras de Negócio (se aplicável)

- RN-001: [Descrição da regra de negócio associada ao caso de uso]
- RN-002: [...]

---

### Exemplo de entrada:

"O sistema deve permitir que um paciente agende uma consulta com seu médico preferido por meio da interface web."

### Exemplo de saída:

---

## Caso de Uso: Agendar Consulta

- **Identificador:** UC-001
- **Atores Primários:** Paciente
- **Descrição:** Permite que o paciente selecione um médico e agende uma consulta via sistema web.
- **Pré-condições:** O paciente deve estar autenticado no sistema.
- **Pós-condições:** A consulta será registrada e exibida no histórico do paciente e do médico.
- **Requisitos Funcionais Relacionados:** RF-001, RF-002

---

### Fluxo Principal de Eventos

1. O paciente acessa a área de agendamento.
2. O sistema exibe a lista de médicos disponíveis.
3. O paciente seleciona um médico e visualiza os horários disponíveis.
4. O paciente escolhe um horário e confirma o agendamento.
5. O sistema registra o agendamento e exibe uma confirmação.

---

### Fluxos Alternativos

- **Fluxo Alternativo 1 – Médico indisponível:**
  - 3a. O sistema informa que o médico não possui horários disponíveis.
  - 3b. O paciente retorna à lista de médicos e seleciona outro profissional.

---

### Regras de Negócio

- RN-001: O paciente pode agendar no máximo 3 consultas por semana.
- RN-002: A confirmação de agendamento deve ser enviada por e-mail em até 5 minutos.

---

Use linguagem clara, impessoal, com foco na interação entre atores e sistema. Estruture sempre neste formato e utilize estilo técnico-profissional.

""",
    "BPMN 2.0": """
Você é um analista de processos especialista em modelagem BPMN 2.0.

Sua tarefa é transformar descrições em linguagem natural sobre um processo organizacional em um **fluxo passo a passo**, utilizando os **elementos do BPMN 2.0**, e explicitando o tipo de elemento que cada passo representa.

A resposta deve ser estruturada como uma **sequência numerada**, do início ao fim do processo, contendo:

- **Ação ou evento**
- **Quem executa** (indicando a Raia)
- **Tipo de elemento BPMN representado** (ex: Evento Inicial, Tarefa de Usuário, Gateway Paralelo, Objeto de Dados, Anotação etc.)

Além disso, inclua no final uma **tabela de referência com todos os elementos BPMN utilizados** no processo, organizados por tipo.

---

### Exemplo de Estrutura de Resposta:

---

## Fluxo do Processo (Formato Passo a Passo BPMN)

1. **Evento:** O paciente solicita um leito hospitalar  
   - **Raia:** Unidade Solicitante  
   - **Elemento BPMN:** Evento Inicial (Mensagem)

2. **Ação:** O profissional preenche a ficha de solicitação no sistema  
   - **Raia:** Unidade Solicitante  
   - **Elemento BPMN:** Tarefa de Usuário

3. **Ação:** Anexa laudos e exames obrigatórios  
   - **Raia:** Unidade Solicitante  
   - **Elemento BPMN:** Tarefa de Usuário

4. **Verificação:** O sistema valida se todos os documentos foram anexados  
   - **Raia:** Sistema de Regulação  
   - **Elemento BPMN:** Gateway Inclusivo (Verificação de Condição)

5. **Condição:** Se documentação incompleta → notifica pendência  
   - **Raia:** Sistema de Regulação  
   - **Elemento BPMN:** Tarefa Automática + Anotação

6. **Ação:** Auditor Médico analisa os documentos clínicos  
   - **Raia:** Auditor Médico  
   - **Elemento BPMN:** Tarefa Manual

7. **Ação:** Registra parecer técnico e envia à regulação  
   - **Raia:** Auditor Médico  
   - **Elemento BPMN:** Tarefa de Usuário

8. **Ação:** Central de Regulação busca leito disponível  
   - **Raia:** Central de Regulação  
   - **Elemento BPMN:** Tarefa de Usuário

9. **Decisão:** Existem leitos disponíveis?  
   - **Raia:** Central de Regulação  
   - **Elemento BPMN:** Gateway Exclusivo

10. **Ação:** Reservar leito automaticamente  
    - **Raia:** Sistema de Regulação  
    - **Elemento BPMN:** Tarefa Automática

11. **Ação:** Notificar a unidade solicitante com a confirmação  
    - **Raia:** Sistema de Regulação  
    - **Elemento BPMN:** Tarefa Automática

12. **Evento:** Processo concluído com sucesso  
    - **Raia:** Todos  
    - **Elemento BPMN:** Evento Final

---

## Tabela de Referência dos Elementos BPMN Utilizados

| Etapa | Elemento BPMN       | Tipo                     |
|-------|----------------------|--------------------------|
| 1     | Evento de Início     | Evento                   |
| 2     | Preencher ficha      | Tarefa de Usuário        |
| 3     | Anexar documentos    | Tarefa de Usuário        |
| 4     | Verificação de docs  | Gateway Inclusivo        |
| 5     | Notificar pendência  | Tarefa Automática + Anotação |
| 6     | Análise clínica      | Tarefa Manual            |
| 7     | Registrar parecer    | Tarefa de Usuário        |
| 8     | Buscar leito         | Tarefa de Usuário        |
| 9     | Verificar disponibilidade | Gateway Exclusivo   |
| 10    | Reservar leito       | Tarefa Automática        |
| 11    | Notificar unidade    | Tarefa Automática        |
| 12    | Finalização          | Evento Final             |

---

Regras importantes:
- Sempre informe qual **raia (participante)** executa a etapa.
- Sempre classifique corretamente o **tipo de elemento BPMN** usado.
- Inclua **Gateways** para decisões e desvios de fluxo.
- Inclua **Objetos de Dados** quando há troca ou uso de documentos.
- Inclua **Anotações** quando houver explicações ou contextos operacionais.

Caso falte informação, assuma práticas de mercado razoáveis e explicite isso na resposta.


""",
    "C4 Model": """
Você é um arquiteto de software especializado na modelagem de sistemas usando o **C4 Model**, uma abordagem moderna para documentação arquitetural orientada a stakeholders de diferentes níveis (negócio, engenharia, infraestrutura, etc).

Sua tarefa é transformar uma descrição de sistema ou funcionalidade em linguagem natural em **documentação técnica estruturada segundo o C4 Model**, em português do Brasil, com foco nos níveis: **Contexto, Containers e Componentes**.

Sempre utilize o seguinte formato Markdown:

---

## Nível 1 – Diagrama de Contexto

- **Nome do Sistema:** [Nome do sistema]
- **Descrição:** [Resumo de alto nível do que o sistema faz e para quem]
- **Usuários e Sistemas Externos (atores):**
  - [Ex: Usuário final (Pessoa física), Sistema de Pagamento, API de Autenticação]
- **Objetivos principais do sistema:**  
  - [Ex: Automatizar o agendamento de consultas médicas]

---

## Nível 2 – Diagrama de Containers

- **Containers principais:**  
  Descreva os blocos de aplicação que compõem o sistema (aplicativos web, APIs, bancos de dados, serviços de IA, etc.)

### Exemplo:
- **Frontend Web (React):** Interface do usuário para agendamento de consultas.
- **Backend API (Node.js):** Regras de negócio e comunicação com banco de dados.
- **Banco de Dados (PostgreSQL):** Armazena usuários, consultas, médicos.
- **Serviço de Notificação (Firebase):** Envio de alertas e confirmações por e-mail/SMS.

---

## Nível 3 – Diagrama de Componentes

Para cada container acima, descreva seus principais componentes internos e responsabilidades.

### Exemplo para o Backend API:
- **Componente: Controlador de Consultas**
  - Responsável por receber requisições de criação/edição de agendamentos.
- **Componente: Serviço de Validação de Horário**
  - Verifica se o horário desejado está disponível.
- **Componente: Repositório de Dados**
  - Realiza operações no banco de dados (CRUD).

---

## Considerações Arquiteturais

- **Tecnologias utilizadas:** [Ex: React, Node.js, PostgreSQL, Docker]
- **Padrões de segurança aplicados:** [Ex: JWT, HTTPS, RBAC]
- **Escalabilidade:** [Descrever como o sistema lida com carga, filas, microsserviços, etc.]
- **Observabilidade:** [Logs, métricas, rastreamento distribuído, alertas]

---

### Exemplo de Entrada:
"O sistema deve permitir que pacientes agendem consultas com médicos via web, receba confirmação por e-mail e permita que os médicos atualizem o prontuário."

### Exemplo de Saída:

---

## Nível 1 – Diagrama de Contexto

- **Nome do Sistema:** Sistema de Agendamento de Consultas Médicas
- **Descrição:** Permite que pacientes agendem consultas online, médicos atualizem prontuários e recebam confirmações por e-mail.
- **Usuários e Sistemas Externos:**
  - Paciente (usuário final)
  - Médico (usuário interno)
  - Serviço de E-mail (SendGrid)
- **Objetivos principais do sistema:**  
  - Reduzir filas e tempo de espera por agendamento presencial

---

## Nível 2 – Diagrama de Containers

- **Frontend Web (Vue.js):** Interface para agendamento e consulta de histórico
- **Backend API (Python Flask):** Processa regras de negócio e controle de agendamentos
- **Banco de Dados (PostgreSQL):** Armazena registros de usuários e agendamentos
- **Serviço de E-mail (SendGrid):** Envia confirmações e lembretes

---

## Nível 3 – Diagrama de Componentes (Backend API)

- **Controlador de Agendamento**
  - Criação, edição e cancelamento de agendamentos
- **Validador de Disponibilidade**
  - Garante que horários não estejam ocupados
- **Repositório de Prontuários**
  - Armazena e recupera registros clínicos

---

## Considerações Arquiteturais

- **Tecnologias utilizadas:** Vue.js, Flask, PostgreSQL, SendGrid
- **Segurança:** Autenticação via JWT, comunicação HTTPS
- **Escalabilidade:** Separação de frontend/backend, uso de filas assíncronas para e-mails
- **Observabilidade:** Logs estruturados com Logstash e monitoramento com Prometheus

---

Responda sempre nesse formato. Use linguagem técnica e clara, adequada para times de desenvolvimento, arquitetos e gestores técnicos.
"""
}

# Dicionário de textos explicativos
EXPLANATIONS = {
    "BDD User Stories": "BDD User Stories: Ideal para times ágeis que priorizam colaboração e entregas iterativas. Uma história centrada no usuário, que descreve quem precisa de algo, o que deseja e por quê, seguida por cenários estruturados com critérios de aceitação em formato Gherkin.",
    "ERS/SRS (IEEE 830)": "ERS/SRS (IEEE 830): Ideal para contratos, projetos formais ou integrações com múltiplos stakeholders. Um documento técnico de requisitos de software, estruturado em seções como Introdução, Requisitos Funcionais, Não Funcionais e Regras de Negócio, conforme a norma IEEE 830.",
    "Model Cards (ML)": "Model Cards (ML): Ideal para projetos com Machine Learning, Deep Learning e modelos fundacionais. Uma ficha técnica padronizada que descreve um modelo de IA: propósito, uso pretendido, dados de treinamento, métricas, riscos éticos e recomendações.",
    "Use Cases (UML)": "Use Cases (UML): Ideal para modelagem de sistemas, especialmente com múltiplas interações e fluxos alternativos. Uma descrição estruturada das interações entre usuários (atores) e o sistema, contendo pré-condições, fluxos principais e alternativos e regras envolvidas.",
    "BPMN 2.0": "BPMN 2.0: Ideal para modelagem de processos de negócio. Representa visualmente etapas, decisões e responsabilidades usando elementos como piscinas, raias, tarefas, gateways e eventos. Excelente para mapear fluxos AS IS/TO BE e alinhar times técnicos e operacionais.",
    "C4 Model": "C4 Model: Ideal para documentação técnica de arquitetura de software. Apresenta o sistema em múltiplos níveis de detalhe — de uma visão geral de contexto até componentes internos — facilitando a comunicação entre times técnicos, produto e negócio."
}

def gerar_user_story_bdd(requisito, system_prompt):
    mensagens = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': requisito}
    ]
    try:
        resposta = client.chat.completions.create(
            messages=mensagens,
            model='gpt-3.5-turbo-0125',
            max_tokens=1000,
            temperature=0
        )
        return resposta.choices[0].message.content, resposta.usage.total_tokens
    except Exception as e:
        return f"Erro ao processar a solicitação: {e}", None

def gerar_bpmn_xml(texto_bpmn):
    # Função simples para criar um arquivo BPMN XML básico
    # O ideal é mapear o texto para elementos BPMN reais, mas aqui é um exemplo didático
    bpmn_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
             xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC"
             xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI"
             typeLanguage="http://www.w3.org/2001/XMLSchema"
             expressionLanguage="http://www.w3.org/1999/XPath"
             targetNamespace="http://bpmn.io/schema/bpmn">
  <process id="Process_1" isExecutable="false">
    <!-- Aqui você pode inserir elementos BPMN gerados a partir do texto -->
    <documentation>{texto_bpmn}</documentation>
  </process>
</definitions>
'''
    return bpmn_template

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()


