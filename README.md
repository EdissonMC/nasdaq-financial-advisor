
# FINANCIAL AI CHATBOT - PROJECT GUIDE

## PROJECT OVERVIEW

**Duration**: 5 weeks  
**Team**: 7 members  
**Goal**: Build a professional financial chatbot using Retrieval-Augmented Generation (RAG) with NASDAQ documents  
**Deployment**: Currently running on an AWS EC2 instance for production  
**Scope**: Enterprise-grade functionality with manageable complexity



## Project summary (current implementation)

This repository contains a working financial question-answering system based on Retrieval-Augmented Generation (RAG). The implemented system ingests financial documents (PDFs), indexes semantic embeddings in a vector store, and serves a conversational frontend that returns source-backed answers.

Key features implemented:
- Natural-language Q&A over financial documents and structured tables (income statements, balance sheets, cash flows).
- Context retrieval using embeddings stored in Pinecone (or configured vector DB).
- Prompting and generation via a cloud LLM provider (AWS Bedrock by default) with templates that enforce citation and concise explanations.
- A FastAPI-based Chat API that orchestrates RAG, session/history storage, and streaming responses.
- A React frontend that provides a chat UI, citation display, and an admin dashboard for metrics.
- A Sentiment Analysis service that collects per-message sentiment and provides dashboard metrics.

Implementation overview (what is present in this repo):
1. Ingestion pipeline (doc-processor) that extracts text from PDFs, chunks documents, and computes embeddings.
2. Search service that queries the vector DB and returns top-K contexts with metadata.
3. Chat API (FastAPI) that constructs RAG prompts, calls the LLM provider, streams results, and persists chat history in PostgreSQL.
4. Frontend (React) that connects to the Chat API, displays streaming messages and citations, and includes a simple admin/login flow.
5. Docker Compose configurations and helper scripts to run the full stack locally or on an EC2 host.

Benefits realized by the current implementation:
- Immediate access to searchable, source-cited answers across ingested NASDAQ documents.
- Traceability: each generated answer can include citations to the original document, page, and metadata.
- Production-ready pieces: containerized services, persistent storage (Postgres), and monitoring hooks.

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

### Knowledge Base Update Modes
- **Initial backfill (one-shot):** Processes the entire dataset and creates the index.
- **Incremental (scheduled):** Daily/weekly jobs that detect new PDFs (by name/date in S3) and only index the new ones.
- **Partial reindex:** When chunking or embedding model changes, reindex specific companies or years.
- **Full reindex (controlled):** For major changes (e.g., vector DB swap or model change). Maintain index versioning in PostgreSQL for rollback.

> **Note**: Embeddings are **NOT** recalculated in real-time during chat. They are part of an **internal pipeline** that triggers on-demand or by schedule.

## Technical Decisions and Clarifications

### Why PostgreSQL and what for?
- **What it stores:**
  - `users`, `sessions`, `chat_messages` → conversational history and context.
  - `documents`, `document_versions`, `ingestion_runs` → catalog, versioning, and audit of the pipeline.
  - `configs` → RAG parameters (top_k, chunk_size, overlap, LLM model, active index version).
- **Why Postgres:** Relational, complex queries, and easy locally (Docker). If more later you need *serverless key/value* (high volume), you can migrate **only the appropriate parts** to DynamoDB without breaking the rest.

### Microservices or not?
- **MVP (recommended):** *Macroservices* separated in **distinct containers**, but in the same repo (monorepo).
  - `chat-api` (public)
  - `search-service` (internal)
  - `llm-service` (internal)
  - `doc-processor` (batch/worker)
- **Why this way:** Facilitates scaling *only* what needs capacity; maintains clear limits without over-fragmenting.
- **Production:** Deploy each service as containers on an EC2 instance (docker-compose or container runtime) or managed platform; dependencies managed by secrets/variables.

### Vector DB Choice
- **Pinecone (SaaS):** Fast, simple, pay-as-you-go. Excellent for starting.
- **OpenSearch (AWS) / Qdrant (self-hosted):** More control (cost/privacy). Useful if you want 100% in AWS.
- Abstract with a port (interface) in `search-service` to be able to change the backend without touching the rest.

### LLM Provider
- **Bedrock (Claude/Titan) or OpenAI**. Encapsulate in `llm-service` an interface `generate()` and `embed()` to allow *multi-provider* and *failover*.

### Security
- Secrets in **AWS Secrets Manager**.
- Pre-authorized S3 signatures for ingestion.
- Sanitize prompts (anti-jailbreak instructions) and **cite sources** (IDs + URLs) when possible.

---

## TEAM DISTRIBUTION (7 PEOPLE)

### **Persona 1: Data Pipeline Lead**
- **Responsibility**: Document ingestion, text extraction, chunking
- **Technologies**: Python, S3, PyMuPDF, batch processing
- **Deliverables**: Download scripts, PDF processing, cleaning pipeline

### **Persona 2: Embeddings & Vector Specialist**
- **Responsibility**: Embedding generation, vector DB integration
- **Technologies**: Pinecone/OpenSearch, Bedrock Embeddings, indexing
- **Deliverables**: Embedding service, vector DB configuration

### **Persona 3: Search Service Developer**
- **Responsibility**: Semantic search API, filters, re-ranking
- **Technologies**: FastAPI, search algorithms, relevance metrics
- **Deliverables**: Optimized Search Service with endpoints

### **Persona 4: LLM Integration Engineer**
- **Responsibility**: Multi-provider abstraction, prompt engineering, streaming
- **Technologies**: Bedrock/OpenAI APIs, prompt templates, text generation
- **Deliverables**: LLM Service with failover and prompt optimization

### **Persona 5: Chat API & Orchestration**
- **Responsibility**: RAG orchestration, session management, public endpoints
- **Technologies**: FastAPI, PostgreSQL, business logic, authentication
- **Deliverables**: Main Chat API with complete RAG flow

### **Persona 6: Frontend Developer**
- **Responsibility**: Conversational interface, citation visualization, UX
- **Technologies**: Streamlit (initial) → React (advanced), API integration
- **Deliverables**: Complete frontend with optimized user experience

### **Persona 7: DevOps & Infrastructure**
- **Responsibility**: Containerization, CI/CD, monitoring, AWS deployment
- **Technologies**: Docker, ECS Fargate, CloudWatch, GitHub Actions
- **Deliverables**: Deployment pipelines, AWS infrastructure, observability

---

## IMPLEMENTATION STATUS - 5 WEEKS COMPLETED

### **Week 1: Foundations & Local Setup**
**Objective**: Base infrastructure working + clear work division

#### Day 1-2: Project Setup
1. **Repository structure** - Monorepo with microservices structure
2. **Development environment** - Docker Compose + Python environments
3. **API contracts** - Define interfaces between services
4. **Database schema** - Initial PostgreSQL + migrations

#### Day 3-5: Core Infrastructure
5. **Local Docker services** - PostgreSQL, basic containers
6. **Service skeletons** - FastAPI apps with health checks
7. **Database models** - SQLAlchemy models + Alembic migrations
8. **Inter-service communication** - HTTP client setup between services

**Week 1 Deliverables**:
- ✅ Docker Compose working on all machines
- ✅ Basic services responding (health checks)
- ✅ Database with initial schema
- ✅ Communication between containers established

### **Week 2: Document Processing & Embeddings Pipeline**
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

### **Week 3: RAG Implementation & Chat Logic**
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

### **Week 4: Frontend Enhancement & Performance**
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

### **Week 5: Production Deployment**
**Goal**: Deploy to production (EC2) + production-ready features

#### Day 21-23: Infrastructure
33. **Prepare EC2 host(s)** - Docker, Docker Compose, user data for startup
34. **ALB / DNS** - Load balancer + custom domain + SSL (optional)
35. **RDS migration** - PostgreSQL managed or self-hosted + data migration

#### Day 24-25: Production Features
37. **CI/CD pipeline** - GitHub Actions to build images and deploy to EC2 or registry
38. **Monitoring setup** - CloudWatch + dashboards + alerts
39. **Security hardening** - Secrets Manager + IAM roles + VPC
40. **Final optimization** - Auto-scaling & backups

**Week 5 Deliverables**:
- ✅ System deployed to production (EC2)
- ✅ CI/CD automated (optional registry usage)
- ✅ Monitoring and alerts configured
- ✅ Final demo and complete documentation

---

## REPOSITORY STRUCTURE (MONOREPO)

```
financial-ai-chatbot/
├── README.md
├── docker-compose.yml         # local environment (services + dependencies)
├── .env.example               # example variables (NEVER upload real .env)
├── requirements.lock          # dependency lock (optional)
│
├── apps/
│   ├── chat-api/              # Public FastAPI (RAG orchestration + sessions)
│   │   ├── app/
│   │   │   ├── main.py        # FastAPI startup + routers + middlewares
│   │   │   ├── api/
│   │   │   │   ├── routes_chat.py      # /chat, /stream, /health
│   │   │   │   └── routes_admin.py     # /configs, /reindex (protected)
│   │   │   ├── core/
│   │   │   │   ├── config.py           # env vars reading
│   │   │   │   ├── logging.py          # logging configuration
│   │   │   │   └── security.py         # auth/jwt/cors
│   │   │   ├── services/
│   │   │   │   ├── rag_orchestrator.py # calls search-service and llm-service
│   │   │   │   └── citations.py        # formats citations/metadata
│   │   │   ├── db/
│   │   │   │   ├── models.py           # SQLAlchemy: users, sessions, messages...
│   │   │   │   ├── schema.sql          # (optional) pure SQL
│   │   │   │   └── repository.py       # CRUD and helpers
│   │   │   ├── schemas/                # Pydantic request/response
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── pyproject.toml / requirements.txt
│   │
│   ├── search-service/        # Internal API for semantic search
│   │   ├── app/
│   │   │   ├── main.py        # endpoints: /search, /upsert, /delete
│   │   │   ├── adapters/
│   │   │   │   ├── pinecone_adapter.py # implements VectorStore interface
│   │   │   │   ├── qdrant_adapter.py   # (optional)
│   │   │   │   └── opensearch_adapter.py# (optional)
│   │   │   ├── core/
│   │   │   │   ├── vectorstore.py      # common interface (search, upsert)
│   │   │   │   └── ranking.py          # hybrid re-rank/BM25 (optional)
│   │   │   ├── models/
│   │   │   │   └── types.py            # dataclasses for chunks/metadata
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── llm-service/           # Internal API for LLMs (chat + embeddings)
│   │   ├── app/
│   │   │   ├── main.py        # /generate (stream and non-stream), /embed
│   │   │   ├── providers/
│   │   │   │   ├── bedrock.py # Claude/Titan (boto3)
│   │   │   │   ├── openai.py  # GPT APIs
│   │   │   │   └── ollama.py  # local (optional)
│   │   │   ├── core/
│   │   │   │   ├── prompt_templates/
│   │   │   │   │   ├── financial_qa.j2 # jinja template
│   │   │   │   │   └── system_policies.md
│   │   │   │   └── generation.py       # orchestrates provider + streaming
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── doc-processor/         # batch jobs for ingestion/embeddings
│   │   ├── app/
│   │   │   ├── main.py        # CLI: backfill, incremental, reindex
│   │   │   ├── ingestion/
│   │   │   │   ├── s3_scanner.py       # finds new PDFs
│   │   │   │   └── metadata_parser.py  # parses names/dates/company
│   │   │   ├── processing/
│   │   │   │   ├── pdf_to_text.py      # extraction (pymupdf/pdfminer)
│   │   │   │   ├── clean_text.py       # normalization
│   │   │   │   ├── chunker.py          # chunking (configurable size/overlap)
│   │   │   ├── embeddings/
│   │   │   │   ├── embedder.py         # calls llm-service / direct provider
│   │   │   │   └── schema.py           # vector structure + metadata
│   │   │   ├── indexing/
│   │   │   │   └── upsert_vectors.py   # inserts into Vector DB (batch)
│   │   │   ├── db/
│   │   │   │   ├── models.py           # ingestion_runs, document_versions
│   │   │   │   └── repository.py
│   │   │   ├── config.py
│   │   │   ├── tests/
│   │   │   └── Dockerfile
│   │   └── requirements.txt
│   │
│   └── frontend/              # Streamlit (MVP) or React (production)
│       ├── streamlit_app/     # app.py, pages/, components/
│       ├── react_app/         # (optional) Next.js/CRA
│       └── Dockerfile
│
├── infra/
│   ├── local/
│   │   ├── docker/            # configs, healthchecks
│   │   └── compose/           # compose files per environment
│   ├── aws/
│   │   ├── deployment/        # scripts/configs for deploy in AWS (EC2, ALB, etc.)
│   │   ├── rds/               # parameters/migrations
│   │   ├── opensearch/        # if used
│   │   └── terraform/         # IaC (optional)
│   └── scripts/
│       ├── deploy.sh          # generic deploy script (EC2 or registry)
│       ├── build_images.sh
│       └── migrate_db.py
│
├── migrations/                # alembic or plain SQL
├── tests/                     # e2e and shared utilities
└── docs/                      # diagrams, architecture decisions (ADR)
```

---

## LOCAL DEVELOPMENT - STEP BY STEP SETUP

### Prerequisites
- Python 3.11+
- Docker + Docker Compose
- Git
- 16GB RAM recommended
- AWS CLI (for deployment)

### 1. Quick Start
```bash
# 1. Clone and setup
git clone <repo-url>
cd financial-ai-chatbot

# 2. Complete development setup (automated script)
python scripts/dev_setup.py

# 3. Verify everything works
python scripts/health_check.py

# 4. Access application
# Frontend: http://localhost:8501
# Chat API: http://localhost:8000/docs
# Search Service: http://localhost:8001/docs
# LLM Service: http://localhost:8002/docs
```

### 2. Docker Compose (Local Development)
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
    profiles: ["processing"]  # Only runs manually

volumes:
  postgres_data:
```

### 3. Environment Variables (.env)
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

## DETAILED DATA FLOW

### 1. Knowledge Pipeline (Background)
```
PDFs in S3 → Doc Processor → Text extraction → Chunking
                ↓
        Embedding generation → Upsert Pinecone → Update PostgreSQL metadata
```

### 2. RAG Flow (Online)
```
User query → Chat API → Search Service → Pinecone (top-k chunks)
                   ↓
            Prompt Template + Context → LLM Service → Streamed response
                   ↓
            Save history + Return response + Citations
```

### 3. Session Management
```
User → Chat API → Check/Create session → Load historical context
                        ↓
                   RAG process + Add to context → Update session
```

---

## Production & Deployment Notes

- Production is currently run on an AWS EC2 instance. The simplest production model is to run the same containers there using Docker Compose or a container runtime and keep secrets in AWS Secrets Manager.
- You can add a CI/CD pipeline (GitHub Actions) later to build images and deploy to the EC2 host. Detailed instructions for ECS/ECR have been removed to keep this guide focused on the current setup.
- Monitoring should be integrated with CloudWatch or your preferred observability backend.

---

## SUCCESS CRITERIA

### Technical
- ✅ RAG system responding to relevant NASDAQ questions
- ✅ Responses with verifiable citations and metadata
- ✅ Performance < 3 seconds per query
- ✅ System deployed in AWS with high availability
- ✅ Automated CI/CD working
- ✅ Automated tests > 80% critical coverage

### Learning
- ✅ Each person masters their technical domain
- ✅ Everyone understands the complete architecture and RAG flow
- ✅ Experience with enterprise technologies (Docker, ECS, microservices)
- ✅ Impressive portfolio project for interviews
- ✅ Professional quality technical documentation

### Functional
- ✅ Chatbot responds to specific financial questions
- ✅ Handles multiple simultaneous sessions
- ✅ Intuitive ChatGPT-style interface
- ✅ Administration system for reindexing
- ✅ Monitoring and alerts working

---


## SUCCESS METRICS

### Technical KPIs
- **Average latency**: < 3 seconds end-to-end
- **Availability**: > 99% uptime in production
- **RAG accuracy**: > 80% relevant responses (manual evaluation)
- **Test coverage**: > 80% in critical services
- **Error rate**: < 5% of failed requests

### Learning KPIs
- **Contributions**: Each person must have significant commits in their area
- **Code review participation**: 100% PRs reviewed by at least 2 people
- **Documentation**: Complete API docs + documented architecture decisions
- **Knowledge sharing**: Each person presents their module to the team (15 min each)

---

## QUICK REFERENCE - ESSENTIAL COMMANDS

### Local Development
```bash
# Complete initial setup
python scripts/dev_setup.py

# Start all services
docker-compose up -d

# View logs in real time
docker-compose logs -f chat-api

# Run tests
docker-compose exec chat-api pytest

# Process documents (manual)
docker-compose run --rm doc-processor python -m app.main backfill

# Check health of all services
python scripts/health_check.py

# Clean and restart
docker-compose down -v && docker-compose up -d
```

### Commands by Service
```bash
# Chat API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query":"What is Apple revenue?","session_id":"test"}'

# Search Service
curl -X POST http://localhost:8001/search -H "Content-Type: application/json" -d '{"query":"Apple revenue","top_k":5}'

# LLM Service
curl -X POST http://localhost:8002/generate -H "Content-Type: application/json" -d '{"prompt":"Hello","model":"claude-3-sonnet"}'
```

---

## DATA STRUCTURES - KEY SCHEMAS

### PostgreSQL Schema
```sql
-- Users and sessions
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

-- Document catalog
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

-- Processing control
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

-- System configurations
CREATE TABLE system_configs (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Vector Metadata Schema (Pinecone)
```python
# Metadata stored with each chunk vector
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

## DETAILED API CONTRACTS

### Chat API (Port 8000)
```python
# POST /chat
{
    "session_id": "uuid-optional",
    "query": "What was Apple's revenue in 2023?",
    "company_filters": ["AAPL", "MSFT"],  # optional
    "top_k": 8,  # optional, default from config
    "stream": false  # optional
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

### Search Service (Port 8001)
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
    "min_score": 0.7  # optional
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

### LLM Service (Port 8002)
```python
# POST /generate
{
    "prompt": "Based on the context: [CONTEXT], answer: What was Apple's revenue?",
    "model": "claude-3-5-sonnet",  # or "gpt-4o"
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