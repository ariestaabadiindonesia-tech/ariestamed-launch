# Setup Guide - Ariestamed Launch

## Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- Git

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/ariestaabadiindonesia-tech/ariestamed-launch.git
cd ariestamed-launch
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Edit .env with your credentials
nano .env

# Run migrations
flask db upgrade

# Start Flask server
python -m flask run
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000" > .env

# Start development server
npm start
```

### 4. Celery Worker Setup (separate terminal)

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A tasks worker --loglevel=info
```

### 5. Celery Beat Setup (separate terminal for scheduling)

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Start Celery Beat
celery -A tasks beat --loglevel=info
```

## Database Setup

```bash
cd backend

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## API Credentials Setup

### YouTube
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Add credentials to .env

### Instagram/Facebook
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create app
3. Configure Facebook Login
4. Generate access tokens
5. Add to .env

### TikTok
1. Go to [TikTok Developer](https://developer.tiktok.com/)
2. Create developer account
3. Apply for TikTok API access
4. Get credentials
5. Add to .env

### OpenAI
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Generate API key
3. Add to .env

## Using Docker

```bash
# Start all services
docker-compose up

# Access services:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

## Verify Installation

```bash
# Check backend
curl http://localhost:5000/api/health

# Check frontend
visit http://localhost:3000
```

## Next Steps

1. Create user account
2. Add digital products
3. Configure platform credentials
4. Generate content
5. Schedule posts
6. Monitor analytics
