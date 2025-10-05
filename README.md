# NASDAQ Financial Advisor - AI Chatbot with Sentiment Analysis

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

# Start all services
docker-compose up -d

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