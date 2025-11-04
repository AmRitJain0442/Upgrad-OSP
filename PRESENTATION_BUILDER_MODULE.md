# AI-Powered Presentation Builder Module

## Overview

The **Presentation Builder** is a new module added to the Upgrad OSP platform that teaches users how to create professional HTML/CSS presentations from documents using AI prompting techniques.

## Module Structure

### 4 Progressive Lessons

#### Lesson 1: Document Analysis & Information Extraction

**Objective**: Learn to extract structured information from documents for presentation content

**Key Skills**:

- Prompting AI to identify main topics and sections
- Extracting key points and supporting details
- Structuring information for slide format
- Specifying format requirements (sections, bullet points, quotes)

**Example Prompt**:

```
Extract from this document:
1) Main title/topic
2) 3-5 key sections with headings
3) 2-3 bullet points per section
4) Any important data or quotes
```

---

#### Lesson 2: Content Generation for Slides

**Objective**: Master prompting AI to generate presentation-ready content

**Key Skills**:

- Creating slide titles and descriptions
- Generating concise bullet points
- Writing speaker notes
- Applying length and style constraints

**Example Prompt**:

```
Based on this document, create content for 5-7 presentation slides.
For each slide provide:
1) A catchy title
2) 3-4 concise bullet points (under 15 words each)
3) A brief speaker note
Format: Professional, suitable for business presentation
```

---

#### Lesson 3: Content Refinement & Validation

**Objective**: Learn to iterate and improve AI-generated content

**Key Skills**:

- Reviewing content for accuracy
- Making specific refinement requests
- Ensuring information flows logically
- Cross-validating against source document

**Example Prompt**:

```
Review slide 3:
1) Shorten bullet 2 to under 10 words
2) Replace generic terms with specific examples from the document
3) Add a transition phrase connecting to the next slide
4) Ensure all facts are from the original document
```

---

#### Lesson 4: HTML/CSS Code Generation

**Objective**: Generate complete, runnable presentation code

**Key Skills**:

- Specifying design requirements
- Requesting interactive features (navigation, transitions)
- Ensuring responsive design
- Including keyboard controls

**Example Prompt**:

```
Create an HTML/CSS presentation with:
1) Full-screen slides with centered content
2) Navigation buttons (prev/next/slide numbers)
3) Smooth fade transitions between slides
4) Dark theme with accent colors
5) Mobile-responsive layout
6) Keyboard controls (arrow keys for navigation)
Output complete code ready to run in a browser.
```

---

## Features

### Triple-Panel Interface

**Left Panel: AI Tutor**

- Real-time guidance and feedback
- Contextual tips based on lesson progress
- Chat interface for questions
- Streaming responses for natural interaction

**Middle Panel: Workspace**

- Document upload (PDF, DOCX, TXT) or sample documents
- Prompt input with real-time analysis
- AI-generated responses with markdown formatting
- Code highlighting for generated HTML/CSS

**Right Panel: Live Preview**

- Real-time rendering of generated presentations
- Iframe-based isolated preview
- Refresh and fullscreen controls
- Automatic preview update when code is detected

### Code Detection & Rendering

The system automatically detects HTML/CSS code blocks in AI responses:

````javascript
// Regex patterns for code detection
const htmlRegex = /```html\s*([\s\S]*?)```/gi;
const cssRegex = /```css\s*([\s\S]*?)```/gi;
````

When code is detected:

1. Extracts HTML and CSS from markdown code blocks
2. Combines them into a complete HTML document
3. Creates a Blob URL for secure iframe rendering
4. Displays preview in the right panel
5. Notifies user that preview is ready

### Sample Documents

Two comprehensive documents included for practice:

**AI Healthcare Report** (Lessons 1-2)

- Professional healthcare industry report
- Multiple sections with data and statistics
- Perfect for extraction and content generation practice

**Climate Change Guide** (Lessons 3-4)

- Comprehensive climate science overview
- Rich content for refinement exercises
- Ideal for full presentation generation

---

## Technical Implementation

### New Files Created

#### Backend

- **Modified**: `app/prompting/curriculum.py` - Added presentation-builder module
- **Modified**: `app/prompting/router.py` - Route handling for new module

#### Frontend

- **New**: `frontend/templates/prompting/presentation_module.html` - Triple-panel template
- **New**: `frontend/static/js/presentation_builder.js` - Module JavaScript (1040 lines)
- **Modified**: `frontend/static/css/prompting.css` - Styles for triple-panel layout

#### Sample Documents

- **New**: `frontend/static/samples/ai_healthcare_report.txt`
- **New**: `frontend/static/samples/climate_change_guide.txt`
- **Modified**: `frontend/static/samples/document_mapping.json` - Added mappings

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Builder                      │
├─────────────────┬─────────────────┬─────────────────────────┤
│   AI Tutor      │   Workspace     │   Preview Panel         │
│                 │                 │                         │
│ • Guidance      │ • Upload        │ • Live Rendering        │
│ • Feedback      │ • Prompting     │ • Navigation            │
│ • Quiz          │ • Generation    │ • Fullscreen            │
│ • Streaming     │ • Code Display  │ • Refresh               │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### Key JavaScript Functions

**Code Detection**:

```javascript
detectAndExtractCode(content);
// Extracts HTML/CSS from markdown code blocks
```

**Preview Rendering**:

```javascript
renderPreview(code);
// Creates blob URL and renders in iframe
```

**Streaming Generation**:

```javascript
handleGenerate();
// Streams AI responses and detects code
```

---

## User Workflow

### Step-by-Step Process

1. **Choose Module**: Select "AI-Powered Presentation Builder" from course list
2. **Upload Document**: Use sample or upload own document (PDF/DOCX/TXT)
3. **Extract Information**: Learn to prompt for structured data extraction
4. **Generate Content**: Create slide-ready content with AI assistance
5. **Refine Content**: Iterate and improve using specific prompts
6. **Generate Code**: Prompt AI to create HTML/CSS presentation
7. **Preview Live**: See rendered presentation in right panel
8. **Navigate Slides**: Use navigation controls or keyboard arrows
9. **Refine Design**: Adjust prompts to modify appearance
10. **Complete Quiz**: Test understanding of concepts

---

## API Endpoints Used

- `POST /prompting/api/sample/load` - Load sample documents
- `POST /prompting/api/upload` - Handle document uploads
- `POST /prompting/api/chat/stream` - Stream tutor responses
- `POST /prompting/api/summarize/stream` - Stream workspace AI responses
- `POST /prompting/api/quiz/submit` - Validate quiz answers

---

## Educational Objectives

### Learning Outcomes

By completing this module, users will:

✅ Understand how to structure complex prompts for multi-step tasks
✅ Master techniques for extracting structured information
✅ Learn to specify format and constraint requirements
✅ Develop skills in iterative prompt refinement
✅ Gain experience in code generation prompting
✅ Understand the importance of specificity in technical prompts

### Skill Progression

**Beginner → Intermediate → Advanced**

- **Beginner**: Simple extraction prompts
- **Intermediate**: Structured content generation with constraints
- **Advanced**: Complex code generation with multiple requirements

---

## Preview Panel Features

### Controls

**Refresh Button** (↻)

- Reloads the current preview
- Useful after making manual edits

**Fullscreen Button** (⛶)

- Expands preview to full screen
- Better viewing for presentations
- ESC to exit fullscreen

### Security

- Iframe sandboxing for isolated code execution
- Blob URLs for secure content delivery
- No external resource loading (CSP-safe)
- Code runs in isolated context

---

## Example Generated Presentation

A well-prompted AI will generate presentations with:

### HTML Structure

```html
<!DOCTYPE html>
<html>
  <head>
    <title>AI in Healthcare</title>
    <style>
      /* Clean, professional styling */
    </style>
  </head>
  <body>
    <div class="slide">
      <h1>Slide Title</h1>
      <ul>
        <li>Key Point 1</li>
        <li>Key Point 2</li>
        <li>Key Point 3</li>
      </ul>
    </div>
    <!-- Navigation -->
    <div class="nav">
      <button id="prev">←</button>
      <span id="counter">1/7</span>
      <button id="next">→</button>
    </div>
    <script>
      // Slide navigation logic
    </script>
  </body>
</html>
```

### Features

- Full-screen slides
- Smooth transitions
- Keyboard navigation (arrow keys)
- Progress indicator
- Responsive design
- Professional typography
- Consistent color scheme

---

## Troubleshooting

### Issue: Preview not showing

**Solution**:

- Ensure code blocks are properly formatted with `html and `css
- Check browser console for errors
- Click refresh button to reload
- Verify HTML is valid (opening/closing tags match)

### Issue: Transitions not smooth

**Solution**:

- Prompt AI to add CSS transitions
- Specify "smooth fade between slides" in prompt
- Include animation duration (e.g., "0.3s transition")

### Issue: Navigation not working

**Solution**:

- Ensure JavaScript is included in generated code
- Prompt for "keyboard arrow controls"
- Check that event listeners are attached
- Verify button IDs match JavaScript selectors

---

## Future Enhancements

Potential improvements for future versions:

- [ ] **Export Functionality**: Download generated HTML as a file
- [ ] **Template Library**: Pre-built presentation templates
- [ ] **Theme Customization**: Color scheme selector
- [ ] **Slide Library**: Reusable slide components
- [ ] **Collaboration**: Share presentations with others
- [ ] **PDF Export**: Convert HTML presentation to PDF
- [ ] **Analytics**: Track slide views and time spent
- [ ] **Animation Library**: Pre-built slide transitions

---

## Testing the Module

### Quick Test

1. Start server: `python -m uvicorn main:app --reload`
2. Open: http://127.0.0.1:8000
3. Click "AI-Powered Presentation Builder"
4. Complete Lesson 1: "Document Analysis"
5. Click "Use Sample Document"
6. Follow AI tutor guidance
7. Try example prompts
8. View results in workspace
9. Progress through all 4 lessons
10. Generate full presentation in Lesson 4
11. See live preview in right panel

### Verify Features

- ✅ Triple-panel layout working
- ✅ Document upload functioning
- ✅ Sample documents loading
- ✅ AI tutor streaming responses
- ✅ Workspace generation working
- ✅ Code detection operating
- ✅ Preview rendering correctly
- ✅ Navigation controls functional
- ✅ Fullscreen mode working
- ✅ Quizzes displaying and validating

---

## Conclusion

The Presentation Builder module represents a significant addition to the Upgrad OSP platform, teaching practical AI prompting skills for a real-world use case. By guiding users through the complete workflow—from document analysis to live HTML/CSS presentation—it demonstrates the power of well-crafted prompts in creating complex, functional outputs.

The module combines:

- **Pedagogy**: Progressive skill building across 4 lessons
- **Technology**: Real-time AI streaming, code detection, live preview
- **User Experience**: Intuitive triple-panel interface
- **Practicality**: Immediately usable outputs

Users emerge with both prompting skills and tangible presentations they can actually use.

---

## Access the Module

**URL**: http://127.0.0.1:8000/prompting/module/presentation-builder/1

**Course Page**: http://127.0.0.1:8000/prompting/

The new "AI-Powered Presentation Builder" card will appear in the course list alongside the existing modules.

Enjoy creating presentations with AI! 🎨✨
