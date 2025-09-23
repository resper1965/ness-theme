# Guia Completo de Integração - Agno SDK

Este documento apresenta todas as possibilidades de integração disponíveis no Agno SDK, baseado na documentação oficial.

## 📋 Índice

1. [Instalação e Configuração](#instalação-e-configuração)
2. [Modelos de IA Suportados](#modelos-de-ia-suportados)
3. [Bases de Conhecimento](#bases-de-conhecimento)
4. [Leitores de Documentos](#leitores-de-documentos)
5. [Toolkits Disponíveis](#toolkits-disponíveis)
6. [Interfaces Multi-Modais](#interfaces-multi-modais)
7. [Autenticação e Workspaces](#autenticação-e-workspaces)
8. [Exemplos de Implementação](#exemplos-de-implementação)

---

## 🚀 Instalação e Configuração

### Instalação Básica

```bash
# Criar ambiente virtual
python3 -m venv ~/.venvs/agno
source ~/.venvs/agno/bin/activate

# Instalar Agno SDK
pip install -U agno

# Para desenvolvimento com UI
pip install agno ag-ui-protocol
```

### Configuração de Autenticação

```bash
# Método 1: CLI Authentication
ag setup

# Método 2: Manual API Key
export AGNO_API_KEY=ag-***
```

### Upgrade

```bash
pip install -U agno --no-cache-dir
```

---

## 🤖 Modelos de IA Suportados

### OpenAI Models
```python
from agno.models import OpenAIChat

model = OpenAIChat(
    model="gpt-4",
    api_key="your-openai-api-key"
)
```

### Claude Models
```python
from agno.models import Claude

model = Claude(
    model="claude-3-sonnet-20240229",
    api_key="your-anthropic-api-key"
)
```

### Mistral Models
```python
from agno.models import Mistral

model = Mistral(
    model="mistral-large-latest",
    api_key="your-mistral-api-key"
)
```

### Azure OpenAI
```python
from agno.models import AzureOpenAIChat

model = AzureOpenAIChat(
    model="gpt-4",
    azure_endpoint="your-azure-endpoint",
    api_key="your-azure-api-key"
)
```

### Modelos Locais
```python
from agno.models import Ollama

model = Ollama(
    model="llama2",
    host="localhost:11434"
)
```

---

## 📚 Bases de Conhecimento

### Base de Conhecimento Simples
```python
from agno.knowledge import KnowledgeBase
from agno.document.reader.pdf_reader import PDFReader

# Criar base de conhecimento
knowledge_base = KnowledgeBase(
    name="documentos-empresa",
    vector_db=ChromaDB(collection="empresa_docs")
)

# Adicionar documentos
knowledge_base.load_documents(
    reader=PDFReader(),
    documents=["documento1.pdf", "documento2.pdf"]
)
```

### Base de Conhecimento com Filtros
```python
# Configurar filtros
knowledge_base = KnowledgeBase(
    name="documentos-filtrados",
    vector_db=ChromaDB(collection="filtered_docs")
)

# Usar com filtros
agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    knowledge_filters={
        "user_id": "jordan_mitchell",
        "document_type": "cv",
        "year": 2025,
    }
)
```

### Tipos de Bases de Conhecimento

#### ChromaDB
```python
from agno.knowledge import ChromaDB

vector_db = ChromaDB(
    collection="meus_documentos",
    path="./chroma_db"
)
```

#### Pinecone
```python
from agno.knowledge import Pinecone

vector_db = Pinecone(
    index_name="meus-documentos",
    api_key="your-pinecone-api-key"
)
```

#### Weaviate
```python
from agno.knowledge import Weaviate

vector_db = Weaviate(
    url="http://localhost:8080",
    index_name="Documentos"
)
```

---

## 📄 Leitores de Documentos

### PDF Reader
```python
from agno.document.reader.pdf_reader import PDFReader

reader = PDFReader()
documents = reader.read("documento.pdf")
```

### Website Reader
```python
from agno.document.reader.website_reader import WebsiteReader

reader = WebsiteReader()
documents = reader.read("https://example.com")
```

### S3 Readers
```python
from agno.document.reader.s3.pdf_reader import S3PDFReader
from agno.document.reader.s3.text_reader import S3TextReader

# PDF do S3
pdf_reader = S3PDFReader(
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)

# Texto do S3
text_reader = S3TextReader(
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)
```

### Outros Leitores
```python
# DOCX
from agno.document.reader.docx_reader import DOCXReader

# JSON
from agno.document.reader.json_reader import JSONReader

# Texto
from agno.document.reader.text_reader import TextReader

# ArXiv
from agno.document.reader.arxiv_reader import ArXivReader
```

---

## 🛠️ Toolkits Disponíveis

### Busca na Web
```python
from agno.tools import DuckDuckGoTools

tools = DuckDuckGoTools()
```

### Exa Search
```python
from agno.tools import ExaTools

tools = ExaTools(
    api_key="your-exa-api-key"
)
```

### Google Maps
```python
from agno.tools import GoogleMapsTools

tools = GoogleMapsTools(
    api_key="your-google-maps-api-key"
)
```

### Gmail
```python
from agno.tools import GmailTools

tools = GmailTools(
    credentials_path="path/to/credentials.json"
)
```

### GitHub
```python
from agno.tools import GitHubTools

tools = GitHubTools(
    token="your-github-token"
)
```

### Zoom
```python
from agno.tools import ZoomTools

tools = ZoomTools(
    client_id="your-zoom-client-id",
    client_secret="your-zoom-client-secret"
)
```

### Twitter/X
```python
from agno.tools import TwitterTools

tools = TwitterTools(
    bearer_token="your-twitter-bearer-token"
)
```

### Slack
```python
from agno.tools import SlackTools

tools = SlackTools(
    bot_token="your-slack-bot-token"
)
```

### Notion
```python
from agno.tools import NotionTools

tools = NotionTools(
    integration_token="your-notion-token"
)
```

---

## 🖼️ Interfaces Multi-Modais

### Processamento de Imagens
```python
from agno.models import Image

# Imagem por URL
image = Image(url="https://example.com/image.jpg")

# Imagem por arquivo local
image = Image(filepath="/path/to/image.jpg")

# Imagem por conteúdo
image = Image(content=image_bytes)

# Com metadados
image = Image(
    url="https://example.com/image.jpg",
    detail="high",
    id="image_001"
)
```

### Uso com Agentes
```python
# Processar imagem
response = agent.print_response(
    "Descreva esta imagem",
    images=[image]
)

# Processar múltiplas imagens
images = [
    Image(url="https://example.com/image1.jpg"),
    Image(filepath="/path/to/image2.jpg")
]

response = agent.run(
    "Compare estas imagens",
    images=images
)
```

---

## 🏢 Autenticação e Workspaces

### Configuração de Workspace
```bash
# Configurar workspace existente
ag ws setup

# Resetar configuração
ag init -r
```

### Gerenciamento de Git
```bash
# Inicializar repositório
git init
git add .
git commit -m "Init LLM App"
git branch -M main
git remote add origin https://github.com/[YOUR_GIT_REPO].git
git push -u origin main
```

---

## 💡 Exemplos de Implementação

### Agente Básico
```python
from agno.agent import Agent
from agno.models import OpenAIChat

# Criar agente
agent = Agent(
    model=OpenAIChat(model="gpt-4"),
    instructions=[
        "Você é um assistente útil e prestativo.",
        "Seja conciso e direto nas respostas.",
        "Se não souber algo, admita."
    ]
)

# Usar agente
response = agent.print_response("Olá, como você pode me ajudar?")
```

### Agente com Conhecimento
```python
from agno.agent import Agent
from agno.knowledge import KnowledgeBase
from agno.document.reader.pdf_reader import PDFReader

# Criar base de conhecimento
knowledge_base = KnowledgeBase(
    name="documentos-empresa",
    vector_db=ChromaDB(collection="empresa_docs")
)

# Carregar documentos
knowledge_base.load_documents(
    reader=PDFReader(),
    documents=["manual.pdf", "procedimentos.pdf"]
)

# Criar agente com conhecimento
agent = Agent(
    model=OpenAIChat(model="gpt-4"),
    knowledge=knowledge_base,
    search_knowledge=True
)
```

### Agente com Ferramentas
```python
from agno.agent import Agent
from agno.tools import DuckDuckGoTools, GitHubTools

# Criar ferramentas
tools = [
    DuckDuckGoTools(),
    GitHubTools(token="your-github-token")
]

# Criar agente com ferramentas
agent = Agent(
    model=OpenAIChat(model="gpt-4"),
    tools=tools
)
```

### Agente Multi-Modal
```python
from agno.agent import Agent
from agno.models import Image

# Criar agente
agent = Agent(
    model=OpenAIChat(model="gpt-4-vision-preview")
)

# Processar imagem
image = Image(url="https://example.com/chart.jpg")
response = agent.print_response(
    "Analise este gráfico e me dê insights",
    images=[image]
)
```

### Agente com Filtros de Conhecimento
```python
# Agente com filtros específicos
agent = Agent(
    model=OpenAIChat(model="gpt-4"),
    knowledge=knowledge_base,
    search_knowledge=True,
    knowledge_filters={
        "user_id": "jordan_mitchell",
        "document_type": "cv",
        "year": 2025,
    }
)

response = agent.print_response(
    "Conte-me sobre a experiência de Jordan Mitchell",
    markdown=True
)
```

---

## 🔧 Desenvolvimento e Qualidade

### Formatação de Código
```bash
# Formatar código
./scripts/format.sh
# ou
ruff format .
```

### Validação
```bash
# Validar código
./scripts/validate.sh
# ou
ruff check .
mypy .
```

### Configuração de Desenvolvimento
```bash
# Setup de desenvolvimento
./scripts/dev_setup.sh

# Ativar ambiente
source .venv/bin/activate

# Instalar em modo editável
uv pip install -e .
```

---

## 🌐 Integração com Frontend

### Dojo (Frontend Avançado)
```bash
# Clonar projeto Dojo
git clone https://github.com/ag-ui-protocol/ag-ui.git

# Instalar dependências
cd ag-ui/typescript-sdk
pnpm install

# Build do pacote Agno
cd integrations/agno
pnpm run build

# Executar Dojo
pnpm run dev
```

### Exemplo de Backend com AGUIApp
```python
from agno.agent import Agent
from agno.app import AGUIApp

# Criar agente
agent = Agent(
    model=OpenAIChat(model="gpt-4"),
    instructions=["Você é um assistente útil."]
)

# Criar aplicação
app = AGUIApp(agent=agent)

# Executar
if __name__ == "__main__":
    app.run()
```

---

## 📊 Monitoramento e Métricas

### Configuração de Monitoramento
```python
# Agente com monitoramento
agent = Agent(
    model=OpenAIChat(model="gpt-4"),
    monitoring=True,  # Habilita monitoramento
    workspace_id="your-workspace-id"
)
```

### Métricas de Performance
- Tracking automático de performance
- Métricas de uso de tokens
- Análise de qualidade de respostas
- Dashboard em app.agno.com

---

## 🚀 Deploy e Produção

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

### AWS Deployment
```bash
# Deploy para AWS
ag deploy --platform aws
```

### Variáveis de Ambiente
```bash
# Configurações necessárias
export AGNO_API_KEY=ag-***
export OPENAI_API_KEY=sk-***
export ANTHROPIC_API_KEY=sk-ant-***
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [Documentação Agno](https://docs.agno.com)
- [Exemplos no GitHub](https://github.com/agno-agi/agno)
- [Cookbook de Exemplos](https://github.com/agno-agi/agno/tree/main/cookbook)

### Comunidade
- [Discord](https://discord.gg/4MtYHHrgA8)
- [Discourse](https://community.agno.com/)
- [GitHub Issues](https://github.com/agno-agi/agno/issues)

### Contribuição
- Fork do repositório
- Criar branch para feature
- Enviar pull request
- Seguir guidelines de contribuição

---

## 🔄 Migração de Phidata

### Principais Mudanças
```python
# Antes (Phidata)
from phi.model import OpenAIChat
from phi.knowledge_base import ChromaDB
from phi.document.reader.pdf import PDFReader

# Depois (Agno)
from agno.models import OpenAIChat
from agno.knowledge import ChromaDB
from agno.document.reader.pdf_reader import PDFReader
```

### CLI Changes
```bash
# Antes
phi setup
phi ws setup

# Depois
ag setup
ag ws setup
```

---

Este guia cobre todas as possibilidades de integração disponíveis no Agno SDK. Para implementações específicas, consulte a documentação oficial e os exemplos no repositório GitHub.
