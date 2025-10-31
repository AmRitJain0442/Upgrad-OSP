from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.secret_key = 'your-secret-key-here-change-in-production'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'YOUR_API_KEY_HERE'))
model = genai.GenerativeModel('gemini-pro')

COURSES = [
    {
        'id': 'foundations',
        'title': 'Foundations of Prompting',
        'description': 'Master the fundamentals of prompt engineering for AI tools',
        'submodules': [
            {'id': 1, 'title': 'Focused Summarization', 'completed': False},
            {'id': 2, 'title': 'Advanced Techniques', 'completed': False},
            {'id': 3, 'title': 'Chain-of-Thought Reasoning', 'completed': False},
            {'id': 4, 'title': 'Real-world Practice', 'completed': False}
        ]
    }
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    
    if ext == 'txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == 'pdf':
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ' '.join([page.extract_text() for page in reader.pages])
            return text
    elif ext == 'docx':
        doc = docx.Document(filepath)
        return ' '.join([para.text for para in doc.paragraphs])
    return ''

@app.route('/')
def index():
    return render_template('courses.html', courses=COURSES)

@app.route('/module/<course_id>/<int:submodule_id>')
def module(course_id, submodule_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    
    submodule = next((s for s in course['submodules'] if s['id'] == submodule_id), None)
    if not submodule:
        return "Submodule not found", 404
    
    return render_template('module_new.html', course=course, submodule=submodule)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    context = data.get('context', '')
    
    try:
        prompt = f"You are an AI tutor teaching prompt engineering. Context: {context}\n\nUser: {message}\n\nProvide helpful, encouraging guidance."
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        text = extract_text(filepath)
        session['uploaded_document'] = text[:5000]  # Store first 5000 chars
        
        return jsonify({
            'success': True,
            'filename': filename,
            'preview': text[:500] + '...' if len(text) > 500 else text
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.json
    prompt = data.get('prompt', '')
    document_text = session.get('uploaded_document', '')
    
    if not document_text:
        return jsonify({'error': 'No document uploaded'}), 400
    
    try:
        full_prompt = f"{prompt}\n\nDocument:\n{document_text}"
        response = model.generate_content(full_prompt)
        return jsonify({'summary': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
