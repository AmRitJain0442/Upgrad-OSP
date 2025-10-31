# Test Checklist - AI Skills Academy

## 🧪 Manual Testing Guide

### Pre-Flight Check
- [ ] Python installed (3.7+)
- [ ] Flask installed (`pip install Flask`)
- [ ] Navigate to `backend` folder
- [ ] Run `python app.py`
- [ ] Server starts on port 5000
- [ ] No errors in terminal

---

## 🏠 Homepage Testing

### Course Listing Page
- [ ] Open http://localhost:5000
- [ ] Page loads with dark theme
- [ ] "AI SKILLS ACADEMY" header visible with red gradient
- [ ] "Foundations of Prompting" course card displays
- [ ] 4 submodules listed:
  - [ ] 01: Focused Summarization
  - [ ] 02: Advanced Techniques
  - [ ] 03: Chain-of-Thought Reasoning
  - [ ] 04: Real-world Practice
- [ ] "Launch" button visible on Submodule 1
- [ ] Hover effects work on course card

---

## 📚 Lesson 1: Focused Summarization

### Initial Load
- [ ] Click "Launch" on Submodule 1
- [ ] Two-panel interface loads
- [ ] Left panel: "AI Tutor" header
- [ ] Right panel: "Workspace" header
- [ ] 4 tabs at top (01 active, others locked)
- [ ] Status shows "Online" with pulsing dot

### Step 1: Welcome Message
- [ ] Tutor message appears automatically
- [ ] Says: "Welcome to your first lesson!"
- [ ] Second message appears after 1.5 seconds
- [ ] Says: "First, please click the 'Upload Document' button"
- [ ] **Upload Document button gets RED GLOWING BORDER** ⭐

### Step 2: Document Upload
- [ ] Click the glowing "Upload Document" button
- [ ] Upload section disappears
- [ ] Workspace chat appears with document preview
- [ ] Shows "Document loaded: The Rise of Remote Work"
- [ ] Tutor says: "Great! The document is loaded..."
- [ ] After 1.5 seconds, **prompt input box glows red** ⭐

### Step 3: Bad Prompt Attempt
- [ ] Click in prompt input box (glow should remove)
- [ ] Type: "Summarize this document"
- [ ] Click Generate button (lightning icon)
- [ ] Button shows "Generating..." with loading animation
- [ ] User message appears in workspace: "Summarize this document"
- [ ] AI response includes hallucinated content (HBR, Microsoft, etc.)
- [ ] Tutor explains: "Notice how the AI mentioned..."
- [ ] Tutor suggests: "Try again with a constraint..."
- [ ] **Prompt input glows red again** ⭐

### Step 4: Proactive Suggestion (Alternative Path)
*If you type slowly instead of clicking Generate immediately:*
- [ ] Start typing: "Summarize this"
- [ ] After 10+ characters WITHOUT "based on" or "only"
- [ ] **Proactive tip appears in tutor chat** ⭐
- [ ] Styled with red left border and 💡 icon
- [ ] Says: "Remember, we want to constrain the AI..."

### Step 5: Good Prompt
- [ ] Clear prompt input or refresh
- [ ] Type: "Based only on the text provided, summarize this document"
- [ ] Click Generate
- [ ] User message appears in workspace
- [ ] AI response is focused, accurate summary (no hallucination)
- [ ] Tutor says: "Fantastic! See the difference?"

### Step 6: Interactive Quiz
- [ ] After good summary, tutor says: "Time for a quick quiz!"
- [ ] **Quiz appears embedded in tutor chat** ⭐
- [ ] Question: "Why did we add that constraint?"
- [ ] 4 options visible:
  - [ ] To make the AI work faster
  - [ ] To prevent 'hallucination' (making up facts)
  - [ ] To make the summary longer
  - [ ] To make the AI smarter
- [ ] Click wrong answer → **turns red** ⭐
- [ ] Correct answer → **turns green** ⭐
- [ ] Tutor says: "Exactly right! You've mastered..."
- [ ] **Tab 02 starts glowing red** ⭐
- [ ] Tab 02 no longer says "locked"

### Step 7: Free Chat (Optional)
- [ ] Type question in left panel chat input
- [ ] Example: "What is hallucination?"
- [ ] Click send or press Enter
- [ ] Message appears in tutor chat
- [ ] If Gemini API configured: AI responds
- [ ] If not configured: Error message (expected)

---

## 🎨 Visual Design Check

### Color Scheme
- [ ] Background is dark (#0d0d0d)
- [ ] Primary accent is red (#ff3333)
- [ ] No cyan or magenta colors visible
- [ ] Text is light gray/white
- [ ] Glow effects are red, not blue

### Typography
- [ ] Headers use Orbitron font (robotic feel)
- [ ] Body text uses Roboto Mono
- [ ] Text is readable
- [ ] Proper hierarchy (sizes make sense)

### Animations
- [ ] Glow pulse is smooth (not jarring)
- [ ] Messages slide in smoothly
- [ ] Transitions are subtle
- [ ] No janky animations
- [ ] Status indicator pulses

### Responsiveness
- [ ] Page looks good at full screen
- [ ] Left panel stays 400px wide
- [ ] Right panel fills remaining space
- [ ] Scroll works in both panels independently

---

## 🐛 Edge Cases & Error Handling

### User Mistakes
- [ ] Click Generate with empty prompt → Shows error message
- [ ] Type only whitespace → Prompt not submitted
- [ ] Spam click Generate → Button disables during generation
- [ ] Fast typing → Proactive tip doesn't spam

### Navigation
- [ ] Click "Back to Courses" → Returns to homepage
- [ ] Click locked tab 02-04 → Shows "under development" alert
- [ ] Refresh page → Lesson restarts (expected behavior)

### Browser Console
- [ ] Open DevTools (F12)
- [ ] Check Console tab
- [ ] No JavaScript errors
- [ ] academy.js loaded successfully
- [ ] style.css loaded successfully

---

## ✅ Success Criteria

### Must Pass (Critical)
- [x] Visual highlighting works (glowing red borders)
- [x] Proactive suggestion appears while typing
- [x] Quiz is interactive and clickable
- [x] Good vs bad prompt comparison works
- [x] Tab unlocks after quiz completion

### Should Pass (Important)
- [x] All tutor messages appear in correct order
- [x] Workspace chat displays user and AI messages
- [x] Animations are smooth
- [x] Design is clean and professional
- [x] No console errors

### Nice to Have (Polish)
- [ ] Page loads in under 2 seconds
- [ ] Animations feel natural (timing)
- [ ] Copy is encouraging and clear
- [ ] Mobile responsive (not required)

---

## 📝 Test Results Template

```
Date: _______
Tester: _______
Browser: _______
OS: _______

Homepage: PASS / FAIL
Notes: _______

Lesson Flow: PASS / FAIL
Notes: _______

Highlighting: PASS / FAIL
Notes: _______

Proactive Tips: PASS / FAIL
Notes: _______

Quiz System: PASS / FAIL
Notes: _______

Visual Design: PASS / FAIL
Notes: _______

Overall: PASS / FAIL
```

---

## 🚨 Known Limitations (Not Bugs)

1. **No Real Upload**: File input doesn't actually upload - sample doc is hardcoded
2. **No Persistence**: Refresh loses progress (no database)
3. **Gemini API**: Chat Q&A requires API key setup
4. **Submodules 2-4**: Not implemented yet (by design)
5. **No Authentication**: No user accounts

These are intentional for the MVP/demo.

---

## 🎯 Testing Tips

1. **Test twice**: Once with bad prompt first, once with good prompt first
2. **Type slowly**: To trigger proactive suggestion
3. **Try different prompts**: Test the constraint detection logic
4. **Check all clicks**: Every button should do something
5. **Read console**: Catch any hidden errors

---

**Happy Testing!** 🧪

If you find issues, check:
1. `academy.js` line numbers in error message
2. Browser compatibility (Chrome/Edge recommended)
3. Flask server is running
4. Files are in correct directories
