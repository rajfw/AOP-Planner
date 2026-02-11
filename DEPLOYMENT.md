# Deployment Guide - AOP Planner

## Pre-Deployment Checklist

### 1. Security Audit

#### ⚠️ CRITICAL: Remove Hardcoded Credentials

The current `app.py` contains **hardcoded API credentials** that MUST be removed before deployment:

**Lines 138-139 in app.py:**
```python
api_key="eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im5hbWUiOiJSYWplc3dhciBQIFMiLCJlbWFpbCI6InJhamVzd2FyLnN1YnJhbWFuaUBmcmVzaHdvcmtzLmNvbSIsImltYWdlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0FBUkNWSktyMjhxbU0xRTdnUE1fSlhPcDU4MEZHM2prNThMYzQ1SVB6eVFqN0lxWF89czk2LWMifSwianRpIjoiUGNVU0xxOFNrR3lYdmF1aFlEQTdsIiwiaWF0IjoxNzcwNzg2NTYwLCJleHAiOjE3NzEzOTEzNjB9.JglVKNUeldw7thE2swT0jiXKkf2M3DNUCZZ0WAIAWOg" # REMOVE THIS
base_url="https://cloudverse.freshworkscorp.com/api/v1" # MOVE TO .env
```

**Action Required:**
```python
# Replace with:
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
)
```

#### Update Secret Key
```python
# Line 70 - Change from:
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fw-aop-secret-key-2025')

# To (remove default):
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Then validate it exists at startup
```

### 2. Environment Configuration

Create production `.env` file:

```env
# Production Configuration
SECRET_KEY=<generate-with-python-secrets-token-hex-32>
GOOGLE_CLIENT_ID=<your-production-google-client-id>
GOOGLE_CLIENT_SECRET=<your-production-google-client-secret>
OPENAI_API_KEY=<your-api-key>
OPENAI_BASE_URL=<your-endpoint>
OPENAI_MODEL=<your-model>
FLASK_ENV=production
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Database Migration

**Current State**: JSON file-based storage in `data/` directory

**Production Recommendation**: Migrate to PostgreSQL or MySQL

#### Migration Steps:
1. Design database schema for:
   - Users table
   - Roadmaps table
   - Form configurations table
   - Attachments metadata table

2. Create migration scripts
3. Implement SQLAlchemy models
4. Update data access functions

**Quick Fix for MVP**: Ensure `data/` directory has proper permissions and backup strategy

### 4. File Upload Security

Current configuration:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'doc', 'docx', 'md'}
```

**Production Enhancements**:
- Add virus scanning for uploaded files
- Implement file content validation
- Use cloud storage (S3, GCS) instead of local filesystem
- Add rate limiting on upload endpoints

## Deployment Options

### Option 1: Traditional Server (Ubuntu/Debian)

#### 1. Install Dependencies
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv nginx supervisor
```

#### 2. Setup Application
```bash
# Create app directory
sudo mkdir -p /var/www/aop-planner
sudo chown $USER:$USER /var/www/aop-planner
cd /var/www/aop-planner

# Copy application files
# (upload via git, scp, or rsync)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

#### 3. Configure Gunicorn

Create `/var/www/aop-planner/gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
accesslog = "/var/log/aop-planner/access.log"
errorlog = "/var/log/aop-planner/error.log"
loglevel = "info"
```

#### 4. Configure Supervisor

Create `/etc/supervisor/conf.d/aop-planner.conf`:
```ini
[program:aop-planner]
directory=/var/www/aop-planner
command=/var/www/aop-planner/venv/bin/gunicorn -c gunicorn_config.py app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/aop-planner/err.log
stdout_logfile=/var/log/aop-planner/out.log
```

Start the service:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start aop-planner
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/aop-planner`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/aop-planner/static;
        expires 30d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/aop-planner /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. Setup SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p uploads data

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "--timeout", "120", "app:app"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_BASE_URL=${OPENAI_BASE_URL}
      - OPENAI_MODEL=${OPENAI_MODEL}
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: Cloud Platform (Heroku, Railway, Render)

#### For Heroku:

Create `Procfile`:
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.9.18
```

Deploy:
```bash
heroku create aop-planner
heroku config:set SECRET_KEY=<your-secret>
heroku config:set GOOGLE_CLIENT_ID=<your-id>
# ... set other env vars
git push heroku main
```

## Post-Deployment

### 1. Initialize Data

Create initial admin user:
```bash
# SSH into server or use docker exec
python -c "
import json
import uuid

users = [{
    'id': str(uuid.uuid4()),
    'username': 'admin',
    'name': 'Admin User',
    'email': 'admin@yourcompany.com',
    'role': 'admin',
    'password': 'change-this-password',
    'avatar': 'https://ui-avatars.com/api/?name=Admin'
}]

with open('data/users.json', 'w') as f:
    json.dump(users, f, indent=2)
"
```

### 2. Setup Monitoring

- Configure application logging
- Setup error tracking (Sentry, Rollbar)
- Monitor server resources
- Setup uptime monitoring

### 3. Backup Strategy

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/backups/aop-planner"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup data directory
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" /var/www/aop-planner/data

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /var/www/aop-planner/uploads

# Keep only last 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup-aop-planner.sh
```

### 4. Update Google OAuth Redirect URIs

In Google Cloud Console, add production callback:
```
https://your-domain.com/login/google/callback
```

## Monitoring & Maintenance

### Health Check Endpoint

Add to `app.py`:
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })
```

### Log Rotation

Configure logrotate in `/etc/logrotate.d/aop-planner`:
```
/var/log/aop-planner/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        supervisorctl restart aop-planner
    endscript
}
```

## Troubleshooting

### Common Issues

1. **500 Error on AI Features**
   - Check OpenAI API key is set correctly
   - Verify API endpoint is accessible
   - Check logs for specific error messages

2. **Google OAuth Fails**
   - Verify redirect URI matches exactly
   - Check client ID and secret
   - Ensure OAuth consent screen is configured

3. **File Upload Fails**
   - Check directory permissions
   - Verify disk space
   - Check nginx client_max_body_size

### Debug Mode

**Never enable in production**, but for troubleshooting:
```python
# Temporarily set in app.py
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Performance Optimization

1. **Enable Caching**: Add Flask-Caching
2. **Database Connection Pooling**: When migrating to SQL
3. **CDN for Static Assets**: Use CloudFlare or similar
4. **Compress Responses**: Enable gzip in nginx
5. **Rate Limiting**: Add Flask-Limiter

## Security Hardening

1. **HTTPS Only**: Enforce SSL
2. **Security Headers**: Add helmet-like middleware
3. **CSRF Protection**: Enable Flask-WTF CSRF
4. **Input Validation**: Strengthen all form inputs
5. **Regular Updates**: Keep dependencies updated

## Scaling Considerations

- **Horizontal Scaling**: Use load balancer with multiple app instances
- **Session Storage**: Move to Redis for shared sessions
- **File Storage**: Migrate to S3/GCS
- **Database**: PostgreSQL with read replicas
- **Caching Layer**: Redis for frequently accessed data
