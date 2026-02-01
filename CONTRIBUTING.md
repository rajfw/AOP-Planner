# Developer Guide & Code Walkthrough

Welcome to the AOP Planner project! This guide is designed to help new developers understand the codebase, architecture, and workflows so they can contribute effectively.

## 🏗 System Architecture

The AOP Planner is a **monolithic Flask application** designed for simplicity and portability. It avoids complex database dependencies by using a file-based JSON storage system, making it easy to deploy and backup.

```mermaid
graph TD
    Client[Web Browser] <-->|HTTP/HTTPS| FlaskApp[Flask Application (app.py)]
    
    subgraph "Backend Layer"
        FlaskApp <--> Auth[Auth Module (OAuth/Custom)]
        FlaskApp <--> Logic[Business Logic & AI]
    end
    
    subgraph "Data & Storage"
        Logic <--> JSONDB[(JSON Database /data)]
        Logic <--> FileSys[File System /uploads]
    end
    
    subgraph "External Services"
        Logic <--> OpenAI[OpenAI API / LLM]
        Auth <--> Google[Google OAuth]
    end
```

## 📂 Project Structure

```text
AOP-Planner/
├── app.py                  # 🧠 THE BRAIN: Main Flask application entry point
├── templates/              # 🎨 FRONTEND: Jinja2 HTML templates + Embedded JS
│   ├── prd_management.html #    - Heavy frontend logic for PRD editor
│   ├── roadmap.html        #    - Interactive roadmap dashboard
│   └── ...
├── data/                   # 💾 DATABASE: JSON files acting as DB
│   ├── roadmaps.json       #    - Stores all roadmap requests
│   ├── users.json          #    - Stores user credentials & roles
│   └── roadmap_form.json   #    - Dynamic form configuration
├── uploads/                # 📂 STORAGE: User uploaded files
└── requirements.txt        # 📦 DEPS: Python dependencies
```

## 🧠 Code Deep Dive (`app.py`)

The `app.py` file is the heart of the application. Here are the key sections you need to know:

### 1. Configuration & Setup (Lines 1-52)
- **Imports**: Standard Flask ecosystem (`flask`, `flask_login`, `flask_cors`).
- **File System**: Sets up `uploads/` and `data/` directories automatically on startup.
- **LLM Setup**: Initializes the OpenAI client if the library is available. *Note: The app degrades gracefully if OpenAI is missing.*

### 2. Database Layer (Custom JSON ORM)
Instead of SQL, we use helper functions to read/write JSON files:
- `get_roadmaps()` / `save_roadmaps(data)`: specific to roadmap items.
- `get_users()`: Reads `data/users.json`.
- **Note**: This is not concurrency-safe for high-scale production but perfect for internal tools.

### 3. Authentication (Lines 72-132)
- **Hybrid Auth**: Supports both **Google OAuth** and **Custom JSON-based Login**.
- `User` class: A simple wrapper around the JSON dictionary to satisfy `flask_login.UserMixin`.
- `load_user`: The crucial callback for Flask-Login to fetching user sessions.
- **Decorators**: `@admin_required` protects sensitive routes.

### 4. Core Features

#### A. PRD Management (Lines 518-646)
The PRD flow is:
1.  **Upload**: `/api/upload` - Parses PDF/DOCX/MD using libraries like `PyPDF2` or `docx`.
2.  **Display**: Frontend shows the parsed text.
3.  **Improve**: `/api/improve` - Sends content to LLM with specific prompts ("clarify", "expand").
4.  **Chat**: `/api/prd/chat` - Context-aware chat using the current document content as system context.

#### B. Roadmap Planning (Lines 880-980)
- **CRUD Operations**: Standard API structure (`GET`, `POST`, `PUT`, `DELETE`).
- **RICE Scoring**: Sometimes calculated via AI in `analyze_prd`, but stored as integers in the roadmap object.
- **Dynamic Forms**: The form fields are often driven by `data/roadmap_form.json` to allow admins to change dropdowns without deployment.

## 🎨 Frontend Architecture

The frontend is built with **Server-Side Rendered (SSR) HTML** + **Vanilla JavaScript**.

- **Templates**: `templates/` contains the HTML.
- **Logic**: Most interactivity (drag-and-drop, AJAX calls, dynamic rendering) lives inside `<script>` tags within the HTML files.
    - *Example*: See `templates/prd_management.html` for the complex PRD editor logic.
- **Styling**: Likely uses Tailwind CSS (via CDN) or custom CSS embedded in templates.

## 🛠 Development Workflow

### 1. Setting Up
```bash
# Clone
git clone <repo-url>
cd AOP-Planner

# Virtual Env
python3 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt

# Environment
cp .env.example .env
# -> Edit .env with your OPENAI_API_KEY and GOOGLE_CLIENT_ID
```

### 2. Running Locally
```bash
python app.py
# Server starts at http://127.0.0.1:5000
```

### 3. Debugging
- **Logs**: Check `app.log` for application errors and parsed file metadata.
- **Console**: Since it's Flask `debug=True`, errors appear in the terminal.
- **Users**: If you can't login, check `data/users.json` or use `debug_login.py`.


### 4. Security
Please review [SECURITY.md](SECURITY.md) before making changes.
- **Critical**: Never commit API keys or secrets to git.
- **Best Practice**: Always use environment variables for sensitive data.

## 🤝 How to Contribute


### Scenario A: Adding a new Field to Roadmap
1.  **Backend**: Open `app.py` -> `create_roadmap_request`. Add the new field to the `data` dictionary.
2.  **Frontend**: Open `templates/roadmap.html`. 
    - Add the input field to the "New Request" modal.
    - Update the JavaScript function that handles form submission (`submitRoadmap`).
    - Update the rendering logic to display the new column/card info.

### Scenario B: Improving AI Prompts
1.  **Locate**: Go to `improve_prd_with_llm` function in `app.py`.
2.  **Edit**: Modify the `prompt_templates` dictionary.
3.  **Test**: Restart app and try the "Improve" button on a PRD.

### Scenario C: Switching to a Real Database
1.  Replace `get_roadmaps()` / `save_roadmaps()` functions.
2.  Implement a SQLAlchemy model.
3.  Update the helper functions to query SQL instead of reading JSON.
4.  The rest of the app (API/Frontend) will remain largely unchanged!

---
*Happy Coding! For any questions, refer to the `README.md` or contact the team lead.*
