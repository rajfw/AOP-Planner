import os
import logging
from datetime import datetime
import docx
import PyPDF2
import fitz  # PyMuPDF
import markdown

logger = logging.getLogger("aop_planner.parser")

def parse_document(filepath, filename):
    """Parse different document formats and extract text."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    text = ""
    
    try:
        if ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                
        elif ext == 'pdf':
            # Method 1: Try PyPDF2
            try:
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            except:
                pass
                
            # Method 2: Fallback to PyMuPDF if empty or failed
            if not text.strip():
                try:
                    doc = fitz.open(filepath)
                    for page in doc:
                        text += page.get_text() + "\n"
                except Exception as e:
                    logger.error(f"PDF parsing error: {e}")
                    if not text:
                        text = f"Error parsing PDF: {str(e)}"
                    
        elif ext in ['doc', 'docx']:
            try:
                doc = docx.Document(filepath)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            except Exception as e:
                logger.error(f"DOCX parsing error: {e}")
                text = f"Error parsing DOCX: {str(e)}"
                
        elif ext == 'md':
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                
    except Exception as e:
        logger.error(f"Error parsing document {filename}: {e}")
        text = f"Error parsing document: {str(e)}"
    
    return {
        'filename': filename,
        'content': text,
        'word_count': len(text.split()),
        'char_count': len(text),
        'parsed_at': datetime.now().isoformat()
    }

def parse_prd_structure(text):
    """Parse PRD and extract structured information."""
    sections = {
        'overview': '',
        'objectives': '',
        'scope': '',
        'features': '',
        'user_stories': '',
        'requirements': '',
        'success_metrics': '',
        'timeline': '',
        'risks': ''
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.strip().lower()
        
        if any(keyword in line_lower for keyword in ['overview', 'introduction', 'background']):
            current_section = 'overview'
        elif any(keyword in line_lower for keyword in ['objectives', 'goals', 'purpose']):
            current_section = 'objectives'
        elif any(keyword in line_lower for keyword in ['scope', 'in scope', 'out of scope']):
            current_section = 'scope'
        elif any(keyword in line_lower for keyword in ['features', 'functionality']):
            current_section = 'features'
        elif any(keyword in line_lower for keyword in ['user stories', 'user personas', 'user journey']):
            current_section = 'user_stories'
        elif any(keyword in line_lower for keyword in ['requirements', 'functional requirements', 'non-functional']):
            current_section = 'requirements'
        elif any(keyword in line_lower for keyword in ['success metrics', 'kpis', 'metrics']):
            current_section = 'success_metrics'
        elif any(keyword in line_lower for keyword in ['timeline', 'milestones', 'schedule']):
            current_section = 'timeline'
        elif any(keyword in line_lower for keyword in ['risks', 'assumptions', 'constraints']):
            current_section = 'risks'
        elif line.strip() and current_section:
            sections[current_section] += line + '\n'
    
    return sections
