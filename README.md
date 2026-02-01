# AOP Planner - Annual Operating Plan Management System

A comprehensive Flask-based web application for managing Annual Operating Plans (AOP) with AI-powered PRD (Product Requirements Document) management and roadmap planning capabilities.

## 🌟 Features

### Core Functionality
- **PRD Management**: Upload, parse, analyze, and improve Product Requirements Documents
- **AI-Powered Improvements**: Leverage OpenAI to enhance PRD quality and completeness
- **Roadmap Planning**: Create and manage roadmap requests with RICE scoring
- **Multi-format Support**: Handle TXT, PDF, DOC, DOCX, and Markdown files
- **Interactive Chat Assistant**: Context-aware AI assistant for PRD refinement

### User Management
- **Google OAuth Integration**: Secure authentication via Google
- **Role-Based Access Control**: Support for Requester, Reviewer, and Admin roles
- **User Dashboard**: Personalized views based on user roles

### Admin Features
- **Form Configuration**: Customize roadmap request forms
- **User Management**: Manage users and their roles
- **Sample Data Loading**: Quick setup with pre-populated data

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google OAuth credentials (for authentication)
- OpenAI API key or compatible API endpoint (for AI features)

## 🚀 Quick Start

### 1. Clone or Download the Repository

```bash
cd /path/to/AOP-Planner
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

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional: for custom endpoints
OPENAI_MODEL=gpt-4  # Optional: default model
```

### 5. Run the Application

```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

## 📁 Project Structure

```
AOP-Planner/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── data/                   # Application data storage
│   ├── roadmaps.json      # Roadmap requests
│   ├── users.json         # User database
│   └── roadmap_form.json  # Form configuration
├── templates/              # HTML templates
│   ├── login.html         # Login page
│   ├── home.html          # Dashboard
│   ├── prd_management.html # PRD tool
│   ├── roadmap.html       # Roadmap planner
│   └── admin.html         # Admin panel
├── uploads/                # Uploaded files
│   └── roadmap_attachments/ # Roadmap file attachments
└── venv/                   # Virtual environment (not in version control)
```

## 🔐 Security Considerations

### Before Deployment

1. **Remove Hardcoded Credentials**: The current `app.py` contains hardcoded API keys (lines 138-139). These MUST be moved to environment variables.

2. **Update Secret Key**: Change the default `SECRET_KEY` in production:
   ```python
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
   ```

3. **Configure Google OAuth**:
   - Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com/)
   - Add authorized redirect URIs: `http://localhost:5000/login/google/callback`
   - For production, add your production domain

4. **Secure File Uploads**: Review file upload size limits and allowed extensions

5. **Database Security**: Consider migrating from JSON files to a proper database (PostgreSQL, MySQL) for production

## 🎯 User Roles

### Requester
- Create roadmap requests
- Upload and manage PRDs
- Use AI improvement features
- View own submissions

### Reviewer
- Review roadmap requests
- Provide feedback
- Access all PRDs

### Admin
- Full system access
- User management
- Form configuration
- Load sample data

## 🔧 Configuration

### Form Customization

Admins can customize the roadmap request form through the Admin Panel:
- Add/remove fields
- Configure dropdown options
- Set validation rules

### AI Model Configuration

The application supports custom OpenAI-compatible endpoints. Configure in `.env`:

```env
OPENAI_BASE_URL=https://your-custom-endpoint.com/api/v1
OPENAI_MODEL=your-model-name
```

## 📊 Features in Detail

### PRD Management
- **Upload**: Support for multiple document formats
- **Parse**: Automatic extraction of PRD sections
- **Analyze**: Completeness scoring and RICE analysis
- **Improve**: AI-powered content enhancement
- **Export**: Download in MD or DOCX format

### Roadmap Planning
- **Multi-step Form**: Structured data collection
- **File Attachments**: Upload PRDs and mockups
- **Dependencies**: Track feature dependencies
- **RICE Scoring**: Reach, Impact, Confidence, Effort analysis
- **Filtering**: By business unit, quarter, status

## 🐛 Known Issues & Limitations

1. **JSON-based Storage**: Not suitable for high-concurrency production use
2. **File Upload Security**: Limited validation on file contents
3. **No Email Notifications**: Manual notification system
4. **Session Management**: Uses Flask's default session handling
5. **No Audit Trail**: Limited tracking of changes

## 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions.

## 📝 License

[Specify your license here]

## 👥 Contributing

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for a detailed code walkthrough and development guide.

## 📧 Support

For issues or questions, contact: [Your contact information]

## 🙏 Acknowledgments

- Built with Flask, OpenAI, and modern web technologies
- Inspired by product management best practices
