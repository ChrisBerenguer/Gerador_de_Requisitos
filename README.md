# Gerador de Requisitos para Engenharia de Software

Este sistema é uma aplicação web interativa desenvolvida em Python com Streamlit, projetada para auxiliar analistas, engenheiros de requisitos e times de desenvolvimento a gerar documentação de requisitos de software em diferentes padrões reconhecidos pelo mercado, a partir de descrições em linguagem natural.

## O que o sistema faz?

- Transforma descrições de requisitos de software em documentos estruturados nos seguintes formatos:
  - **User Stories BDD** (com critérios de aceitação em Gherkin)
  - **ERS/SRS (IEEE 830)**
  - **Model Cards (ML)**
  - **Use Cases (UML)**
  - **BPMN 2.0** (com exportação para XML básico)
- Utiliza a API da OpenAI para gerar textos estruturados e claros, facilitando a comunicação entre stakeholders técnicos e não técnicos.
- Permite exportar processos BPMN para uso em ferramentas como Draw.io.

## Bibliotecas e APIs utilizadas

- [Streamlit](https://streamlit.io/) — Interface web interativa
- [openai](https://pypi.org/project/openai/) — Integração com a API da OpenAI (GPT-3.5 Turbo)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Carregamento de variáveis de ambiente (chave da OpenAI)

## Pré-requisitos

- Python 3.8+
- Conta na OpenAI e chave de API válida

## Instalação

1. Clone este repositório ou baixe os arquivos para sua máquina.
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # Ative o ambiente virtual:
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave da OpenAI:
   ```env
   OPENAI_API_KEY=sua-chave-aqui
   ```

## Como rodar a aplicação

Execute o comando abaixo no terminal, na pasta do projeto:

```bash
streamlit run 22_User_Stories_BDD.py
```

Acesse o endereço exibido no terminal (geralmente http://localhost:8501) para utilizar a interface web.

## Observações
- O consumo da API da OpenAI pode gerar custos conforme o uso.
- O sistema foi projetado para facilitar a documentação de requisitos, mas recomenda-se revisão humana antes de uso em contratos ou documentação oficial.

---

Desenvolvido para apoiar a Engenharia de Requisitos e a comunicação entre times de software. 