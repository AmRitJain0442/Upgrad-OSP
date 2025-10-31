# 📄 Real Document Upload & AI Summarization Guide

## 🎉 New Feature: Real Document Processing!

The platform now extracts text from YOUR documents and sends them to Gemini API for real AI-powered summarization!

---

## ✅ What Works Now

### 1. **Real File Upload**
- Upload PDF, DOCX, or TXT files
- Text extraction happens on the backend
- No more hardcoded sample documents

### 2. **Real AI Summarization**
- Your uploaded document is sent to Gemini API
- AI generates summaries based on YOUR prompts
- See real-time how prompt quality affects results

### 3. **Supported File Types**
- **PDF** - Extracts text from all pages
- **DOCX** - Extracts text from Word documents
- **TXT** - Reads plain text files

---

## 🚀 How to Use

### Step 1: Set Up Gemini API Key

**Get a FREE API key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

**Set the environment variable:**

**PowerShell:**
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
cd backend
python app.py
```

**CMD:**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
cd backend
python app.py
```

**Or edit `backend/app.py` line 19:**
```python
genai.configure(api_key='paste_your_key_here')
```

### Step 2: Run the Application

```bash
cd ai-learning-platform
pip install -r requirements.txt
cd backend
python app.py
```

### Step 3: Upload Your Document

1. Open http://localhost:5000
2. Click "Launch" on Submodule 1
3. AI Tutor will guide you
4. Click "Upload Document" button (it will glow red!)
5. Choose a PDF, DOCX, or TXT file
6. Watch as it uploads and extracts text

### Step 4: Try Different Prompts

**Bad Prompt (AI might hallucinate):**
```
Summarize this document
```

**Good Prompt (Constrained):**
```
Based only on the text provided in this document, summarize the main points without adding any external information.
```

**See the difference!**

---

## 📝 What Happens Behind the Scenes

### Upload Process:
```
1. User selects file → Frontend
2. File uploaded via FormData → Backend /api/upload
3. Backend extracts text (PDF/DOCX/TXT)
4. Text stored in session (first 5000 chars)
5. Preview sent back to frontend
6. Document appears in workspace
```

### Summarization Process:
```
1. User types prompt → Frontend
2. Prompt sent to → Backend /api/summarize
3. Backend combines: prompt + document text
4. Sent to Gemini API
5. AI generates summary
6. Summary displayed in workspace
```

---

## 🎯 Try These Sample Documents

### Create a Test File

**sample_article.txt:**
```
Artificial Intelligence in Healthcare

Artificial intelligence is transforming the healthcare industry. Machine learning 
algorithms can now detect diseases from medical images with accuracy matching human 
doctors. AI-powered chatbots provide 24/7 patient support, answering common health 
questions and triaging cases.

Key Applications:
- Medical imaging analysis (X-rays, MRIs, CT scans)
- Drug discovery and development
- Personalized treatment recommendations
- Administrative task automation
- Predictive analytics for patient outcomes

Challenges include data privacy concerns, the need for large training datasets, 
and ensuring AI systems are unbiased. Despite these hurdles, AI is expected to 
save the healthcare industry billions annually while improving patient care.
```

**Try these prompts:**
1. "Summarize this"
2. "Based only on the text, list the key applications of AI in healthcare"
3. "Based only on the text provided, explain the challenges mentioned"

---

## 🔍 Debugging Tips

### Issue: "No file provided"
- Make sure you selected a file
- Check file extension (PDF, DOCX, TXT only)

### Issue: "Connection error"
- Server not running? Start with `python app.py`
- Check you're in the `backend` folder

### Issue: "API error" 
- Gemini API key not set or invalid
- Set environment variable correctly
- Or edit app.py directly

### Issue: "No document uploaded" when generating
- Upload a document first
- Session might have expired (refresh page and try again)

### Issue: Empty or garbled text from PDF
- PDF might be scanned images (OCR not included)
- Try a text-based PDF or DOCX instead

---

## 💡 Pro Tips

### 1. Document Size Limits
- System stores first 5000 characters
- For longer documents, key info should be early
- Or increase limit in app.py line 102

### 2. Best File Types
- **TXT**: Always works perfectly
- **DOCX**: Reliable for text extraction
- **PDF**: Best with text-based PDFs (not scans)

### 3. Prompt Engineering Practice
- Start with bad prompts to see hallucination
- Add constraints to see improvement
- Compare results side-by-side

### 4. API Rate Limits
- Gemini free tier: 60 requests per minute
- Don't spam the Generate button
- Wait for response before trying again

---

## 📊 Example Learning Flow

### Session 1: Understanding Hallucination

**Document:** Upload any article

**Prompt 1:** "Summarize this"
→ AI might add external facts

**Prompt 2:** "Based only on the text provided, summarize this"
→ AI stays focused

**Learn:** Constraints prevent hallucination!

### Session 2: Specific Extraction

**Document:** Upload business report

**Prompt 1:** "What are the key points?"
→ Generic summary

**Prompt 2:** "Based only on the text, list the top 3 recommendations with their supporting evidence"
→ Structured, specific output

**Learn:** Specific instructions = better results!

---

## 🛠️ Technical Details

### Backend (app.py)

**Text Extraction:**
```python
def extract_text(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    
    if ext == 'txt':
        return open(filepath).read()
    elif ext == 'pdf':
        reader = PyPDF2.PdfReader(filepath)
        return ' '.join([p.extract_text() for p in reader.pages])
    elif ext == 'docx':
        doc = docx.Document(filepath)
        return ' '.join([p.text for p in doc.paragraphs])
```

**API Call:**
```python
full_prompt = f"{user_prompt}\n\nDocument:\n{document_text}"
response = model.generate_content(full_prompt)
```

### Frontend (academy.js)

**File Upload:**
```javascript
const formData = new FormData();
formData.append('file', file);
fetch('/api/upload', { method: 'POST', body: formData })
```

**Summarization:**
```javascript
fetch('/api/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: userPrompt })
})
```

---

## 🎓 Educational Value

This real integration teaches users:

1. **How file upload works** - FormData, multipart/form-data
2. **Text extraction** - Different formats need different approaches
3. **API integration** - Sending data to AI services
4. **Prompt engineering** - Quality prompts = quality outputs
5. **Error handling** - What happens when things go wrong

---

## 🔮 Future Enhancements

- [ ] OCR for scanned PDFs
- [ ] Support for images (with Gemini Vision)
- [ ] Larger document support (chunking)
- [ ] Save favorite prompts
- [ ] Compare multiple summaries
- [ ] Export results

---

## ✅ Checklist for First Use

- [ ] Gemini API key obtained
- [ ] Environment variable set
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`python app.py`)
- [ ] Browser opened to http://localhost:5000
- [ ] Test document ready (PDF/DOCX/TXT)
- [ ] Ready to learn!

---

**You're now using REAL AI document processing!** 🚀

Try uploading different documents and experimenting with various prompts to see how AI responds. The learning experience is now authentic and personalized to YOUR documents!
