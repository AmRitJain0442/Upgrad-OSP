/**
 * Presentation Builder Module
 * Handles document upload, AI prompting workflow, and HTML/CSS preview
 */

// ===== STATE MANAGEMENT =====
const LessonStep = {
    WELCOME: 'welcome',
    AWAITING_UPLOAD: 'awaiting_upload',
    EXTRACTION: 'extraction',
    CONTENT_GENERATION: 'content_generation',
    REFINEMENT: 'refinement',
    CODE_GENERATION: 'code_generation',
    PREVIEW: 'preview',
    COMPLETE: 'complete'
};

const state = {
    sessionId: window.LESSON_DATA?.sessionId || '',
    moduleId: window.LESSON_DATA?.moduleId || '',
    submoduleId: window.LESSON_DATA?.submoduleId || 0,
    submodule: window.LESSON_DATA?.submodule || {},
    currentStep: LessonStep.WELCOME,
    documentUploaded: false,
    extractedData: null,
    slideContent: null,
    generatedCode: null,
    promptAttempts: 0,
    lessonComplete: false
};

// ===== DOM ELEMENTS =====
const elements = {
    tutorChat: document.getElementById('tutorChat'),
    chatInput: document.getElementById('chatInput'),
    sendButton: document.getElementById('sendButton'),
    
    workspaceChat: document.getElementById('workspaceChat'),
    uploadSection: document.getElementById('uploadSection'),
    uploadDocBtn: document.getElementById('uploadDocBtn'),
    useSampleBtn: document.getElementById('useSampleBtn'),
    fileInput: document.getElementById('fileInput'),
    
    promptInputSection: document.getElementById('promptInputSection'),
    promptInput: document.getElementById('promptInput'),
    generateBtn: document.getElementById('generateBtn'),
    
    promptAnalysis: document.getElementById('promptAnalysis'),
    analysisContent: document.getElementById('analysisContent'),
    
    previewContainer: document.getElementById('previewContainer'),
    previewFrame: document.getElementById('previewFrame'),
    refreshPreview: document.getElementById('refreshPreview'),
    fullscreenPreview: document.getElementById('fullscreenPreview'),
    
    leftPanel: document.getElementById('leftPanel'),
    rightPanel: document.getElementById('rightPanel'),
    resizeHandle: document.getElementById('resizeHandle')
};

// ===== MARKDOWN RENDERING =====
marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false,
    mangle: false
});

function parseMarkdown(text) {
    return marked.parse(text);
}

// ===== AUTO-SCROLL UTILITIES =====
function scrollToBottom(element) {
    if (element) {
        element.scrollTop = element.scrollHeight;
    }
}

// ===== CHAT FUNCTIONS =====
function addTutorMessage(content, isQuiz = false, quizData = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message ai-message';
    
    if (isQuiz) {
        messageDiv.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content">
                <p>${content}</p>
                <div class="quiz-container">
                    <div class="quiz-question">${quizData.question}</div>
                    <div class="quiz-options">
                        ${quizData.options.map((opt, idx) => `
                            <div class="quiz-option" data-correct="${idx === quizData.correct_index}" data-index="${idx}">
                                ${opt}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        setTimeout(() => {
            const options = messageDiv.querySelectorAll('.quiz-option');
            options.forEach(opt => {
                opt.addEventListener('click', function() {
                    handleQuizAnswer(this, options, quizData);
                });
            });
        }, 100);
    } else {
        const parsedContent = parseMarkdown(content);
        messageDiv.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content">${parsedContent}</div>
        `;
    }
    
    elements.tutorChat.appendChild(messageDiv);
    scrollToBottom(elements.tutorChat);
}

function addUserMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message user-message';
    messageDiv.innerHTML = `
        <div class="message-content"><p>${content}</p></div>
        <div class="message-avatar">You</div>
    `;
    
    elements.tutorChat.appendChild(messageDiv);
    scrollToBottom(elements.tutorChat);
}

function addWorkspaceMessage(content, isUser = false, skipMarkdown = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user-message' : 'ai-message'}`;
    
    let parsedContent;
    if (isUser) {
        parsedContent = `<p>${content}</p>`;
    } else if (skipMarkdown) {
        parsedContent = content;
    } else {
        parsedContent = parseMarkdown(content);
    }
    
    if (isUser) {
        messageDiv.innerHTML = `
            <div class="message-content">${parsedContent}</div>
            <div class="message-avatar">You</div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content">${parsedContent}</div>
        `;
    }
    
    elements.workspaceChat.appendChild(messageDiv);
    scrollToBottom(elements.workspaceChat);
}

// ===== CODE DETECTION AND PREVIEW =====
function detectAndExtractCode(content) {
    // Look for HTML code in the response
    const htmlRegex = /```html\s*([\s\S]*?)```/gi;
    const cssRegex = /```css\s*([\s\S]*?)```/gi;
    
    const htmlMatches = [...content.matchAll(htmlRegex)];
    const cssMatches = [...content.matchAll(cssRegex)];
    
    if (htmlMatches.length > 0 || cssMatches.length > 0) {
        let html = htmlMatches.length > 0 ? htmlMatches[0][1].trim() : '';
        let css = cssMatches.length > 0 ? cssMatches[0][1].trim() : '';
        
        // If we have both, combine them
        if (html && css) {
            return {
                hasCode: true,
                html: html,
                css: css,
                combined: `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation</title>
    <style>
        ${css}
    </style>
</head>
<body>
    ${html}
</body>
</html>
                `.trim()
            };
        } else if (html) {
            // HTML only, might have inline styles
            return {
                hasCode: true,
                html: html,
                css: '',
                combined: html.includes('<!DOCTYPE') ? html : `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation</title>
</head>
<body>
    ${html}
</body>
</html>
                `.trim()
            };
        }
    }
    
    return { hasCode: false };
}

function renderPreview(code) {
    console.log('Rendering preview with code');
    state.generatedCode = code;
    
    // Show preview container if hidden
    elements.previewContainer.style.display = 'block';
    
    // Show preview controls
    elements.refreshPreview.style.display = 'flex';
    elements.fullscreenPreview.style.display = 'flex';
    
    // Hide placeholder, show iframe
    const placeholder = elements.previewContainer.querySelector('.preview-placeholder');
    if (placeholder) placeholder.style.display = 'none';
    elements.previewFrame.style.display = 'block';
    
    // Create blob URL for the iframe
    const blob = new Blob([code], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    elements.previewFrame.src = url;
    
    // Show success message in tutor
    addTutorMessage('🎉 **Preview is ready!** Your presentation is now visible in the embedded preview below the workspace. You can navigate the slides and see your work come to life!');
}

// ===== PREVIEW CONTROLS =====
function refreshPreview() {
    if (state.generatedCode) {
        console.log('Refreshing preview');
        renderPreview(state.generatedCode);
        addTutorMessage('Preview refreshed! ');
    } else {
        addTutorMessage('No code generated yet. Complete the lesson steps to generate your presentation code.');
    }
}

function toggleFullscreen() {
    if (elements.previewFrame.requestFullscreen) {
        elements.previewFrame.requestFullscreen();
    } else if (elements.previewFrame.webkitRequestFullscreen) {
        elements.previewFrame.webkitRequestFullscreen();
    } else if (elements.previewFrame.msRequestFullscreen) {
        elements.previewFrame.msRequestFullscreen();
    }
}

// ===== STREAMING CHAT =====
async function sendChatMessage(message) {
    if (!message.trim()) return;
    
    addUserMessage(message);
    elements.chatInput.value = '';
    elements.chatInput.disabled = true;
    elements.sendButton.disabled = true;
    
    // Create streaming message
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message ai-message streaming';
    messageDiv.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content"><span class="loading-dots">Thinking...</span></div>
    `;
    elements.tutorChat.appendChild(messageDiv);
    scrollToBottom(elements.tutorChat);
    
    try {
        const response = await fetch('/prompting/api/chat/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: state.sessionId,
                message: message,
                context: `Current step: ${state.currentStep}`
            })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        
        const contentDiv = messageDiv.querySelector('.message-content');
        contentDiv.innerHTML = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) {
                        fullResponse += data.chunk;
                        contentDiv.innerHTML = parseMarkdown(fullResponse);
                        scrollToBottom(elements.tutorChat);
                    }
                }
            }
        }
        
        messageDiv.classList.remove('streaming');
        
    } catch (error) {
        console.error('Chat error:', error);
        messageDiv.querySelector('.message-content').innerHTML = 
            '<p class="error">Sorry, there was an error. Please try again.</p>';
    } finally {
        elements.chatInput.disabled = false;
        elements.sendButton.disabled = false;
        elements.chatInput.focus();
    }
}

// ===== WORKSPACE GENERATION WITH STREAMING =====
async function handleGenerate() {
    const prompt = elements.promptInput.value.trim();
    if (!prompt || !state.documentUploaded) return;
    
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = `
        <span class="loading-spinner"></span>
        Generating...
    `;
    
    addWorkspaceMessage(prompt, true);
    
    // Create streaming message
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message ai-message streaming';
    messageDiv.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content"><span class="loading-dots">Generating...</span></div>
    `;
    elements.workspaceChat.appendChild(messageDiv);
    scrollToBottom(elements.workspaceChat);
    
    try {
        const response = await fetch('/prompting/api/summarize/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: state.sessionId,
                prompt: prompt
            })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        
        const contentDiv = messageDiv.querySelector('.message-content');
        contentDiv.innerHTML = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) {
                        fullResponse += data.chunk;
                        contentDiv.innerHTML = parseMarkdown(fullResponse);
                        scrollToBottom(elements.workspaceChat);
                    }
                }
            }
        }
        
        messageDiv.classList.remove('streaming');
        
        // Check if generated content contains code
        const codeDetection = detectAndExtractCode(fullResponse);
        if (codeDetection.hasCode) {
            console.log('Code detected in response!');
            renderPreview(codeDetection.combined);
            
            // Update state
            if (state.submoduleId === 4) {
                state.currentStep = LessonStep.PREVIEW;
            }
        }
        
        // Provide feedback based on lesson
        provideLessonFeedback();
        
    } catch (error) {
        console.error('Generation error:', error);
        messageDiv.querySelector('.message-content').innerHTML = 
            '<p class="error">Sorry, there was an error generating the response.</p>';
    } finally {
        elements.generateBtn.disabled = false;
        elements.generateBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            Generate
        `;
        elements.promptInput.value = '';
    }
}

function provideLessonFeedback() {
    state.promptAttempts++;
    
    // Lesson-specific feedback logic
    setTimeout(() => {
        if (state.promptAttempts === 1 && state.submodule.success_message) {
            addTutorMessage(state.submodule.success_message);
            
            // Show quiz after first successful attempt
            setTimeout(() => {
                if (state.submodule.quiz) {
                    addTutorMessage('Let\'s test your understanding:', true, state.submodule.quiz);
                }
            }, 2000);
        }
    }, 1500);
}

// ===== QUIZ HANDLING =====
async function handleQuizAnswer(selectedOption, allOptions, quizData) {
    const selectedIndex = parseInt(selectedOption.dataset.index);
    const isCorrect = selectedIndex === quizData.correct_index;
    
    // Disable all options
    allOptions.forEach(opt => {
        opt.style.pointerEvents = 'none';
        if (parseInt(opt.dataset.index) === quizData.correct_index) {
            opt.classList.add('correct');
        } else if (opt === selectedOption && !isCorrect) {
            opt.classList.add('incorrect');
        }
    });
    
    // Show feedback
    setTimeout(() => {
        if (isCorrect) {
            addTutorMessage('✅ **Correct!** You\'ve mastered this concept. Great work!');
            state.lessonComplete = true;
            
            // Unlock next submodule
            setTimeout(() => {
                addTutorMessage('🎉 **Lesson Complete!** You can now proceed to the next lesson or continue practicing here.');
            }, 1500);
        } else {
            addTutorMessage(`❌ Not quite. The correct answer is: **${quizData.options[quizData.correct_index]}**. Take a moment to review the lesson.`);
        }
    }, 1000);
}

// ===== FILE UPLOAD =====
async function handleFileUpload(file) {
    if (!file) return;
    
    console.log('handleFileUpload called');

    if (state.documentUploaded) {
        addTutorMessage("You've already uploaded a document. Continue with your prompt!");
        return;
    }
    const MAX_FILE_SIZE = 25 * 1024 * 1024;
    if (file.size > MAX_FILE_SIZE) {
        addTutorMessage("File size exceeds 25MB limit. Please upload a smaller file.");
        return;
    }

    if (state.currentStep !== LessonStep.AWAITING_UPLOAD) {
        console.log('Not in AWAITING_UPLOAD step, transitioning...');
        transitionToStep(LessonStep.AWAITING_UPLOAD);
    }

    elements.uploadDocBtn.disabled = true;
    elements.uploadDocBtn.innerHTML = `
        <span class="loading-spinner"></span>
        Uploading...
    `;
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', state.sessionId);
    
    try {
        const response = await fetch('/prompting/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            elements.uploadSection.style.display = 'none';
            elements.workspaceChat.style.display = 'flex';
            elements.promptInputSection.style.display = 'block';
            
            addWorkspaceMessage(`
                <strong>📄 ${data.filename}</strong><br><br>
                <div style="margin: 1rem 0; padding: 1rem; background: var(--bg-tertiary); border-left: 3px solid var(--primary); border-radius: 6px;">
                    ${data.preview}
                </div>
            `, false, true);
            
            onDocumentUploaded();
        } else {
            elements.uploadDocBtn.disabled = false;
            elements.uploadDocBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                Upload Your Own
            `;
            addTutorMessage(`Sorry, there was an error: ${data.error}`);
        }
    } catch (error) {
        console.error('Upload error:', error);
        elements.uploadDocBtn.disabled = false;
        elements.uploadDocBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            Upload Your Own
        `;
        addTutorMessage('Sorry, there was a connection error. Please try again.');
    }
}

// ===== SAMPLE DOCUMENT LOADING =====
async function loadSampleDocument() {
    console.log('loadSampleDocument called');
    
    if (state.documentUploaded) {
        addTutorMessage("You've already uploaded a document. Continue with your prompt!");
        return;
    }
    
    if (state.currentStep !== LessonStep.AWAITING_UPLOAD) {
        console.log('Not in AWAITING_UPLOAD step, transitioning...');
        transitionToStep(LessonStep.AWAITING_UPLOAD);
    }
    
    elements.useSampleBtn.disabled = true;
    elements.useSampleBtn.innerHTML = `
        <span class="loading-spinner"></span>
        Loading Sample...
    `;
    
    try {
        const response = await fetch('/prompting/api/sample/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: state.sessionId,
                module_id: state.moduleId,
                submodule_id: state.submoduleId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            elements.uploadSection.style.display = 'none';
            elements.workspaceChat.style.display = 'flex';
            elements.promptInputSection.style.display = 'block';
            
            addWorkspaceMessage(`
                <strong>📄 ${data.filename}</strong><br><br>
                <div style="margin: 1rem 0; padding: 1rem; background: var(--bg-tertiary); border-left: 3px solid var(--primary); border-radius: 6px;">
                    ${data.preview}
                </div>
            `, false, true);
            
            window.fullDocumentContent = data.full_content;
            onDocumentUploaded();
        } else {
            elements.useSampleBtn.disabled = false;
            elements.useSampleBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                Use Sample Document
            `;
            addTutorMessage(`Sorry, there was an error: ${data.error}`);
        }
    } catch (error) {
        console.error('Sample load error:', error);
        elements.useSampleBtn.disabled = false;
        elements.useSampleBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
            </svg>
            Use Sample Document
        `;
        addTutorMessage('Sorry, there was a connection error. Please try again.');
    }
}

// ===== LESSON FLOW =====
function transitionToStep(newStep) {
    console.log(`Transitioning from ${state.currentStep} to ${newStep}`);
    state.currentStep = newStep;
}

function startLesson() {
    if (!state.submodule.welcome_message) return;
    
    transitionToStep(LessonStep.WELCOME);
    addTutorMessage(state.submodule.welcome_message);
    
    setTimeout(() => {
        requestDocumentUpload();
    }, 1500);
}

function requestDocumentUpload() {
    if (state.currentStep !== LessonStep.WELCOME) return;
    
    transitionToStep(LessonStep.AWAITING_UPLOAD);
    
    if (state.submodule.upload_prompt) {
        addTutorMessage(state.submodule.upload_prompt);
    }
}

function onDocumentUploaded() {
    if (state.currentStep !== LessonStep.AWAITING_UPLOAD) return;
    
    transitionToStep(LessonStep.EXTRACTION);
    state.documentUploaded = true;
    
    if (state.submodule.prompt_guidance) {
        setTimeout(() => {
            addTutorMessage(state.submodule.prompt_guidance);
        }, 1000);
    }
}

// ===== EVENT LISTENERS =====
function initEventListeners() {
    // Chat input
    if (elements.chatInput && elements.sendButton) {
        elements.sendButton.addEventListener('click', () => {
            const message = elements.chatInput.value.trim();
            if (message) {
                sendChatMessage(message);
            }
        });
        
        elements.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                elements.sendButton.click();
            }
        });
    }
    
    // Sample document
    if (elements.useSampleBtn) {
        elements.useSampleBtn.addEventListener('click', () => {
            console.log('Sample button clicked');
            if (state.currentStep === LessonStep.AWAITING_UPLOAD || !state.documentUploaded) {
                loadSampleDocument();
            }
        });
    }
    
    // File upload
    if (elements.uploadDocBtn) {
        elements.uploadDocBtn.addEventListener('click', () => {
            console.log('Upload button clicked');
            if (state.currentStep === LessonStep.AWAITING_UPLOAD || !state.documentUploaded) {
                elements.fileInput.click();
            }
        });
    }
    
    if (elements.fileInput) {
        elements.fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }
    
    // Generate button
    if (elements.generateBtn) {
        elements.generateBtn.addEventListener('click', handleGenerate);
    }
    
    // Prompt input
    if (elements.promptInput) {
        elements.promptInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                elements.generateBtn.click();
            }
        });
    }
    
    // Preview controls
    if (elements.refreshPreview) {
        elements.refreshPreview.addEventListener('click', refreshPreview);
    }
    
    if (elements.fullscreenPreview) {
        elements.fullscreenPreview.addEventListener('click', toggleFullscreen);
    }
    
    // Tab navigation
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            if (!this.classList.contains('locked')) {
                const submoduleId = this.dataset.submodule;
                const moduleId = this.dataset.module;
                window.location.href = `/prompting/module/${moduleId}/${submoduleId}`;
            }
        });
    });
}

// ===== INITIALIZATION =====
function init() {
    console.log('Initializing Presentation Builder...');
    console.log('Session:', state.sessionId);
    console.log('Module:', state.moduleId);
    console.log('Submodule:', state.submoduleId);
    
    initEventListeners();
    startLesson();
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
