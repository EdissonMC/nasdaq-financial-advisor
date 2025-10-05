# 🚀 Deployment Guide - NASDAQ Financial Advisor

This guide provides step-by-step instructions for deploying the NASDAQ Financial Advisor system.

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Production Deployment](#production-deployment)
3. [Environment Variables Reference](#environment-variables-reference)
4. [Common Issues](#common-issues)

---

## 🖥️ Local Development Setup

### Prerequisites

Ensure you have the following installed:

- **Docker Desktop** (Windows/Mac) or **Docker + Docker Compose** (Linux)
  - Download: https://www.docker.com/products/docker-desktop
- **Git**
  - Download: https://git-scm.com/downloads
- **Text Editor** (VS Code recommended)

### API Keys Required

You'll need to sign up for the following services and obtain API keys:

1. **OpenAI** (for sentiment analysis)
   - Sign up: https://platform.openai.com/signup
   - Get API key: https://platform.openai.com/api-keys

2. **AWS** (for Bedrock LLM service)
   - Sign up: https://aws.amazon.com/
   - Create IAM user with Bedrock permissions
   - Generate access keys

3. **Pinecone** (for vector database)
   - Sign up: https://www.pinecone.io/
   - Create index named `financial-docs`
   - Get API key from dashboard

### Step-by-Step Setup

#### 1. Clone Repository

```bash
git clone <repository-url>
cd nasdaq-financial-advisor
```

#### 2. Create Environment Files

```bash
# Root .env
cp .env.example .env

# Chat API .env
cp apps/chat-api/.env.example apps/chat-api/.env

# Sentiment API .env
cp sentiment_analysis/.env.example sentiment_analysis/.env

# Frontend .env
cp frontend/.env.example frontend/.env
```

#### 3. Configure Credentials

Edit each `.env` file and add your API keys:

**Root `.env`:**
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_API_KEY=pcsk_xxxxxxxxxxxxx
```

**`apps/chat-api/.env`:**
```env
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_API_KEY=pcsk_xxxxxxxxxxxxx
SECRET_KEY=$(openssl rand -hex 32)  # Generate secure key
```

**`sentiment_analysis/.env`:**
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**`frontend/.env`:**
```env
VITE_CHAT_API_URL=http://localhost:8000
VITE_SENTIMENT_API_URL=http://localhost:8001
```

#### 4. Start Services

```bash
# Build all images (first time only)
docker-compose build

# Start all services
docker-compose up -d

# Verify all containers are running
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                    STATUS          PORTS
xxxxx          chatapi-frontend         Up 10 seconds   0.0.0.0:5173->5173/tcp
xxxxx          chatapi-backend          Up 10 seconds   0.0.0.0:8000->8000/tcp
xxxxx          sentiment-analysis       Up 10 seconds   0.0.0.0:8001->8001/tcp
xxxxx          chatapi-postgres         Up 10 seconds   0.0.0.0:5433->5432/tcp
```

#### 5. Access Application

- **Frontend**: http://localhost:5173
- **Chat API Docs**: http://localhost:8000/docs
- **Sentiment API Docs**: http://localhost:8001/docs

#### 6. Login

Use the default admin credentials:
- Email: `admin@gmail.com`
- Password: `Admin1234`

---

## 🌐 Production Deployment

### Using Docker Compose (Recommended for Simple Deployments)

#### 1. Update Environment Variables

Create production `.env` files with secure credentials:

```env
# Use strong passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -hex 32)

# Set environment to production
ENVIRONMENT=production
DEBUG=false

# Use production-grade API keys
OPENAI_API_KEY=sk-prod-xxxxx
```

#### 2. Configure CORS for Production Domain

Edit `apps/chat-api/.env`:
```env
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

#### 3. Use Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  chat-api:
    build: ./apps/chat-api
    restart: always
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    depends_on:
      - postgres
    networks:
      - app-network

  sentiment-api:
    build: ./sentiment_analysis
    restart: always
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    depends_on:
      - postgres
    networks:
      - app-network

  frontend:
    build:
      context: ./frontend
      target: runner  # Production build
    restart: always
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - chat-api
      - sentiment-api
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

#### 4. Deploy

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Using Kubernetes (Advanced)

For Kubernetes deployment, refer to the `k8s/` directory (if available) or contact the development team.

---

## 📚 Environment Variables Reference

### Root `.env`

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for sentiment analysis | Yes | - |
| `AWS_REGION` | AWS region for Bedrock | Yes | us-west-2 |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes | - |
| `PINECONE_API_KEY` | Pinecone API key | Yes | - |
| `PINECONE_ENVIRONMENT` | Pinecone environment | Yes | us-east-1 |
| `PINECONE_INDEX_NAME` | Pinecone index name | Yes | financial-docs |
| `POSTGRES_USER` | PostgreSQL username | No | chatapi_user |
| `POSTGRES_PASSWORD` | PostgreSQL password | No | chatapi_password |
| `POSTGRES_HOST` | PostgreSQL host | No | 127.0.0.1 |
| `POSTGRES_PORT` | PostgreSQL port | No | 5433 |
| `POSTGRES_DB` | PostgreSQL database name | No | chatapi_db |
| `DEBUG` | Enable debug mode | No | true |
| `ENVIRONMENT` | Environment (development/production) | No | development |

### Chat API `.env`

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | JWT secret key | Yes | - |
| `ALGORITHM` | JWT algorithm | No | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | No | 1440 |
| `LLM_PROVIDER` | LLM provider (bedrock/dummy) | No | bedrock |
| `ALLOWED_ORIGINS` | CORS allowed origins | No | ["http://localhost:5173"] |

### Sentiment API `.env`

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_MODEL` | OpenAI model to use | No | gpt-4o-mini |
| `OPENAI_MAX_TOKENS` | Max tokens for LLM | No | 150 |
| `OPENAI_TEMPERATURE` | LLM temperature | No | 0.7 |

### Frontend `.env`

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_CHAT_API_URL` | Chat API URL | Yes | http://localhost:8000 |
| `VITE_SENTIMENT_API_URL` | Sentiment API URL | Yes | http://localhost:8001 |

---

## 🐛 Common Issues

### Issue: Port Already in Use

**Error:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:5433: bind: address already in use
```

**Solution:**
```bash
# Find process using the port
netstat -ano | findstr :5433  # Windows
lsof -i :5433                 # Mac/Linux

# Kill the process or change the port in docker-compose.yml
```

### Issue: Database Connection Failed

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Issue: OpenAI API Key Invalid

**Error:**
```
openai.error.AuthenticationError: Incorrect API key provided
```

**Solution:**
1. Verify your API key at https://platform.openai.com/api-keys
2. Ensure no extra spaces in `.env` file
3. Restart the sentiment-api container:
   ```bash
   docker-compose restart sentiment-api
   ```

### Issue: AWS Credentials Invalid

**Error:**
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solution:**
1. Verify IAM user has Bedrock permissions
2. Check access key and secret are correct
3. Ensure no trailing spaces in `.env`
4. Restart chat-api:
   ```bash
   docker-compose restart chat-api
   ```

### Issue: Frontend Shows Blank Page

**Solution:**
```bash
# Clear browser cache
# Or rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

---

## 📞 Support

For additional help:
1. Check the main README.md
2. Review API documentation at `/docs` endpoints
3. Check Docker logs: `docker-compose logs -f [service-name]`

---

**Happy Deploying! 🚀**