# Troubleshooting Guide - Ariestamed Launch

## Common Issues

### Backend Issues

#### Port 5000 already in use
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
FLASK_PORT=5001 python -m flask run
```

#### Database connection error
```
Error: could not connect to server
```

**Solutions:**
1. Verify PostgreSQL is running
2. Check connection string in .env
3. Verify credentials are correct
4. Check firewall rules
5. Run migrations: `flask db upgrade`

#### Redis connection error
```
Error: Error -3 connecting to localhost:6379
```

**Solutions:**
1. Verify Redis is running: `redis-cli ping`
2. Check REDIS_URL in .env
3. Restart Redis: `redis-server`
4. Check firewall rules

### Frontend Issues

#### Blank page or 404
1. Check browser console for errors
2. Verify backend is running
3. Check REACT_APP_API_URL
4. Clear browser cache
5. Check network tab for API errors

#### API 401 Unauthorized
1. Clear localStorage (dev tools)
2. Login again
3. Check token expiration
4. Verify JWT_SECRET_KEY in backend

#### CORS errors
```
Access to XMLHttpRequest blocked by CORS
```

**Solution:** Update `.env`
```
CORS_ORIGINS=http://localhost:3000
```

### API Errors

#### 400 Bad Request
- Check request parameters
- Verify Content-Type header
- Validate input data

#### 404 Not Found
- Verify resource exists
- Check resource ID
- Verify you own the resource

#### 500 Server Error
1. Check backend logs: `docker-compose logs backend`
2. Check database connection
3. Verify all environment variables
4. Check Celery worker status

### Content Generation Issues

#### AI generation not working
1. Verify OpenAI API key is valid
2. Check account has credits
3. Review rate limits
4. Check task logs: `docker-compose logs celery_worker`

#### Slow content generation
1. Check Celery worker logs
2. Verify Redis connection
3. Check OpenAI API latency
4. Review queue length

### Posting Issues

#### Posts not publishing
1. Verify platform credentials are active
2. Check OAuth tokens haven't expired
3. Review API rate limits
4. Check post status in database
5. Review Celery worker logs

#### Platform authentication errors
- Re-authenticate account
- Verify permissions are granted
- Check OAuth scope settings
- Verify app credentials

### Analytics Issues

#### No analytics data showing
1. Wait 24-48 hours for initial data
2. Verify posts are published
3. Check platform API access
4. Manually trigger analytics refresh
5. Verify database contains analytics records

#### Incorrect metrics
1. Verify platform API responses
2. Check metric calculation logic
3. Clear cache: `redis-cli FLUSHALL`
4. Re-fetch analytics

## Performance Optimization

### Database
- Add indexes on frequently queried columns
- Optimize slow queries
- Regular VACUUM and ANALYZE
- Use connection pooling

### Caching
- Cache API responses
- Cache user data
- Use Redis for sessions
- Cache product/content lists

### API
- Add pagination to list endpoints
- Implement request rate limiting
- Use compression
- Minimize response size

## Monitoring

### Logs to Check
```bash
# Backend logs
docker-compose logs -f backend

# Celery worker logs
docker-compose logs -f celery_worker

# Database logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis
```

### Health Checks
```bash
# API health
curl http://localhost:5000/api/health

# Database
psql -U ariestamed -d ariestamed -c "SELECT 1"

# Redis
redis-cli ping

# Celery
celery -A app.tasks inspect active
```

## Getting Help

1. Check this guide
2. Review error messages carefully
3. Check logs
4. Search GitHub issues
5. Ask in community Discord
6. Contact support

## Reporting Bugs

When reporting bugs, include:
1. Error message (full text)
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment info (OS, Python version, etc.)
6. Relevant logs
