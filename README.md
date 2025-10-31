# AI Skills Academy 

An interactive AI learning platform that teaches prompt engineering to working professionals through guided, hands-on experiences.

## Features

###  Core Experience
- **Two-Panel Interface**: AI Tutor (left) + Interactive Workspace (right)
- **Dark Theme**: Clean, professional design with sharp red accents
- **Proactive Learning**: Real-time guidance, tips, and feedback

###  Interactive "Magic" Features
- **Visual Highlighting**: Elements glow red when the tutor guides you to them
- **Proactive Suggestions**: Real-time tips appear as you type prompts
- **Interactive Quizzes**: Knowledge checks embedded directly in the tutor chat
- **Workspace AI**: Separate AI that responds to your prompts in real-time
- **Progress Tracking**: Tabbed navigation unlocks as you complete lessons

###  Lesson 1: Focused Summarization
Learn to write prompts that prevent AI "hallucination" (making up facts) through:
- Guided document loading
- Real-time prompt feedback
- Comparison of good vs. bad prompts
- Interactive quiz on key concepts

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API Key ⭐ EASY METHOD

**IMPORTANT**: The platform now uses real document upload and Gemini API for summarization!

**Quick Setup (2 minutes):**

1. Get your FREE API key: **https://makersuite.google.com/app/apikey**

2. Create a `.env` file in the `ai-learning-platform` folder:
   ```bash
   cd ai-learning-platform
   copy .env.example .env
   ```

3. Edit `.env` file and add your key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

**That's it!** The app will automatically load your API key from the `.env` file.

📖 **Detailed guide:** See `SETUP_API.md` for troubleshooting

### 3. Run the Application

```bash
cd backend
python app.py
```

### 4. Access the Platform

Open your browser and go to: `http://localhost:5000`

## Project Structure

```
ai-learning-platform/
├── backend/
│   └── app.py              # Flask server + API endpoints
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Futuristic UI styling
│   │   └── js/
│   │       ├── main.js     # Course page interactions
│   │       └── module.js   # Module page functionality
│   └── templates/
│       ├── courses.html    # Course listing page
│       └── module.html     # Learning module interface
├── uploads/                # Uploaded documents storage
└── requirements.txt        # Python dependencies
```

## How to Use

1. **Select Course**: Choose "Foundations of Prompting" from homepage
2. **Follow the Tutor**: The AI Tutor will guide you step-by-step
3. **Watch for Highlights**: Red glowing borders show what to do next
4. **Type Prompts**: The Tutor watches and offers real-time tips
5. **Complete Quiz**: Answer questions to reinforce learning
6. **Unlock Next Lesson**: Progress through all 4 submodules

## User Journey Example

**Step 1**: Tutor welcomes you and highlights "Upload Document" button  
**Step 2**: Sample document loads automatically in workspace  
**Step 3**: You type a basic prompt like "Summarize this"  
**Step 4**: Tutor interrupts with a proactive tip about constraints  
**Step 5**: You refine your prompt with "Based only on the text provided..."  
**Step 6**: AI generates accurate summary  
**Step 7**: Complete quiz about "hallucination"  
**Step 8**: Submodule 2 unlocks with glowing red highlight

## Technologies

- **Backend**: Python Flask
- **AI**: Google Gemini API
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Design**: Custom cyberpunk/robotic theme

## Future Enhancements

- Complete submodules 2-4
- Add more courses
- User authentication & progress tracking
- Code execution sandbox
- More interactive exercises

## Key Technologies

- **Visual Guidance**: Dynamic CSS highlighting system
- **Real-time Detection**: JavaScript event listeners for typing
- **Simulated AI**: Pre-programmed responses for demo (can connect to real Gemini API)
- **State Management**: Tracks user progress through lesson steps

---

Built with ❤️ for working professionals who want to master AI tools
