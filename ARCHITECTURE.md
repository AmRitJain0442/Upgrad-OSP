# AI Skills Academy - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser (Client)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │   Left Panel     │              │   Right Panel    │        │
│  │   (AI Tutor)     │              │   (Workspace)    │        │
│  ├──────────────────┤              ├──────────────────┤        │
│  │                  │              │                  │        │
│  │ • Welcome msg    │              │ • Submodule tabs │        │
│  │ • Instructions   │◀────────────▶│ • Upload button  │        │
│  │ • Proactive tips │  Highlights  │ • Workspace chat │        │
│  │ • Quiz system    │              │ • Prompt input   │        │
│  │ • Free chat Q&A  │              │ • AI responses   │        │
│  │                  │              │                  │        │
│  └──────────────────┘              └──────────────────┘        │
│           ▲                                   ▲                 │
│           │                                   │                 │
│           └───────────────┬───────────────────┘                 │
│                           │                                     │
│                    academy.js                                   │
│              (State Machine + Logic)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Optional: Chat API calls
                            ▼
                  ┌──────────────────┐
                  │  Flask Backend   │
                  │   (app.py)       │
                  ├──────────────────┤
                  │ • /api/chat      │
                  │ • /api/upload    │
                  │ • /api/summarize │
                  └──────────────────┘
                            │
                            │ Optional: Real AI
                            ▼
                  ┌──────────────────┐
                  │  Gemini API      │
                  │  (Google)        │
                  └──────────────────┘
```

---

## 📁 File Structure Diagram

```
ai-learning-platform/
│
├── 📄 README.md           ← Main documentation
├── 📄 QUICKSTART.md       ← 5-min setup guide
├── 📄 FEATURES.md         ← Feature deep-dive
├── 📄 PROJECT_SUMMARY.md  ← Complete overview
├── 📄 ARCHITECTURE.md     ← This file
├── 📄 TEST_CHECKLIST.md   ← Testing guide
├── 📄 requirements.txt    ← Python packages
├── 📄 .gitignore          ← Git ignore rules
│
├── 📂 backend/
│   └── 🐍 app.py          ← Flask server (optional)
│       • Serves templates
│       • API endpoints for chat
│       • Gemini integration
│
└── 📂 frontend/
    ├── 📂 static/
    │   ├── 📂 css/
    │   │   └── 🎨 style.css       ← Dark theme + red accents
    │   │       • Color variables
    │   │       • Highlighting system
    │   │       • Quiz styles
    │   │       • Workspace chat
    │   │
    │   └── 📂 js/
    │       ├── ⚙️ main.js         ← Course page animations
    │       ├── ⚙️ module.js       ← Old module (backup)
    │       └── ⭐ academy.js      ← MAIN LOGIC
    │           • State machine
    │           • Highlighting
    │           • Proactive tips
    │           • Quiz system
    │           • Lesson flow
    │
    └── 📂 templates/
        ├── 📄 courses.html        ← Homepage
        ├── 📄 module.html         ← Old layout (backup)
        └── ⭐ module_new.html     ← Two-panel interface
```

---

## 🔄 State Machine Flow

```
┌──────────────────────────────────────────────────────────────┐
│                  Lesson State Machine                        │
└──────────────────────────────────────────────────────────────┘

  [START]
     │
     ▼
┌─────────────┐
│  'welcome'  │ → Show welcome message
└─────────────┘   "We're going to learn..."
     │
     │ After 1.5s
     ▼
┌─────────────┐
│  'upload'   │ → Highlight Upload button
└─────────────┘   "Please click Upload..."
     │
     │ User clicks Upload
     ▼
┌─────────────┐
│  'prompt'   │ → Highlight Prompt input
└─────────────┘   Watch typing for tips
     │
     │ Watch input events
     ├─ If typing bad prompt → Show proactive tip
     │
     │ User clicks Generate
     ▼
┌─────────────┐
│ 'generate'  │ → Check if constraints exist
└─────────────┘
     │
     ├─ No constraints?
     │    │
     │    ▼
     │  [Show hallucinated summary]
     │  "Try again with constraints..."
     │    │
     │    └──┐
     │       │
     ├─ Has constraints?
     │       │
     │       ▼
     │  [Show good summary]
     │  "Fantastic! See the difference?"
     │       │
     │       ▼
     │  ┌─────────┐
     │  │ 'quiz'  │ → Show interactive quiz
     │  └─────────┘
     │       │
     │       │ Correct answer
     │       ▼
     │  ┌──────────┐
     │  │'complete'│ → Unlock next submodule
     │  └──────────┘   Highlight Tab 02
     │       │
     │       ▼
     │   [LESSON COMPLETE]
     │
     └─────────────────────────────┘
```

---

## 🎯 Highlighting System

```
┌────────────────────────────────────────────────────┐
│           Highlighting Mechanism                    │
└────────────────────────────────────────────────────┘

JavaScript Function:
┌─────────────────────────────────────┐
│ highlightElement(element)           │
├─────────────────────────────────────┤
│ 1. Remove all existing highlights   │
│ 2. Add 'highlight-glow' class       │
│ 3. Scroll element into view         │
└─────────────────────────────────────┘
        │
        ▼
CSS Class Applied:
┌─────────────────────────────────────┐
│ .highlight-glow {                   │
│   border: 2px solid #ff3333;        │
│   box-shadow: 0 0 20px red glow;    │
│   animation: glowPulse 1.5s;        │
│ }                                   │
└─────────────────────────────────────┘
        │
        ▼
Visual Result:
┌════════════════════════════════════┐
║  ⚠️ UPLOAD DOCUMENT ⚠️              ║ ← Pulsing red!
║                                    ║
║  [Smooth glowing animation]        ║
└════════════════════════════════════┘
```

---

## 💬 Chat System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  Dual Chat System                            │
└──────────────────────────────────────────────────────────────┘

LEFT PANEL: Tutor Chat
├─ Purpose: Teaching, guidance
├─ Messages:
│  ├─ Welcome messages
│  ├─ Instructions
│  ├─ Proactive tips
│  ├─ Quizzes
│  └─ Free Q&A (optional)
│
└─ Functions:
   ├─ addTutorMessage(content)
   ├─ addUserMessage(content)
   ├─ addProactiveTip(tip)
   └─ addTutorMessage(content, isQuiz=true)

RIGHT PANEL: Workspace Chat
├─ Purpose: AI interaction workspace
├─ Messages:
│  ├─ Document loaded notification
│  ├─ User prompts
│  └─ AI-generated responses
│
└─ Functions:
   └─ addWorkspaceMessage(content, isUser)

Visual Distinction:
┌────────────────┐         ┌────────────────┐
│ Tutor Message  │         │ Your Message   │
│ (gray bubble)  │         │ (red bubble)   │
│ [Left aligned] │         │[Right aligned] │
└────────────────┘         └────────────────┘
```

---

## 🎮 Event Flow Diagram

```
User Actions → Events → State Changes → UI Updates

┌───────────────┐
│ User clicks   │
│ Upload button │
└───────┬───────┘
        │
        ▼
┌─────────────────────┐
│ onclick event fires │
└─────────┬───────────┘
          │
          ▼
┌──────────────────────────┐
│ handleDocumentUpload()   │
│ • documentUploaded=true  │
│ • currentStep='prompt'   │
└──────────┬───────────────┘
           │
           ▼
┌───────────────────────────┐
│ UI Updates:               │
│ • Hide upload section     │
│ • Show workspace chat     │
│ • Show prompt input       │
│ • Add workspace message   │
│ • Highlight prompt input  │
└───────────────────────────┘


User Types → Events → Logic → Response

┌───────────────┐
│ User types in │
│ prompt input  │
└───────┬───────┘
        │
        ▼
┌─────────────────────┐
│ oninput event fires │
└─────────┬───────────┘
          │
          ▼
┌──────────────────────────┐
│ handlePromptTyping()     │
│ Check: length > 10?      │
│ Check: has constraints?  │
└──────────┬───────────────┘
           │
           ├─ No constraints?
           │    │
           │    ▼
           │ ┌──────────────────┐
           │ │ Show proactive   │
           │ │ tip once         │
           │ └──────────────────┘
           │
           └─ Has constraints? → Do nothing
```

---

## 🗂️ Data Flow

```
Sample Document → Processing → Display

HARDCODED:
const SAMPLE_DOCUMENT = "The Rise of Remote Work..."
                    │
                    ▼
           ┌─────────────────┐
           │ User clicks     │
           │ Upload          │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Load into       │
           │ workspace chat  │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ User writes     │
           │ prompt          │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Analyze prompt  │
           │ for constraints │
           └────────┬────────┘
                    │
          ┌─────────┴─────────┐
          │                   │
    No constraints      Has constraints
          │                   │
          ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│ Hallucinated     │  │ Focused summary  │
│ response with    │  │ from document    │
│ fake sources     │  │ only             │
└──────────────────┘  └──────────────────┘
```

---

## 🧩 Component Relationships

```
module_new.html (Structure)
        │
        ├─── Left Panel
        │    ├─ Panel Header
        │    ├─ Chat Container (id="tutorChat")
        │    └─ Chat Input
        │
        └─── Right Panel
             ├─ Submodule Tabs
             ├─ Panel Header
             ├─ Upload Section (id="uploadSection")
             ├─ Workspace Chat (id="workspaceChat")
             └─ Prompt Input (id="promptInputSection")

academy.js (Behavior)
        │
        ├─── State Variables
        │    ├─ currentStep
        │    ├─ documentUploaded
        │    ├─ promptAttempts
        │    └─ lessonComplete
        │
        ├─── Helper Functions
        │    ├─ addTutorMessage()
        │    ├─ addWorkspaceMessage()
        │    ├─ highlightElement()
        │    └─ addProactiveTip()
        │
        ├─── Lesson Flow Functions
        │    ├─ startLesson()
        │    ├─ handleDocumentUpload()
        │    ├─ handlePromptTyping()
        │    └─ handleGenerate()
        │
        └─── Event Listeners
             ├─ uploadDocBtn.click
             ├─ promptInput.input
             ├─ generateBtn.click
             └─ sendButton.click

style.css (Presentation)
        │
        ├─── Layout
        │    ├─ .split-container (grid)
        │    ├─ .left-panel (400px)
        │    └─ .right-panel (flex 1)
        │
        ├─── Highlighting
        │    ├─ .highlight-glow (red border)
        │    └─ @keyframes glowPulse
        │
        ├─── Chat
        │    ├─ .chat-message
        │    ├─ .workspace-message
        │    └─ .message-avatar
        │
        └─── Interactive
             ├─ .quiz-container
             ├─ .proactive-tip
             └─ .tab (submodule navigation)
```

---

## 🔌 API Integration (Optional)

```
Frontend (academy.js)
        │
        │ User asks free question
        ▼
┌──────────────────────┐
│ sendButton.click     │
│ Fetch POST request   │
└──────────┬───────────┘
           │
           │ JSON: { message, context }
           ▼
Backend (app.py)
┌──────────────────────┐
│ @app.route           │
│ '/api/chat'          │
└──────────┬───────────┘
           │
           │ Extract message
           ▼
┌──────────────────────┐
│ Build prompt:        │
│ "You are AI tutor... │
│ Context: ...         │
│ User: {message}"     │
└──────────┬───────────┘
           │
           ▼
Gemini API
┌──────────────────────┐
│ model.generate_      │
│ content(prompt)      │
└──────────┬───────────┘
           │
           │ AI response
           ▼
Backend Response
┌──────────────────────┐
│ JSON:                │
│ { response: "..." }  │
└──────────┬───────────┘
           │
           ▼
Frontend Display
┌──────────────────────┐
│ addTutorMessage()    │
│ Shows in chat        │
└──────────────────────┘
```

---

## 🎨 Styling Architecture

```
CSS Variables (Root)
├─ --primary: #ff3333 (red)
├─ --darker: #0d0d0d (background)
├─ --text: #f0f0f0 (light text)
└─ --glow: rgba(255,51,51,0.6)

Cascading Usage:
├─ All buttons use var(--primary)
├─ All backgrounds use var(--darker)
├─ All highlights use var(--glow)
└─ Change once, updates everywhere!

Responsive Strategy:
├─ Fixed left panel: 400px
├─ Flexible right panel: 1fr
├─ Mobile: Not prioritized (MVP)
└─ Future: Stack vertically on small screens
```

---

## ⚡ Performance Considerations

### Loading
- Minimal dependencies (just Flask)
- No heavy frameworks (React, Vue)
- Vanilla JavaScript = Fast
- CSS loaded once, cached

### Runtime
- Event delegation where possible
- Highlight class toggle (cheap)
- No complex computations
- Animations use CSS (GPU-accelerated)

### Scalability
- Current: Single lesson, hardcoded
- Future: Database for lessons
- Future: User session storage
- Future: CDN for static assets

---

## 🔐 Security Notes

### Current (MVP)
- No authentication needed
- No sensitive data
- No file uploads (sample only)
- Client-side logic only

### Future (Production)
- Add user authentication
- Validate all inputs server-side
- Sanitize HTML in messages
- Rate limit API calls
- Secure API keys

---

**Architecture complete!** This document shows how all pieces fit together.
