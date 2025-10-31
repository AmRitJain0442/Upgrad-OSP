# Quick Start Guide - AI Skills Academy

## Run the Application (5 minutes)

### ⚠️ IMPORTANT: Real Document Upload Now Available!

The platform now uses REAL file upload and Gemini API for summarization!

### Setup with Gemini API (Recommended)

**Step 1:** Get your FREE API key: https://makersuite.google.com/app/apikey

**Step 2:** Create `.env` file with your API key:
```bash
cd ai-learning-platform
copy .env.example .env
# Edit .env file and add: GEMINI_API_KEY=your_key_here
```

**Step 3:** Install and run:
```bash
pip install -r requirements.txt
cd backend
python app.py
```

You should see: `✓ Gemini API key loaded successfully`

Open browser: **http://localhost:5000**

Now you can upload YOUR OWN documents (PDF, DOCX, TXT)!

### Option 2: With Gemini API (For Chat Feature)
If you want the free-form chat to work:

1. Get API key: https://makersuite.google.com/app/apikey
2. Set environment variable:
   ```cmd
   set GEMINI_API_KEY=your_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   cd backend
   python app.py
   ```

## Try the Interactive Features

### 1. Visual Highlighting
- Click on "Foundations of Prompting" → Launch Submodule 1
- Watch the **Upload Document** button glow red
- The tutor tells you exactly what to do next!

### 2. Proactive Suggestions  
- Click the Upload button (sample document loads)
- Start typing: "Summarize this document"
- **Watch the tutor interrupt** with a helpful tip!

### 3. Good vs Bad Prompts
- Try prompt: "Summarize this document"
  - See the AI "hallucinate" (add fake facts)
- Try prompt: "Based only on the text provided, summarize this document"
  - See the AI stay focused!

### 4. Interactive Quiz
- Complete the lesson with a good prompt
- Answer the quiz question
- **Watch Submodule 2 unlock** with red glow!

## Architecture Overview

```
Left Panel (AI Tutor)          Right Panel (Workspace)
├─ Welcome message             ├─ Submodule tabs
├─ Step-by-step guidance       ├─ Upload button (glows!)
├─ Proactive tips              ├─ Workspace AI chat
├─ Interactive quiz            └─ Prompt input (glows!)
└─ Free-form Q&A chat
```

## Key Files

- `academy.js` - All the magic (highlighting, tips, quizzes)
- `style.css` - Red accent theme + glow animations
- `module_new.html` - Two-panel layout
- `app.py` - Flask backend (optional for chat)

## Customization

### Change Lesson Content
Edit in `academy.js`:
- Line 2: `SAMPLE_DOCUMENT` - Change the article
- Line 145: `startLesson()` - Edit tutor messages
- Line 200: Quiz data - Change questions

### Add More Courses
Edit in `backend/app.py`:
- Line 23: `COURSES` array - Add new courses

### Adjust Colors
Edit in `style.css`:
- Line 1: `--primary: #ff3333` - Change red accent

## Troubleshooting

**Port 5000 already in use?**
```python
# In app.py, change last line:
app.run(debug=True, port=5001)
```

**Styles not loading?**
- Make sure you're running from the `backend` folder
- Flask serves static files from `../frontend/static`

**No tutor messages?**
- Check browser console (F12) for errors
- Verify `academy.js` is loading

## What's Next?

The platform demonstrates the core interactive features. To make it production-ready:

1. Build out submodules 2-4
2. Connect real Gemini API for dynamic responses
3. Add user accounts & progress persistence
4. Create more courses
5. Add analytics to track learning effectiveness

Enjoy building the future of AI education! 🎓
