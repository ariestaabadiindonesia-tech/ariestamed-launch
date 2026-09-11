# Deployment Guide - Ariestamed Launch

## Prerequisites
- Docker & Docker Compose
- PostgreSQL 12+
- Redis 6+
- Domain name (optional)
- SSL Certificate (optional but recommended)

## Deployment Options

### Option 1: Docker Compose (Recommended for Production)

1. **Clone repository**
```bash
git clone https://github.com/ariestaabadiindonesia-tech/ariestamed-launch.git
cd ariestamed-launch
```

2. **Setup environment**
```bash
cp .env.example .env
# Edit .env with production values
```

3. **Start services**
```bash
docker-compose -f docker-compose.yml up -d
```

4. **Run migrations**
```bash
docker-compose exec backend flask db upgrade
```

5. **Verify installation**
```bash
curl http://localhost:5000/api/health
```

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Login to Heroku**
```bash
heroku login
```

3. **Create app**
```bash
heroku create ariestamed-launch
```

4. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Add Redis addon**
```bash
heroku addons:create heroku-redis:premium-0
```

6. **Set environment variables**
```bash
heroku config:set FLASK_ENV=production
heroku config:set OPENAI_API_KEY=your-key
# ... set other variables
```

7. **Deploy**
```bash
git push heroku main
```

### Option 3: AWS (EC2 + RDS + ElastiCache)

1. **Launch EC2 instance** (t3.medium minimum)
2. **Setup RDS PostgreSQL** database
3. **Setup ElastiCache Redis** cluster
4. **Install dependencies** on EC2
5. **Clone and configure** application
6. **Use Gunicorn** for production WSGI
7. **Setup Nginx** reverse proxy
8. **Configure SSL** with Let's Encrypt

## Production Configuration

### Environment Variables
```bash
# Flask
FLASK_ENV=production
FLASK_SECRET_KEY=<secure-random-key>

# Database
DATABASE_URL=postgresql://user:pass@host:5432/ariestamed
REDIS_URL=redis://host:6379/0

# OpenAI
OPENAI_API_KEY=<your-key>

# Platform APIs
YOUTUBE_API_KEY=<your-key>
FACEBOOK_APP_ID=<your-id>
INSTAGRAM_BUSINESS_ACCOUNT_ID=<your-id>
TIKTOK_CLIENT_KEY=<your-key>

# Security
ALLOWED_HOSTS=yourdomain.com
CORS_ORIGINS=yourdomain.com
```

### Security Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong secret keys
- [ ] Enable HTTPS/SSL
- [ ] Setup firewall rules
- [ ] Enable database backups
- [ ] Setup monitoring/logging
- [ ] Configure rate limiting
- [ ] Setup fail2ban for DDoS protection

### Database Backups

```bash
# Automated daily backups
0 2 * * * pg_dump -U user -d ariestamed > /backup/ariestamed_$(date +\%Y\%m\%d).sql
```

### Monitoring

- Setup error tracking (Sentry)
- Monitor logs (ELK Stack)
- Setup alerts for key metrics
- Monitor CPU/Memory usage
- Monitor database performance

## Scaling Considerations

### Horizontal Scaling
- Run multiple backend instances
- Use load balancer (HAProxy, Nginx)
- Shared PostgreSQL database
- Shared Redis cache

### Vertical Scaling
- Upgrade server resources
- Optimize database queries
- Add caching layers
- Use CDN for static files

## Troubleshooting

### Application won't start
1. Check logs: `docker-compose logs -f backend`
2. Verify database connection
3. Run migrations
4. Check environment variables

### High latency
1. Check database query performance
2. Verify Redis connection
3. Review slow query logs
4. Consider adding caching

### Memory issues
1. Monitor Celery workers
2. Check for memory leaks
3. Limit Celery concurrency
4. Increase available memory
