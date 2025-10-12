<<<<<<< HEAD
﻿# NASDAQ Financial Advisor - AI Chatbot with Sentiment Analysis

An intelligent conversational assistant focused on financial analysis and consultation of NASDAQ-listed companies. The system integrates real-time sentiment analysis with LLM-powered responses to provide comprehensive financial insights.

## 🎯 **Project Overview**

This project delivers a complete chatbot system that:
- Provides intelligent responses about NASDAQ companies using AWS Bedrock (Claude 3 Haiku)
- Performs real-time sentiment analysis on user messages using VADER, TextBlob, and OpenAI GPT
- Offers an admin dashboard with analytics and metrics
- Supports multi-user authentication and conversation management
- Containerized architecture with Docker for easy deployment

## 🏗️ **Architecture**

The system consists of four main services:

1. **Chat API** (FastAPI) - Main conversational interface with LLM integration
2. **Sentiment Analysis API** (FastAPI) - Real-time sentiment analysis service
3. **Frontend** (React + TypeScript) - User interface and admin dashboard
4. **PostgreSQL** - Shared database for all services

```
┌─────────────────┐
│   Frontend      │ (React + Vite)
│   Port: 5173    │
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┐
         │                 │                 │
┌────────▼────────┐ ┌──────▼──────┐ ┌───────▼────────┐
│   Chat API      │ │ Sentiment   │ │   PostgreSQL   │
│   Port: 8000    │ │   API       │ │   Port: 5433   │
│                 │ │ Port: 8001  │ │                │
└─────────────────┘ └─────────────┘ └────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**

- Docker Desktop (Windows/Mac) or Docker + Docker Compose (Linux)
- Git
- OpenAI API Key (for sentiment analysis)
- AWS Credentials (for Bedrock LLM service)
- Pinecone API Key (for document search)

### **Step 1: Clone the Repository**

```bash
git clone <your-repository-url>
cd nasdaq-financial-advisor
```

### **Step 2: Configure Environment Variables**

Create `.env` files from the provided examples:

#### **Root `.env` (Main Configuration)**

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# AWS Bedrock Configuration
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=financial-docs

# PostgreSQL Configuration (defaults are fine for local development)
POSTGRES_USER=chatapi_user
POSTGRES_PASSWORD=chatapi_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=chatapi_db

# Application Settings
DEBUG=true
ENVIRONMENT=development

# Admin User (auto-created on startup)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Admin1234
ADMIN_EMAIL=admin@gmail.com
CREATE_ADMIN_ON_STARTUP=true
```

#### **Chat API `.env`**

```bash
cp apps/chat-api/.env.example apps/chat-api/.env
```

Edit `apps/chat-api/.env`:

```env
# AWS Configuration (same as root .env)
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_MAX_TOKENS=4096
BEDROCK_TEMPERATURE=0.7

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=financial-docs

# Database Configuration
POSTGRES_USER=chatapi_user
POSTGRES_PASSWORD=chatapi_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chatapi_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# LLM Provider
LLM_PROVIDER=bedrock
DEFAULT_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

#### **Sentiment API `.env`**

```bash
cp sentiment_analysis/.env.example sentiment_analysis/.env
```

Edit `sentiment_analysis/.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=chatapi_user
POSTGRES_PASSWORD=chatapi_password
POSTGRES_DB=chatapi_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=true

# LLM Configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.7
```

#### **Frontend `.env`**

```bash
cp frontend/.env.example frontend/.env
```

Edit `frontend/.env`:

```env
VITE_CHAT_API_URL=http://localhost:8000
VITE_SENTIMENT_API_URL=http://localhost:8001
```

### **Step 3: Build and Start the Services**

```bash
# Build all Docker images
docker-compose build
=======

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
>>>>>>> origin/develop

# Start all services
docker-compose up -d

<<<<<<< HEAD
# View logs (optional)
docker-compose logs -f
```

### **Step 4: Verify Services are Running**

```bash
# Check container status
docker ps

# You should see 4 containers running:
# - chatapi-frontend (port 5173)
# - chatapi-backend (port 8000)
# - sentiment-analysis (port 8001)
# - chatapi-postgres (port 5433)
```

### **Step 5: Access the Application**

- **Frontend UI**: http://localhost:5173
- **Chat API Docs**: http://localhost:8000/docs
- **Sentiment API Docs**: http://localhost:8001/docs
- **Admin Dashboard**: http://localhost:5173 (login with admin credentials)

## 👥 **Default Users**

### **Admin User**
- Email: `admin@gmail.com`
- Password: `Admin1234`

You can create new users through the registration modal in the UI.

## 🔧 **Development**

### **Running Individual Services**

```bash
# Start only the database
docker-compose up -d postgres

# Start chat-api
docker-compose up -d chat-api

# Start sentiment-api
docker-compose up -d sentiment-api

# Start frontend
docker-compose up -d frontend
```

### **Viewing Logs**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f chat-api
docker-compose logs -f sentiment-api
docker-compose logs -f frontend
```

### **Rebuilding After Code Changes**

```bash
# Rebuild specific service
docker-compose build chat-api

# Rebuild and restart
docker-compose up -d --build chat-api
```

### **Stopping Services**

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes database data)
docker-compose down -v
```

## 📊 **Features**

### **Chat Interface**
- Real-time messaging with AI assistant
- Conversation history and management
- Multi-session support
- Context-aware responses about NASDAQ companies

### **Sentiment Analysis**
- Automatic sentiment detection on user messages
- VADER sentiment scores (positive, negative, neutral, compound)
- TextBlob polarity and subjectivity analysis
- Optional LLM explanations for emotional content
- Smart feedback system for complex queries

### **Admin Dashboard**
- Real-time sentiment metrics and analytics
- Visual charts for sentiment trends
- Recent analysis records table
- User activity monitoring

### **Authentication**
- JWT-based secure authentication
- User registration and login
- Session persistence
- Protected routes and admin-only access

## 🗄️ **Database Schema**

### **Users Table**
```sql
- id (Primary Key)
- name
- email (Unique)
- hashed_password
- is_active
- created_at
- updated_at
```

### **Conversations Table**
```sql
- id (Primary Key)
- session_id (Unique)
- title
- user_id (Foreign Key -> Users)
- created_at
- updated_at
```

### **Messages Table**
```sql
- id (Primary Key)
- conversation_id (Foreign Key -> Conversations)
- role (user/assistant)
- content
- created_at
- updated_at
```

### **Analysis Table** (Sentiment API)
```sql
- id (Primary Key)
- text
- sentiment_pos
- sentiment_neg
- sentiment_neu
- sentiment_compound
- polarity
- subjectivity
- llm_explanation
- user_id
- created_at
```

## 🧪 **Testing**

### **API Endpoints Testing**

```bash
# Health check - Chat API
curl http://localhost:8000/health

# Health check - Sentiment API
curl http://localhost:8001/health

# Register new user
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Sentiment Analysis
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am very excited about this investment opportunity!",
    "explain_with_llm": true,
    "user_id": 1
  }'
```

## 🐛 **Troubleshooting**

### **Database Connection Issues**

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### **Port Already in Use**

If you get port conflict errors, modify the ports in `docker-compose.yml`:

```yaml
services:
  postgres:
    ports:
      - "5434:5432"  # Change from 5433 to 5434
  
  chat-api:
    ports:
      - "8080:8000"  # Change from 8000 to 8080
```

### **Frontend Not Loading**

```bash
# Rebuild frontend
docker-compose build --no-cache frontend

# Restart frontend
docker-compose up -d frontend

# Check logs
docker-compose logs -f frontend
```

### **Sentiment API Timeout**

```bash
# Check if sentiment-api is healthy
curl http://localhost:8001/health

# Restart sentiment-api
docker-compose restart sentiment-api

# View detailed logs
docker-compose logs -f sentiment-api
```

## 📦 **Tech Stack**

### **Backend**
- FastAPI (Python 3.9/3.10)
- SQLAlchemy ORM
- PostgreSQL 15
- JWT Authentication (python-jose)
- AWS Bedrock (Claude 3 Haiku)
- OpenAI GPT-4o-mini
- VADER Sentiment Analyzer
- TextBlob
- Pinecone Vector Database

### **Frontend**
- React 18
- TypeScript
- Vite
- CSS Modules
- Fetch API

### **DevOps**
- Docker & Docker Compose
- Multi-stage builds
- Health checks
- Volume persistence

## 📝 **API Documentation**

Once the services are running, interactive API documentation is available:

- **Chat API**: http://localhost:8000/docs
- **Sentiment API**: http://localhost:8001/docs

## 🔐 **Security Notes**

⚠️ **For Production Deployment:**

1. Change all default passwords and secret keys
2. Use environment-specific `.env` files
3. Enable HTTPS/TLS
4. Configure proper CORS origins
5. Use managed PostgreSQL service
6. Implement rate limiting
7. Add proper logging and monitoring
8. Use secrets management (AWS Secrets Manager, etc.)

## 🤝 **Contributing**

This project was developed as part of the AnyoneAI ML Developer Career program.

## 📄 **License**

This project is developed for educational purposes.

## 👨‍💻 **Author**

Developed as the Final Project for the ML Developer Career Program.

---

**Need Help?** Check the troubleshooting section or review the logs with `docker-compose logs -f`
=======
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
>>>>>>> origin/develop
