# Deployment Guide

This guide covers different deployment options for the AI Customer Support Agent.

## Quick Deployment Options

### 1. Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

### 2. Docker Deployment (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - APPWRITE_PROJECT_ID=${APPWRITE_PROJECT_ID}
      - APPWRITE_API_KEY=${APPWRITE_API_KEY}
      - APPWRITE_ENDPOINT=${APPWRITE_ENDPOINT}
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
```

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Deploy:
```bash
docker-compose up --build
```

## Cloud Deployment Options

### 1. Vercel (Frontend) + Railway/Render (Backend)

**Frontend (Vercel):**
1. Connect your GitHub repo to Vercel
2. Set build command: `npm run build`
3. Set output directory: `build`
4. Add environment variable: `REACT_APP_API_URL=https://your-backend-url.com`

**Backend (Railway):**
1. Connect GitHub repo to Railway
2. Set root directory: `backend`
3. Railway will auto-detect Python and use `requirements.txt`
4. Add environment variables:
   - `GEMINI_API_KEY`
   - `APPWRITE_PROJECT_ID`
   - `APPWRITE_API_KEY`
   - `APPWRITE_ENDPOINT`

### 2. Netlify (Frontend) + Heroku (Backend)

**Frontend (Netlify):**
```bash
# Build settings
npm run build
```

Add `frontend/_redirects`:
```
/api/* https://your-backend-app.herokuapp.com/api/:splat 200
/*    /index.html   200
```

**Backend (Heroku):**

Create `backend/Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Deploy:
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_key
heroku config:set APPWRITE_PROJECT_ID=your_project_id
# ... other env vars
git subtree push --prefix backend heroku main
```

### 3. AWS Deployment

**Backend (AWS Lambda + API Gateway):**

Install serverless framework:
```bash
npm install -g serverless
```

Create `backend/serverless.yml`:
```yaml
service: ai-customer-support-backend

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    GEMINI_API_KEY: ${env:GEMINI_API_KEY}
    APPWRITE_PROJECT_ID: ${env:APPWRITE_PROJECT_ID}
    APPWRITE_API_KEY: ${env:APPWRITE_API_KEY}

functions:
  app:
    handler: lambda_handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true

plugins:
  - serverless-python-requirements
```

Create `backend/lambda_handler.py`:
```python
from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="off")
```

Deploy:
```bash
serverless deploy
```

**Frontend (AWS S3 + CloudFront):**
```bash
npm run build
aws s3 sync build/ s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

### 4. Google Cloud Platform

**Backend (Cloud Run):**

Create `backend/cloudbuild.yaml`:
```yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/ai-support-backend', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/ai-support-backend']
- name: 'gcr.io/cloud-builders/gcloud'
  args: ['run', 'deploy', 'ai-support-backend', '--image', 'gcr.io/$PROJECT_ID/ai-support-backend', '--platform', 'managed', '--region', 'us-central1']
```

Deploy:
```bash
gcloud builds submit --config cloudbuild.yaml
```

**Frontend (Firebase Hosting):**
```bash
npm install -g firebase-tools
firebase init hosting
npm run build
firebase deploy
```

## Environment Variables

Create a `.env.production` file for production settings:

```env
# Production Environment Variables

# Gemini API
GEMINI_API_KEY=your_production_gemini_key

# Appwrite
APPWRITE_PROJECT_ID=your_production_project_id
APPWRITE_API_KEY=your_production_api_key
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1

# App Configuration
ENVIRONMENT=production
DEBUG=false

# Security (add these for production)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Production Considerations

### 1. Security

**Backend Security:**
- Use HTTPS only
- Set proper CORS origins
- Validate all inputs
- Rate limiting
- API key rotation

**Frontend Security:**
- Content Security Policy (CSP)
- Secure cookies
- Input sanitization
- Environment variable protection

### 2. Performance

**Backend Optimization:**
- Enable response caching
- Use connection pooling
- Optimize database queries
- Implement pagination

**Frontend Optimization:**
- Code splitting
- Image optimization
- CDN for static assets
- Service worker for caching

### 3. Monitoring

Set up monitoring with:
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Uptime monitoring
- Log aggregation

### 4. Scaling

**Backend Scaling:**
- Horizontal scaling with load balancer
- Database connection pooling
- Caching layer (Redis)
- CDN for API responses

**Frontend Scaling:**
- CDN distribution
- Image optimization
- Bundle optimization
- Progressive loading

## Health Checks

Implement health check endpoints:

**Backend Health Check:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "gemini": "connected" if not gemini_service.use_mock else "mock",
            "appwrite": "connected" if not appwrite_service.use_mock else "mock"
        }
    }
```

**Frontend Health Check:**
Add to `frontend/public/health.json`:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## CI/CD Pipeline

Example GitHub Actions workflow (`.github/workflows/deploy.yml`):

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          pytest
      
      - name: Test Frontend
        run: |
          cd frontend
          npm install
          npm test -- --watchAll=false

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        # Add your backend deployment steps
        
      - name: Deploy Frontend
        # Add your frontend deployment steps
```

## Backup and Recovery

### Database Backup (Appwrite)
- Set up automated backups in Appwrite console
- Export conversation data regularly
- Test recovery procedures

### Application Backup
- Version control for code
- Configuration backup
- Environment variable backup (encrypted)

## Troubleshooting Deployment

### Common Issues:

1. **CORS Errors**: Update CORS origins in backend
2. **API Key Issues**: Check environment variable configuration
3. **Build Failures**: Verify Node.js/Python versions
4. **Database Connection**: Check Appwrite configuration
5. **Memory Issues**: Increase container memory limits

### Debugging Steps:

1. Check application logs
2. Verify environment variables
3. Test API endpoints individually
4. Check network connectivity
5. Validate SSL certificates

For specific deployment platform issues, refer to their documentation:
- [Vercel Docs](https://vercel.com/docs)
- [Netlify Docs](https://docs.netlify.com)
- [Railway Docs](https://docs.railway.app)
- [Heroku Docs](https://devcenter.heroku.com)
- [AWS Docs](https://docs.aws.amazon.com)
- [Google Cloud Docs](https://cloud.google.com/docs)