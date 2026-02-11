# Security Audit & Fixes Required

## 🚨 CRITICAL ISSUES - Must Fix Before Deployment

### 1. Hardcoded API Credentials in app.py

**Location**: Lines 138-139

**Current Code**:
```python
client = OpenAI(
    api_key="eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im5hbWUiOiJSYWplc3dhciBQIFMiLCJlbWFpbCI6InJhamVzd2FyLnN1YnJhbWFuaUBmcmVzaHdvcmtzLmNvbSIsImltYWdlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0FBUkNWSktyMjhxbU0xRTdnUE1fSlhPcDU4MEZHM2prNThMYzQ1SVB6eVFqN0lxWF89czk2LWMifSwianRpIjoiUGNVU0xxOFNrR3lYdmF1aFlEQTdsIiwiaWF0IjoxNzcwNzg2NTYwLCJleHAiOjE3NzEzOTEzNjB9.JglVKNUeldw7thE2swT0jiXKkf2M3DNUCZZ0WAIAWOg",
    base_url="https://cloudverse.freshworkscorp.com/api/v1"
)
```

**Required Fix**:
```python
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
)
```

**Impact**: Exposed API credentials can be used by unauthorized parties, leading to:
- Unauthorized API usage and costs
- Data breaches
- Service abuse

**Priority**: CRITICAL - Fix immediately

---

### 2. Weak Default Secret Key

**Location**: Line 70

**Current Code**:
```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fw-aop-secret-key-2025')
```

**Required Fix**:
```python
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")
app.config['SECRET_KEY'] = secret_key
```

**Impact**: Weak or default secret keys can compromise:
- Session security
- Cookie integrity
- CSRF protection

**Priority**: CRITICAL

---

### 3. Missing Authentication on Critical Endpoints

**Location**: Multiple endpoints

**Issues**:
- `/api/upload` (line 482) - No `@login_required` decorator
- `/api/export` (line 783) - No authentication
- `/api/list` (line 722) - No authentication
- `/api/roadmap/<id>` PUT (line 908) - No authentication

**Required Fix**: Add `@login_required` decorator to all API endpoints

**Priority**: HIGH

---

## ⚠️ HIGH PRIORITY ISSUES

### 4. Insecure Password Storage

**Location**: Line 380

Users are stored with plaintext passwords in JSON:
```python
user_data = next((u for u in users if u['username'] == username and u['password'] == password), None)
```

**Required Fix**: Implement password hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

# When creating user:
'password': generate_password_hash(password)

# When checking:
if user_data and check_password_hash(user_data['password'], password):
    # login
```

**Priority**: HIGH

---

### 5. No Input Validation

**Issues**:
- File upload content not validated
- JSON inputs not sanitized
- No XSS protection in user-generated content

**Required Fix**: Add input validation library (e.g., marshmallow, pydantic)

**Priority**: HIGH

---

### 6. No Rate Limiting

**Impact**: Vulnerable to:
- Brute force attacks
- API abuse
- DoS attacks

**Required Fix**: Add Flask-Limiter
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/improve', methods=['POST'])
@limiter.limit("10 per hour")
def improve_prd():
    # ...
```

**Priority**: MEDIUM

---

## 📋 MEDIUM PRIORITY ISSUES

### 7. Insecure File Storage

- Files stored locally without encryption
- No virus scanning
- Predictable file paths

**Recommendation**: 
- Use cloud storage (S3, GCS)
- Implement virus scanning
- Use UUIDs for file names

---

### 8. No HTTPS Enforcement

**Required Fix**: Add HTTPS redirect middleware
```python
from flask_talisman import Talisman

if not app.debug:
    Talisman(app, force_https=True)
```

---

### 9. Missing Security Headers

**Required Fix**: Add security headers
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

### 10. No CSRF Protection

**Required Fix**: Enable Flask-WTF CSRF protection
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

---

## 🔍 LOW PRIORITY / IMPROVEMENTS

### 11. Error Information Disclosure

Debug mode exposes stack traces. Ensure `debug=False` in production.

---

### 12. No Audit Logging

Implement logging for:
- User login/logout
- File uploads/downloads
- Data modifications
- Failed authentication attempts

---

### 13. Session Configuration

Add secure session configuration:
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)
)
```

---

## 📝 Immediate Action Items

1. **Before ANY deployment**:
   - [ ] Remove hardcoded API key from app.py
   - [ ] Generate and set strong SECRET_KEY
   - [ ] Add authentication to all API endpoints
   - [ ] Implement password hashing

2. **Before production deployment**:
   - [ ] Add rate limiting
   - [ ] Enable HTTPS
   - [ ] Add security headers
   - [ ] Enable CSRF protection
   - [ ] Implement input validation

3. **Post-deployment**:
   - [ ] Setup monitoring and alerting
   - [ ] Implement audit logging
   - [ ] Regular security updates
   - [ ] Penetration testing

---

## 🛠️ Quick Fix Script

Save as `security_fixes.py` and review before applying:

```python
#!/usr/bin/env python3
"""
Quick security fixes for app.py
Review carefully before running!
"""

import re
import os

def fix_app_py():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Fix 1: Remove hardcoded credentials
    content = re.sub(
        r'api_key="[^"]*"',
        'api_key=os.getenv("OPENAI_API_KEY")',
        content
    )
    content = re.sub(
        r'base_url="https://cloudverse\.freshworkscorp\.com/api/v1"',
        'base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")',
        content
    )
    
    # Fix 2: Remove default secret key
    content = re.sub(
        r"app\.config\['SECRET_KEY'\] = os\.getenv\('SECRET_KEY', '[^']*'\)",
        "app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')",
        content
    )
    
    # Backup original
    with open('app.py.backup', 'w') as f:
        f.write(content)
    
    print("Backup created: app.py.backup")
    print("Review changes before applying!")
    
    # Write fixed version
    with open('app.py.fixed', 'w') as f:
        f.write(content)
    
    print("Fixed version: app.py.fixed")
    print("Review and then: mv app.py.fixed app.py")

if __name__ == '__main__':
    fix_app_py()
```

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
