
# FINANCIAL AI CHATBOT - PROJECT GUIDE

## PROJECT OVERVIEW

**Duration**: 5 weeks  
**Team**: 7 members  
**Goal**: Build a professional financial chatbot using Retrieval-Augmented Generation (RAG) with NASDAQ documents  
**Deployment**: Currently running on an AWS EC2 instance for production  
**Scope**: Enterprise-grade functionality with manageable complexity



## Project Summary

This project aims to build a professional, domain-aware conversational assistant focused on financial documents and reporting (e.g., NASDAQ filings, annual reports, and financial statements). The assistant will allow users to ask natural-language questions about financial data and receive clear, sourced, and contextualized answers built using Retrieval-Augmented Generation (RAG).

Key goals:
- Provide quick, accurate answers to targeted financial queries (e.g., revenue, EPS, cash flow drivers).
- Summarize and explain financial statements and ratios in plain language for both experts and non-experts.
- Surface citations and source metadata for traceability (document, page, company, year).
- Support decision-making by highlighting relevant trends, anomalies, and benchmark comparisons.

Scope and capabilities:
- Question answering over PDFs and structured financial data (income statements, balance sheets, cash flow statements).
- Document-level context retrieval using an embeddings + vector index (Pinecone by default).
- LLM-driven generation via a cloud provider (AWS Bedrock) with prompt templates that enforce safety, source citation, and concise explanations.
- Admin features for indexing, monitoring, and basic sentiment analytics.

Development approach (high level):
1. Data ingestion and preprocessing: extract text from documents, chunk, and create embeddings.
2. Indexing and search: upsert vectors into the vector DB and implement a search service for top-K retrieval.
3. RAG orchestration: format prompts with retrieved context and call the LLM provider to generate responses.
4. Frontend and UX: conversational UI (React) with streaming responses, citations, and admin dashboards.
5. Test, validate, and deploy: automated tests, staging validation, and deploy to EC2 for production.

Expected benefits:
- Faster access to financial insights and source-backed answers.
- Consistent, auditable responses with citations to original documents.
- Lower time-to-insight for analysts and improved financial literacy for general users.

---

## CURRENT ARCHITECTURE: EC2 INSTANCE WITH MODULAR MICROSERVICES

### Why this architecture?
- **Professional and pragmatic**: Technologies adopted by leading tech companies
- **Transferable skills**: Docker, FastAPI, microservices, modern APIs
- **Scalable**: MVP-first, then robust production

### Main Components
1. **Document Store (S3/Filesystem):** Stores original PDFs and processed text.
2. **Doc Processor (Batch Service):** Extracts, cleans, and chunks text → generates **embeddings** → indexes in **Vector DB**.
3. **Vector DB (Pinecone):** Stores vector embeddings and metadata for semantic search.
4. **Search Service (FastAPI):** Handles semantic queries: *query → top‑k chunks*.
5. **LLM Service (FastAPI):** Abstracts the LLM provider (AWS Bedrock). Receives *formatted prompt* + *context*, returns *streamed or complete response*.
6. **Chat API (FastAPI):** Public endpoints, orchestrates the RAG flow (User Query → Search → Prompt Formatting → LLM), manages **history**, **sessions**, and **authorization**.
7. **Frontend (React):** ChatGPT-style conversational interface.
8. **PostgreSQL:** Stores **users/sessions**, **chat history**, **document catalog**, **configurations** (e.g., index version, feature flags).
9. **Sentiment Analysis Service (FastAPI):** Provides sentiment metrics and admin dashboard endpoints.
10. **Observability (CloudWatch/Prometheus):** Logging, metrics, dashboards, and alerts.

---


## ARCHITECTURE DIAGRAM

```
        ┌─── Frontend (React) ────┐
        │   http://<EC2-IP>:8501 │
        └───────┬───────┬────────┘
                │       │
                │       │
                │       │
                │   ┌───────────────┐
                │   │ Sentiment     │
                │   │ Analysis      │
                │   │ Service       │
                │   │ http://<EC2-IP>:8001 │
                │   └───────────────┘
                │
                ▼
    ┌───────────── Chat API (FastAPI) ─────────────┐
    │           http://<EC2-IP>:8000              │
    │  • RAG Orchestration                        │
    │  • Session Management                       │
    │  • Public Endpoints                         │
    └─────────────┬─────────────┬─────────────────┘
          │             │
  ┌───────▼───────┬────▼────────────┐
  │               │                │
┌────▼─────┐   ┌─────────────┐   ┌─────────────┐
│ Search   │   │PostgreSQL   │   │ AWS Bedrock │
│ Service  │   │(Metadata)   │   │ (LLM Model) │
│ :8001    │   │             │   │ (cloud API) │
└────┬─────┘   └─────────────┘   └─────────────┘
  │
  ▼
┌─────────────┐
│ Pinecone    │
│ (Vectors)   │
└─────────────┘
  ▲
  │
┌─────┴─────────┐
│ Doc Processor │
│ (Background)  │
│ S3 → Text     │
│ → Embeddings  │
└───────────────┘
```

---

### Key clarifications:
- The Chat API communicates directly with AWS Bedrock (LLM) via cloud API, not through a local LLM service.
- The Sentiment Analysis Service is accessed directly from the Frontend for metrics and dashboard features.

---

###  High-Level Data Flow
```
[PDFs in S3] --(Doc Processor)--> [Clean Text + Chunks] --(Embeddings)--> [Pinecone Vector DB]
             (metadata → PostgreSQL catalog)

User → [Frontend] → [Chat API] → [Search Service] → [Pinecone] (top‑k + metadata)
                 ↓
           [LLM Service] (Prompt Formatting + Context)
                 ↓
               Response to user (streamed)
              + saves history (PostgreSQL)
```

---

### Prompt Flow and Orchestration

1. **User submits a question** via the frontend.
2. **Chat API** receives the query and sends it to the **Search Service**.
3. **Search Service** queries **Pinecone** for the most relevant document chunks (top‑k results).
4. The results are used as **context** for prompt formatting.
5. **Chat API** formats the prompt and sends it to the **LLM Service** (using AWS Bedrock).
6. **LLM Service** generates a response using the context and returns it to the Chat API.
7. **Chat API** streams the response back to the user and saves the conversation history in **PostgreSQL**.
8. **Sentiment Analysis Service** can be called to analyze user messages and provide metrics for the admin dashboard.

---

### Technologies in Use
- **AWS EC2**: Hosts all services for production.
- **AWS Bedrock**: Large Language Model provider for generation and embeddings.
- **Pinecone**: Vector database for semantic search.
- **PostgreSQL**: Relational database for metadata, users, and chat history.
- **FastAPI**: Backend framework for all microservices (Chat API, Search, LLM, Sentiment Analysis).
- **React**: Frontend for user interaction and admin dashboard.

---

### Notes
- All references to anyoneai have been removed.
- The system is designed for clarity, scalability, and professional maintainability.

###  Modos de actualización de la Base de Conocimiento
- **Backfill inicial (one‑shot):** procesa todo el dataset y crea el índice.
- **Incremental (programado):** jobs diarios/semanales que detectan nuevos PDFs (por nombre/fecha en S3) y solo indexan lo nuevo.
- **Reindex parcial:** cuando cambia el *chunking* o el *modelo de embeddings*, se reindexan compañías o años específicos.
- **Reindex total (bajo control):** para cambios mayores (e.g., swap de vector DB o de modelo). Mantener **versionado de índice** en PostgreSQL para rollback.

> **Nota**: Los embeddings **NO** se recalculan en tiempo real en el chat. Son parte de un **pipeline interno** que se dispara on‑demand o por schedule.

##  Decisiones Técnicas y Claridades

###  ¿Por qué PostgreSQL y para qué?
- **Qué guarda:**  
  - `users`, `sessions`, `chat_messages` → historial y contexto conversacional.  
  - `documents`, `document_versions`, `ingestion_runs` → catálogo, versionado y auditoría del pipeline.  
  - `configs` → parámetros de RAG (top_k, chunk_size, overlap, modelo LLM, versión de índice activa).  
- **Por qué Postgres:** relacional, consultas complejas y fácil en local (Docker). Si más adelante necesitas *serverless key/value* (altísimo volumen), se puede migrar **sólo las partes** adecuadas a DynamoDB sin romper el resto.

###  ¿Microservicios o no?
- **MVP (recomendado):** *macroservicios* separados en **contenedores** distintos, pero en el mismo repo (monorepo).  
  - `chat-api` (público)  
  - `search-service` (interno)  
  - `llm-service` (interno)  
  - `doc-processor` (batch/worker)
- **Por qué así:** facilita escalar *sólo* lo que necesita capacidad; mantiene límites claros sin sobre‑fragmentar.  
-- **Producción:** desplegar cada servicio como contenedores en una instancia EC2 (docker-compose or container runtime) o en una plataforma gestionada; dependencias manejadas por secretos/variables.

###  Elección de Vector DB
- **Pinecone (SaaS):** rápido, simple, pay‑as‑you‑go. Excelente para empezar.  
- **OpenSearch (AWS) / Qdrant (self‑hosted):** más control (coste/privacidad). Útil si quieres 100% en AWS.  
- Abstraer con un puerto (interface) en `search-service` para poder cambiar el backend sin tocar el resto.

### LLM Provider
- **Bedrock (Claude/Titan) o OpenAI**. Encapsular en `llm-service` una interfaz `generate()` y `embed()` para permitir *multi‑provider* y *failover*.

### Seguridad
- Secrets en **AWS Secrets Manager**.  
- Firmas pre‑autorizadas de S3 para ingestión.  
- Sanitizar prompts (instrucciones anti‑jailbreak) y **citar fuentes** (IDs + URLs) cuando sea posible.

---

## DISTRIBUCIÓN DEL EQUIPO (7 PERSONAS)

### **Persona 1: Data Pipeline Lead**
- **Responsabilidad**: Ingesta de documentos, extracción de texto, chunking
- **Tecnologías**: Python, S3, PyMuPDF, procesamiento batch
- **Entregables**: Scripts de descarga, procesamiento de PDFs, pipeline de limpieza

### **Persona 2: Embeddings & Vector Specialist**
- **Responsabilidad**: Generación de embeddings, integración vector DB
- **Tecnologías**: Pinecone/OpenSearch, Bedrock Embeddings, indexación
- **Entregables**: Servicio de embeddings, configuración vector DB

### **Persona 3: Search Service Developer**
- **Responsabilidad**: API de búsqueda semántica, filtros, re-ranking
- **Tecnologías**: FastAPI, algoritmos de búsqueda, métricas de relevancia
- **Entregables**: Search Service con endpoints optimizados

### **Persona 4: LLM Integration Engineer**
- **Responsabilidad**: Abstracción multi-provider, prompt engineering, streaming
- **Tecnologías**: Bedrock/OpenAI APIs, prompt templates, generación texto
- **Entregables**: LLM Service con failover y prompt optimization

### **Persona 5: Chat API & Orchestration**
- **Responsabilidad**: Orquestación RAG, gestión sesiones, endpoints públicos
- **Tecnologías**: FastAPI, PostgreSQL, lógica de negocio, autenticación
- **Entregables**: Chat API principal con flujo RAG completo

### **Persona 6: Frontend Developer**
- **Responsabilidad**: Interfaz conversacional, visualización citas, UX
- **Tecnologías**: Streamlit (inicial) → React (avanzado), integración APIs
- **Entregables**: Frontend completo con experiencia usuario optimizada

### **Persona 7: DevOps & Infrastructure**
- **Responsabilidad**: Containerización, CI/CD, monitoreo, AWS deployment
- **Tecnologías**: Docker, ECS Fargate, CloudWatch, GitHub Actions
- **Entregables**: Pipelines deployment, infraestructura AWS, observabilidad

---

## TIMELINE DETALLADO - 5 SEMANAS

### **SEMANA 1: Foundations & Local Setup**
**Objetivo**: Infraestructura base funcionando + división de trabajo clara

#### Día 1-2: Project Setup
1. **Repository structure** - Monorepo con estructura de microservicios
2. **Development environment** - Docker Compose + Python environments
3. **API contracts** - Definir interfaces entre servicios
4. **Database schema** - PostgreSQL inicial + migraciones

#### Día 3-5: Core Infrastructure

5. **Local Docker services** - PostgreSQL, basic containers
6. **Service skeletons** - FastAPI apps with health checks
7. **Database models** - SQLAlchemy models + Alembic migrations
8. **Inter-service communication** - HTTP client setup between services

**Week 1 Deliverables**:
- ✅ Docker Compose working on all machines
- ✅ Basic services responding (health checks)
- ✅ Database with initial schema
- ✅ Communication between containers established

### **WEEK 2: Document Processing & Embeddings Pipeline**
**Goal**: Fully functional knowledge pipeline

#### Days 6-8: Document Ingestion
9. **PDF processing** - Text extraction, metadata, cleaning
10. **Chunking strategy** - Segmentation with overlap, preserve context
11. **S3 integration** - Upload/download documents, organization
12. **Batch processing** - Scripts to process complete datasets

#### Days 9-10: Embeddings & Indexing
13. **Bedrock Embeddings** - Integration for document embeddings
14. **Vector DB setup** - Pinecone index + batch upsert
15. **Search Service /search** - Basic semantic search
16. **Doc Processor integration** - Complete pipeline: PDF → vectors

**Week 2 Deliverables**:
- ✅ Documents processed and vectorized in Pinecone
- ✅ Search Service returning relevant results
- ✅ Automated embeddings pipeline

### **WEEK 3: RAG Implementation & Chat Logic**
**Goal**: End-to-end RAG system working

#### Days 11-13: RAG Orchestration
17. **Chat API core logic** - Orchestration: query → search → prompt → LLM
18. **Prompt engineering** - Templates for financial answers
19. **Bedrock /generate** - Integration with streaming
20. **Citations system** - Source metadata in responses

#### Days 14-15: Session Management
21. **User sessions** - Conversational context management
22. **Chat history** - Persistence in PostgreSQL
23. **Context window** - Token limit management
24. **Basic frontend** - React app for testing

**Week 3 Deliverables**:
- ✅ Fully functional RAG chatbot
- ✅ Responses with citations and sources
- ✅ Basic interface for demonstration
- ✅ Persistent conversational history

### **WEEK 4: Frontend Enhancement & Performance**
**Goal**: Professional UI + optimizations + testing

#### Days 16-18: Frontend Development
25. **React optimization** - Polished UI, reusable components
26. **Chat interface** - Message bubbles, typing indicators, citations display
27. **Document browser** - View of available sources
28. **Error handling** - Loading states, error management

#### Days 19-20: Performance & Quality
29. **Response optimization** - Streaming, chunked responses
30. **Testing suite** - Critical unit tests + integration tests
31. **Performance tuning** - Latency and memory usage optimization

**Week 4 Deliverables**:
- ✅ Complete and professional frontend
- ✅ Performance < 3 seconds per query
- ✅ Automated testing
- ✅ Optimized and stable system

### **WEEK 5: Production Deployment**
**Goal**: Deploy to production (EC2) + production-ready features

#### Día 21-23: Infrastructure
33. **Prepare EC2 host(s)** - Docker, Docker Compose, user data for startup
34. **ALB / DNS** - Load balancer + custom domain + SSL (optional)
35. **RDS migration** - PostgreSQL managed or self-hosted + data migration

#### Día 24-25: Production Features
37. **CI/CD pipeline** - GitHub Actions to build images and deploy to EC2 or registry
38. **Monitoring setup** - CloudWatch + dashboards + alerts
39. **Security hardening** - Secrets Manager + IAM roles + VPC
40. **Final optimization** - Auto-scaling & backups

**Entregables Semana 5**:
- ✅ System deployed to production (EC2 or chosen target)
- ✅ CI/CD automated (optional registry usage)
- ✅ Monitoring and alerts configured
- ✅ Demo final y documentación completa

---

## ESTRUCTURA DE REPOSITORIO (MONOREPO)

```
financial-ai-chatbot/
├── README.md
├── PROYECTO.md                # (este archivo)
├── docker-compose.yml         # entorno local (servicios + dependencias)
├── .env.example               # variables de ejemplo (NUNCA subir .env real)
├── requirements.lock          # lock de dependencias (opcional)
│
├── apps/
│   ├── chat-api/              # FastAPI público (orquestación RAG + sesiones)
│   │   ├── app/
│   │   │   ├── main.py        # arranque FastAPI + routers + middlewares
│   │   │   ├── api/
│   │   │   │   ├── routes_chat.py      # /chat, /stream, /health
│   │   │   │   └── routes_admin.py     # /configs, /reindex (protegidos)
│   │   │   ├── core/
│   │   │   │   ├── config.py           # lectura env vars
│   │   │   │   ├── logging.py          # configuración logs
│   │   │   │   └── security.py         # auth/jwt/cors
│   │   │   ├── services/
│   │   │   │   ├── rag_orchestrator.py # llama search-service y llm-service
│   │   │   │   └── citations.py        # formatea citas/metadata
│   │   │   ├── db/
│   │   │   │   ├── models.py           # SQLAlchemy: users, sessions, messages...
│   │   │   │   ├── schema.sql          # (opcional) SQL puro
│   │   │   │   └── repository.py       # CRUD y helpers
│   │   │   ├── schemas/                # Pydantic request/response
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── pyproject.toml / requirements.txt
│   │
│   ├── search-service/        # API interna para búsqueda semántica
│   │   ├── app/
│   │   │   ├── main.py        # endpoints: /search, /upsert, /delete
│   │   │   ├── adapters/
│   │   │   │   ├── pinecone_adapter.py # implementa interfaz VectorStore
│   │   │   │   ├── qdrant_adapter.py   # (opcional)
│   │   │   │   └── opensearch_adapter.py# (opcional)
│   │   │   ├── core/
│   │   │   │   ├── vectorstore.py      # interfaz común (search, upsert)
│   │   │   │   └── ranking.py          # re‑rank/BM25 híbrido (opcional)
│   │   │   ├── models/
│   │   │   │   └── types.py            # dataclasses para chunks/metadatos
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── llm-service/           # API interna para LLMs (chat + embeddings)
│   │   ├── app/
│   │   │   ├── main.py        # /generate (stream y no stream), /embed
│   │   │   ├── providers/
│   │   │   │   ├── bedrock.py # Claude/Titan (boto3)
│   │   │   │   ├── openai.py  # GPT APIs
│   │   │   │   └── ollama.py  # local (opcional)
│   │   │   ├── core/
│   │   │   │   ├── prompt_templates/
│   │   │   │   │   ├── financial_qa.j2 # plantilla jinja
│   │   │   │   │   └── system_policies.md
│   │   │   │   └── generation.py       # orquesta provider + streaming
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── doc-processor/         # jobs batch para ingestión/embeddings
│   │   ├── app/
│   │   │   ├── main.py        # CLI: backfill, incremental, reindex
│   │   │   ├── ingestion/
│   │   │   │   ├── s3_scanner.py       # encuentra nuevos PDFs
│   │   │   │   └── metadata_parser.py  # parsea nombres/fechas/empresa
│   │   │   ├── processing/
│   │   │   │   ├── pdf_to_text.py      # extracción (pymupdf/pdfminer)
│   │   │   │   ├── clean_text.py       # normalización
│   │   │   │   ├── chunker.py          # chunking (tamaño/overlap configurables)
│   │   │   ├── embeddings/
│   │   │   │   ├── embedder.py         # llama llm-service / provider directo
│   │   │   │   └── schema.py           # estructura del vector + metadatos
│   │   │   ├── indexing/
│   │   │   │   └── upsert_vectors.py   # inserta en Vector DB (batch)
│   │   │   ├── db/
│   │   │   │   ├── models.py           # ingestion_runs, document_versions
│   │   │   │   └── repository.py
│   │   │   ├── config.py
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── requirements.txt
│   │
│   └── frontend/              # Streamlit (MVP) o React (producción)
│       ├── streamlit_app/     # app.py, pages/, components/
│       ├── react_app/         # (opcional) Next.js/CRA
│       └── Dockerfile
│
├── infra/
│   ├── local/
│   │   ├── docker/            # configs, healthchecks
│   │   └── compose/           # archivos compose por entorno
│   ├── aws/
│   │   ├── deployment/        # scripts/configs para deploy en AWS (EC2, ALB, etc.)
│   │   ├── rds/               # parámetros/migraciones
│   │   ├── opensearch/        # si se usa
│   │   └── terraform/         # IaC (opcional)
│   └── scripts/
│       ├── deploy.sh          # generic deploy script (EC2 or registry)
│       ├── build_images.sh
│       └── migrate_db.py
│
├── migrations/                # alembic o SQL plano
├── tests/                     # e2e y utilidades compartidas
└── docs/                      # diagramas, decisiones de arquitectura (ADR)
```

---

## DESARROLLO LOCAL - SETUP PASO A PASO

### Prerequisitos
- Python 3.11+
- Docker + Docker Compose
- Git
- 16GB RAM recomendado
- AWS CLI (para deployment)

### 1. Quick Start
```bash
# 1. Clone y setup
git clone <repo-url>
cd financial-ai-chatbot

# 2. Setup desarrollo completo (script automatizado)
python scripts/dev_setup.py

# 3. Verificar que todo funciona
python scripts/health_check.py

# 4. Acceder aplicación
# Frontend: http://localhost:8501
# Chat API: http://localhost:8000/docs
# Search Service: http://localhost:8001/docs
# LLM Service: http://localhost:8002/docs
```

### 2. Docker Compose (Desarrollo Local)
```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: financial_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: dev_password
    ports: ["5432:5432"]
    volumes: [postgres_data:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d financial_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis removed: not required by the current deployment. Add redis service here if needed later.

  search-service:
    build: ./apps/search-service
    ports: ["8001:8001"]
    env_file: .env
    depends_on:
      postgres: {condition: service_healthy}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 15s
      timeout: 10s
      retries: 3

  # llm-service removed for local dev: models are accessed via AWS Bedrock in production.

  chat-api:
    build: ./apps/chat-api
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      postgres: {condition: service_healthy}
      search-service: {condition: service_healthy}
      llm-service: {condition: service_healthy}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 15s
      timeout: 10s
      retries: 3

  frontend:
    build: ./apps/frontend/streamlit_app
    ports: ["8501:8501"]
    env_file: .env
    depends_on:
      chat-api: {condition: service_healthy}

  doc-processor:
    build: ./apps/doc-processor
    env_file: .env
    depends_on:
      search-service: {condition: service_healthy}
      llm-service: {condition: service_healthy}
    command: ["python", "-m", "app.main", "backfill"]
    profiles: ["processing"]  # Solo corre manualmente

volumes:
  postgres_data:
```

### 3. Variables de Entorno (.env)
```bash
# Application
APP_ENV=local
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://admin:dev_password@postgres:5432/financial_db

# Vector Database
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=us-east1-gcp-free
PINECONE_INDEX=financial-docs

# LLM Provider
LLM_PROVIDER=bedrock
AWS_REGION=us-east-1
BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
EMBEDDING_MODEL=amazon.titan-embed-text-v1

# OpenAI (backup)
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o

# Document Processing
S3_BUCKET=nasdaq-annual-reports-bucket
S3_PREFIX=nasdaq_annual_reports/
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=8

# Service URLs (internal)
SEARCH_SERVICE_URL=http://search-service:8001
```

---

## FLUJO DE DATOS DETALLADO

### 1. Pipeline de Conocimiento (Background)
```
PDFs en S3 → Doc Processor → Extracción texto → Chunking
                ↓
        Generación embeddings → Upsert Pinecone → Update PostgreSQL metadata
```

### 2. Flujo RAG (En línea)
```
Usuario query → Chat API → Search Service → Pinecone (top-k chunks)
                   ↓
            Prompt Template + Context → LLM Service → Respuesta stream
                   ↓
            Guardar historial + Retornar respuesta + Citations
```

### 3. Gestión de Sesiones
```
Usuario → Chat API → Check/Create session → Load context histórico
                        ↓
                   RAG process + Add to context → Update session
```

---

## Production & Deployment Notes

- Production is currently run on an AWS EC2 instance. The simplest production model is to run the same containers there using Docker Compose or a container runtime and keep secrets in AWS Secrets Manager.
- You can add a CI/CD pipeline (GitHub Actions) later to build images and deploy to the EC2 host. Detailed instructions for ECS/ECR have been removed to keep this guide focused on the current setup.
- Monitoring should be integrated with CloudWatch or your preferred observability backend.

---

## CRITERIOS DE ÉXITO

### Técnicos
- ✅ Sistema RAG respondiendo preguntas relevantes sobre NASDAQ
- ✅ Respuestas con citas verificables y metadatos
- ✅ Performance < 3 segundos por query
- ✅ Sistema desplegado en AWS con alta disponibilidad
- ✅ CI/CD automatizado funcionando
- ✅ Tests automatizados > 80% coverage crítico

### De Aprendizaje
- ✅ Cada persona domina su dominio técnico
- ✅ Todos entienden arquitectura completa y flujo RAG
- ✅ Experiencia con tecnologías enterprise (Docker, ECS, microservicios)
- ✅ Portfolio project impresionante para entrevistas
- ✅ Documentación técnica de calidad profesional

### Funcionales
- ✅ Chatbot responde preguntas financieras específicas
- ✅ Maneja múltiples sesiones simultáneas
- ✅ Interfaz intuitiva tipo ChatGPT
- ✅ Sistema de administración para reindexación
- ✅ Monitoreo y alertas funcionando

---

## ESTIMACIÓN DE COSTOS

### Desarrollo Local (Semanas 1-4)
- **Pinecone Free Tier**: $0 (1M vectores)
- **Bedrock/OpenAI API**: $30-80/mes
- **Total desarrollo**: $30-80/mes

### Production cost estimates (indicative)
- **AWS EC2** (small instance running containers): $20-80/month depending on size and uptime
- **RDS PostgreSQL**: $35/month (example)
- **Pinecone / Vector DB**: tier-based (variable)
- **Bedrock / LLM usage**: usage-based and variable
-- **Total production**: depends on usage (compute + LLM calls + vector DB)

---

##  Paso a Paso para Construir

### Fase A — Fundaciones
1. **Repo + entorno**: clonar, crear `venv`, instalar requirements, `docker-compose up` básico (postgres/hello-world).  
2. **Esquema DB**: crear tablas base (users/sessions/messages/documents). Migraciones (Alembic).  
3. **Frontend MVP**: Streamlit con input y panel de respuestas (sin RAG aún).

### Fase B — Pipeline de Conocimiento
4. **Extracción PDF**: convertir PDF → texto (pymupdf/pdfminer) + limpieza.  
5. **Chunking**: tamaño (e.g., 800‑1200 tokens) y solape (e.g., 100‑150). Guardar metadatos: company, año, doc_type, page, source_url.  
6. **Embeddings**: integrar `llm-service /embed` (o provider directo). Batch + retroceso exponencial en errores.  
7. **Indexación**: `search-service /upsert`. Registrar `ingestion_runs` en Postgres (quién, cuándo, cuántos, versión de índice).  
8. **Incremental**: job que escanee S3 por novedades y procese solo lo nuevo.

### Fase C — RAG End-to-End
9. **Search Service /search**: top‑k vector, filtros (compañía/año), re‑rank híbrido (opcional).  
10. **Prompt Templates**: `financial_qa.j2` con instrucciones: “cita fuentes, sé factual, si no sabes dilo”.  
11. **LLM Service /generate**: streaming SSE/WS.  
12. **Chat API /chat**: orquesta → guarda historial → retorna respuesta + citas.  
13. **Frontend**: muestra mensajes, citas (empresa, año, página, enlace).

### Fase D — Calidad y Producción
14. **Tests**: unit (chunker, ranking), integración (search+llm), e2e (pregunta real).  
15. **Cache (optional)**: Redis can be added for repeated-response caching (hash of query+filters) if needed.
16. **Observabilidad**: logs estructurados (JSON), métricas (latencia, tokens, top_k hitrate), tracing (opcional).  
17. **Seguridad**: auth básica/JWT; CORS; rate limit.  
18. **Deploy**: Build images and deploy to the chosen target (EC2, managed container service, or registry-based workflow).  
19. **SLOs**: p95 < 3s, disponibilidad 99%, coste monitoreado.
---

## RECURSOS RECOMENDADOS

### Pre-proyecto (Opcional)
- Docker fundamentals (3 horas)
- FastAPI tutorial (3 horas)
- RAG concepts (2 horas)
- AWS basics (2 horas)

### Durante Proyecto
- Daily standups (15 min)
- Code review obligatorio
- Architecture discussions
- Pair programming para integraciones críticas

---

## ENTREGABLES POR SEMANA

### Semana 1: Foundation
- Repositorio estructurado + Docker Compose
- Servicios básicos respondiendo
- Database schema + migraciones

### Semana 2: Knowledge Pipeline
- Pipeline de procesamiento PDFs → vectores
- Vector DB poblado con datos reales
- Search Service funcional

### Semana 3: RAG System
- Chat API completo con orquestación RAG
- Respuestas contextuales con citas
- Frontend básico para demos

### Semana 4: Enhancement & Testing
- Frontend optimizado
- Performance tuning + caching
- Testing suite completo

### Semana 5: Production Ready
- Deploy a AWS completo
- CI/CD funcionando
- Monitoring + documentación final

---

## RIESGOS Y MITIGACIONES

### Riesgos Técnicos
- **Complejidad microservicios**: Mitigation → interfaces simples + monorepo
- **Latencia vector search**: Mitigation → caching + optimización índices
- **Costos AWS**: Mitigation → monitoring + alerts + instance right-sizing
- **API rate limits**: Mitigation → retry logic + circuit breakers + multiple providers

### Riesgos de Tiempo
- **Scope creep**: Mitigation → MVP first + feature flags para avanzados
- **Integraciones complejas**: Mitigation → mock services + stub interfaces temprano
- **Dependencias entre equipos**: Mitigation → contratos API claros + trabajo paralelo

### Riesgos de Equipo
- **Diferencias de nivel técnico**: Mitigation → pair programming + code review obligatorio
- **Comunicación**: Mitigation → daily standups + documentación clara + Slack activo

---

## MÉTRICAS DE ÉXITO

### KPIs Técnicos
- **Latencia promedio**: < 3 segundos end-to-end
- **Disponibilidad**: > 99% uptime en producción
- **Accuracy RAG**: > 80% respuestas relevantes (evaluación manual)
- **Test coverage**: > 80% en servicios críticos
- **Error rate**: < 5% de requests fallidos

### KPIs de Aprendizaje
- **Contribuciones**: Cada persona debe tener commits significativos en su área
- **Code review participation**: 100% PRs revisados por al menos 2 personas
- **Documentación**: API docs completa + architecture decisions documentadas
- **Knowledge sharing**: Cada persona presenta su módulo al equipo (15 min c/u)

---

## QUICK REFERENCE - COMANDOS ESENCIALES

### Desarrollo Local
```bash
# Setup inicial completo
python scripts/dev_setup.py

# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f chat-api

# Ejecutar tests
docker-compose exec chat-api pytest

# Procesar documentos (manual)
docker-compose run --rm doc-processor python -m app.main backfill

# Verificar salud de todos los servicios
python scripts/health_check.py

# Limpiar y reiniciar
docker-compose down -v && docker-compose up -d
```

### Comandos por Servicio
```bash
# Chat API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query":"What is Apple revenue?","session_id":"test"}'

# Search Service
curl -X POST http://localhost:8001/search -H "Content-Type: application/json" -d '{"query":"Apple revenue","top_k":5}'

# LLM Service
curl -X POST http://localhost:8002/generate -H "Content-Type: application/json" -d '{"prompt":"Hello","model":"claude-3-sonnet"}'
```

### Deploy to Production (EC2)
```bash
# Build images locally and copy/tar them to the EC2 host or push to a container registry.
# On the EC2 host you can run the containers with docker-compose or docker run.
# Example (on CI or local):
./scripts/build_and_push.sh   # optional if using a registry

# On EC2 host (example using docker-compose)
scp docker-compose.yml ec2-user@<EC2-IP>:/home/ec2-user/
ssh ec2-user@<EC2-IP>
docker-compose pull || true
docker-compose up -d --build

# Verify services on EC2: check container logs and health endpoints
curl http://<EC2-IP>:8000/health
```

---

## ESTRUCTURA DE DATOS - ESQUEMAS CLAVE

### PostgreSQL Schema
```sql
-- Usuarios y sesiones
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    context_summary TEXT
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id),
    role VARCHAR(20) NOT NULL, -- 'user' | 'assistant'
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Catálogo de documentos
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    s3_key VARCHAR(500) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    company VARCHAR(100),
    document_type VARCHAR(50), -- '10-K', '10-Q', 'earnings'
    filing_year INTEGER,
    filing_date DATE,
    processed_at TIMESTAMP,
    chunk_count INTEGER,
    status VARCHAR(20) DEFAULT 'pending' -- 'pending', 'processing', 'completed', 'failed'
);

-- Control de procesamiento
CREATE TABLE ingestion_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_type VARCHAR(20), -- 'backfill', 'incremental', 'reindex'
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    documents_processed INTEGER DEFAULT 0,
    chunks_created INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'running',
    config JSONB
);

-- Configuraciones del sistema
CREATE TABLE system_configs (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Vector Metadata Schema (Pinecone)
```python
# Metadata que se almacena con cada chunk vector
{
    "document_id": "uuid",
    "chunk_index": 0,
    "company": "AAPL",
    "document_type": "10-K",
    "filing_year": 2023,
    "page_number": 45,
    "section": "Risk Factors",
    "source_url": "https://sec.gov/...",
    "text_preview": "First 200 chars...",
    "chunk_size": 1000,
    "processed_at": "2024-01-15T10:30:00Z"
}
```

---

## API CONTRACTS DETALLADOS

### Chat API (Puerto 8000)
```python
# POST /chat
{
    "session_id": "uuid-optional",
    "query": "What was Apple's revenue in 2023?",
    "company_filters": ["AAPL", "MSFT"],  # opcional
    "top_k": 8,  # opcional, default del config
    "stream": false  # opcional
}

# Response
{
    "session_id": "uuid",
    "message_id": "uuid",
    "answer": "According to Apple's 10-K filing...",
    "citations": [
        {
            "document_id": "uuid",
            "company": "AAPL",
            "document_type": "10-K",
            "filing_year": 2023,
            "page_number": 31,
            "text_snippet": "Net sales increased to $394.3 billion...",
            "source_url": "https://sec.gov/...",
            "relevance_score": 0.89
        }
    ],
    "processing_time_ms": 2340
}

# GET /chat/history?session_id=uuid&limit=50
{
    "session_id": "uuid",
    "messages": [
        {
            "id": "uuid",
            "role": "user",
            "content": "What was Apple's revenue?",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "id": "uuid", 
            "role": "assistant",
            "content": "According to...",
            "citations": [...],
            "timestamp": "2024-01-15T10:30:02Z"
        }
    ]
}
```

### Search Service (Puerto 8001)
```python
# POST /search
{
    "query": "Apple revenue growth",
    "top_k": 8,
    "filters": {
        "company": ["AAPL"],
        "document_type": ["10-K", "10-Q"],
        "filing_year": [2022, 2023]
    },
    "min_score": 0.7  # opcional
}

# Response
{
    "results": [
        {
            "id": "vector-id-123",
            "score": 0.89,
            "text": "Net sales increased 2% year over year...",
            "metadata": {
                "document_id": "uuid",
                "company": "AAPL",
                "chunk_index": 15,
                "page_number": 31
            }
        }
    ],
    "total_results": 8,
    "processing_time_ms": 145
}
```

### LLM Service (Puerto 8002)
```python
# POST /generate
{
    "prompt": "Based on the context: [CONTEXT], answer: What was Apple's revenue?",
    "model": "claude-3-5-sonnet",  # o "gpt-4o"
    "max_tokens": 1000,
    "temperature": 0.1,
    "stream": true,
    "system_prompt": "You are a financial analyst..."
}

# Response (no stream)
{
    "text": "Based on the provided context...",
    "model": "claude-3-5-sonnet",
    "usage": {
        "input_tokens": 2500,
        "output_tokens": 340,
        "cost_usd": 0.0123
    },
    "processing_time_ms": 1850
}

# POST /embed
{
    "texts": ["Apple Inc. is a technology company...", "Revenue increased by..."],
    "model": "amazon.titan-embed-text-v1"
}

# Response
{
    "embeddings": [
        {
            "vector": [0.1234, -0.5678, ...],  # 1536 dimensions
            "index": 0
        }
    ],
    "model": "amazon.titan-embed-text-v1",
    "usage": {
        "tokens": 25,
        "cost_usd": 0.0001
    }
}
```

---

## CHECKLIST DE ENTREGA FINAL

### Funcionalidad Core
- [ ] Sistema RAG respondiendo preguntas financieras específicas
- [ ] Respuestas incluyen citas verificables con metadatos
- [ ] Historial conversacional persistente por sesión
- [ ] Interface intuitiva tipo ChatGPT
- [ ] Pipeline de procesamiento de documentos funcional
- [ ] Sistema de administración para reindexación

### Calidad Técnica
- [ ] Tests automatizados > 80% coverage en servicios críticos
- [ ] Performance < 3 segundos promedio por query
- [ ] Logs estructurados y observabilidad configurada
- [ ] Error handling robusto en todos los servicios
- [ ] Security básica implementada (CORS, rate limiting)
- [ ] Documentación completa de APIs

### Infraestructura
- [ ] Sistema desplegado en producción (EC2 or managed container service)
- [ ] CI/CD pipeline automatizado funcionando
- [ ] Database managed (RDS) + cache (optional)
- [ ] Load balancer / routing y SSL configurado (if public)
- [ ] Monitoreo y alertas básicas configuradas
- [ ] Secrets management implementado

### Entregables de Equipo
- [ ] Repositorio bien estructurado con README completo
- [ ] Cada persona ha contribuido significativamente a su área
- [ ] Code reviews completados para todos los PRs importantes  
- [ ] Presentación final preparada (15 min por persona)
- [ ] Documentación de arquitectura y decisiones técnicas
- [ ] Postmortem con lecciones aprendidas

---

## PALABRAS FINALES

Este proyecto está diseñado para ser **ambicioso pero alcanzable** en 5 semanas. La clave del éxito será:

1. **Enfoque en MVP primero** - funcionalidad básica funcionando antes que features avanzados
2. **Comunicación constante** - daily standups y resolución rápida de blockers
3. **Parallelización efectiva** - contratos de API claros para trabajo independiente
4. **Testing continuo** - no dejar testing para el final
5. **Documentación sobre la marcha** - documentar decisiones mientras las tomamos

La arquitectura elegida balancea experiencia de aprendizaje con viabilidad técnica. Al final setendrán un sistema que no solo funciona, sino que demuestra comprensión profunda de:

- Sistemas distribuidos modernos
- RAG y arquitecturas de IA
- DevOps y deployment en cloud
- Trabajo en equipo en proyectos técnicos complejos

