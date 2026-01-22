# Quick Start for New Developers

> ✅ **Validated**: This guide has been tested with a fresh checkout on January 22, 2026

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## Setup (5 minutes)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AOP-Planner
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output**: All packages install successfully (Flask, flask-cors, flask-login, authlib, etc.)

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Edit .env and paste the generated key as SECRET_KEY
# For now, you can leave Google OAuth and OpenAI API placeholders
```

### 5. Run the Application

```bash
python app.py
```

**Expected output**:
```
OpenAI client initialized successfully
Starting AI PRD Management...
Upload folder: uploads
OpenAI available: True
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 6. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

You should see the login page! 🎉

---

## What Works Immediately

- ✅ Application starts and runs
- ✅ Login page accessible
- ✅ All routes functional
- ✅ File upload capabilities
- ✅ PRD management features
- ✅ Roadmap planning

## What Needs Configuration (Optional)

### Google OAuth (for Google Sign-In)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `http://localhost:5000/login/google/callback`
4. Update `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### OpenAI API (for AI Features)

1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Update `.env`:
   ```
   OPENAI_API_KEY=your-api-key
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL=gpt-4
   ```

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or run on different port
python app.py --port 5001
```

### "SECRET_KEY not set"
```bash
# Generate and add to .env
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Next Steps

1. **Read the Documentation**:
   - [README.md](README.md) - Full project overview
   - [USER_GUIDE.md](USER_GUIDE.md) - Feature documentation
   - [SECURITY.md](SECURITY.md) - Security considerations
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

2. **Create an Admin User**:
   - See [DEPLOYMENT.md](DEPLOYMENT.md#post-deployment) for instructions

3. **Explore Features**:
   - Upload a PRD document
   - Try AI improvement features
   - Create a roadmap request

---

## Development Tips

### Running Tests
```bash
# Test OpenAI connection
python test_openai.py

# Test custom API
python test_custom_api.py
```

### Stopping the Server
```
Press CTRL+C in the terminal
```

### Viewing Logs
```bash
# Application logs appear in terminal
# Check for errors or warnings
```

### Database Files
```
data/users.json          # User database
data/roadmaps.json       # Roadmap requests
data/roadmap_form.json   # Form configuration
```

---

## Common Development Workflow

```bash
# 1. Start your day
cd AOP-Planner
source venv/bin/activate
python app.py

# 2. Make changes to code
# Edit files in your IDE

# 3. Test changes
# Refresh browser or restart server

# 4. Commit changes
git add .
git commit -m "Your commit message"
git push
```

---

## Getting Help

- **Documentation**: Check README.md and other .md files
- **Issues**: Review SECURITY.md for known issues
- **Questions**: Contact your team lead

---

**Last Validated**: January 22, 2026  
**Validation Status**: ✅ All steps verified working
