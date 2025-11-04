/**
 * Upgrad OSP - Prompt Engineering Platform
 * Main JavaScript application with streaming, markdown, and interactive features
 */

// ===== STATE MANAGEMENT =====
const LessonStep = {
    WELCOME: 'welcome',
    AWAITING_UPLOAD: 'awaiting_upload',
    AWAITING_PROMPT: 'awaiting_prompt',
    GENERATING: 'generating',
    REVIEWING_OUTPUT: 'reviewing_output',
    QUIZ: 'quiz',
    COMPLETE: 'complete'
};

const state = {
    sessionId: window.LESSON_DATA?.sessionId || '',
    moduleId: window.LESSON_DATA?.moduleId || '',
    submoduleId: window.LESSON_DATA?.submoduleId || 0,
    submodule: window.LESSON_DATA?.submodule || {},
    currentStep: LessonStep.WELCOME,
    documentUploaded: false,
    promptAttempts: 0,
    lessonComplete: false,
    analysisTimeout: null,
    lastGeneratedOutput: null,
    hintsShown: []
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
            <div class="message-content">
                ${parsedContent}
            </div>
        `;
    }
    
    elements.tutorChat.appendChild(messageDiv);
    scrollToBottom(elements.tutorChat);
}

function addUserMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${content}</p>
        </div>
        <div class="message-avatar">YOU</div>
    `;
    elements.tutorChat.appendChild(messageDiv);
    scrollToBottom(elements.tutorChat);
}

function addProactiveTip(tip) {
    const tipDiv = document.createElement('div');
    tipDiv.className = 'chat-message ai-message';
    const parsedTip = parseMarkdown(tip);
    tipDiv.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content">
            <div class="proactive-tip">
                <div class="tip-header">Proactive Suggestion</div>
                ${parsedTip}
            </div>
        </div>
    `;
    elements.tutorChat.appendChild(tipDiv);
    scrollToBottom(elements.tutorChat);
}

function addWorkspaceMessage(content, isUser = false, skipMarkdown = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `workspace-message ${isUser ? 'user' : 'ai'}`;
    
    let parsedContent;
    if (isUser) {
        parsedContent = `<p>${content}</p>`;
    } else if (skipMarkdown) {
        parsedContent = content; // Use raw HTML
    } else {
        parsedContent = parseMarkdown(content);
    }
    
    messageDiv.innerHTML = `
        <span class="message-label">${isUser ? 'You' : 'Workspace AI'}</span>
        <div class="workspace-bubble">${parsedContent}</div>
    `;
    elements.workspaceChat.appendChild(messageDiv);
    scrollToBottom(elements.workspaceChat);
}

// ===== STREAMING FUNCTIONS =====
async function streamTutorChat(message, context = '') {
    try {
        const response = await fetch('/prompting/api/chat/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                context,
                session_id: state.sessionId
            })
        });
        
        if (!response.ok) throw new Error('Stream failed');
        
        // Create a placeholder message
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message ai-message';
        messageDiv.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content"><span class="loading-spinner"></span></div>
        `;
        elements.tutorChat.appendChild(messageDiv);
        
        const contentDiv = messageDiv.querySelector('.message-content');
        let fullText = '';
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) {
                        fullText += data.chunk;
                        contentDiv.innerHTML = parseMarkdown(fullText);
                        scrollToBottom(elements.tutorChat);
                    }
                    if (data.done) break;
                }
            }
        }
        
        scrollToBottom(elements.tutorChat);
    } catch (error) {
        console.error('Streaming error:', error);
        addTutorMessage('Sorry, I encountered an error. Please try again.');
    }
}

async function streamWorkspaceSummary(prompt) {
    try {
        const response = await fetch('/prompting/api/summarize/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                session_id: state.sessionId
            })
        });
        
        if (!response.ok) throw new Error('Stream failed');
        
        // Create a placeholder message
        const messageDiv = document.createElement('div');
        messageDiv.className = 'workspace-message ai';
        messageDiv.innerHTML = `
            <span class="message-label">Workspace AI</span>
            <div class="workspace-bubble"><span class="loading-spinner"></span></div>
        `;
        elements.workspaceChat.appendChild(messageDiv);
        
        const bubbleDiv = messageDiv.querySelector('.workspace-bubble');
        let fullText = '';
        let hasConstraints = false;
        let metadata = {};
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) {
                        fullText += data.chunk;
                        bubbleDiv.innerHTML = parseMarkdown(fullText);
                        scrollToBottom(elements.workspaceChat);
                    }
                    if (data.done && data.metadata) {
                        hasConstraints = data.metadata.has_constraints;
                        metadata = data.metadata;
                    }
                }
            }
        }
        
        scrollToBottom(elements.workspaceChat);
        
        // Store the output
        state.lastGeneratedOutput = fullText;
        
        // Transition to reviewing state
        transitionToStep(LessonStep.REVIEWING_OUTPUT);
        
        // Provide feedback after a brief delay
        setTimeout(() => {
            provideFeedback(hasConstraints, metadata);
        }, 1000);
        
    } catch (error) {
        console.error('Streaming error:', error);
        addWorkspaceMessage('An error occurred during summarization. Please try again.');
        
        // Return to prompt awaiting state on error
        transitionToStep(LessonStep.AWAITING_PROMPT);
        setTimeout(() => {
            highlightElement(elements.promptInput);
        }, 500);
    }
}

// ===== PROMPT ANALYSIS =====
async function analyzePrompt(prompt) {
    if (prompt.length < 10) {
        elements.promptAnalysis.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch('/prompting/api/prompt/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                session_id: state.sessionId
            })
        });
        
        if (!response.ok) return;
        
        const analysis = await response.json();
        
        if (analysis.suggestions && analysis.suggestions.length > 0) {
            elements.analysisContent.innerHTML = `
                <p style="margin-bottom: 0.5rem;">${analysis.feedback}</p>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    ${analysis.suggestions.map(s => `<li>${s}</li>`).join('')}
                </ul>
            `;
            elements.promptAnalysis.style.display = 'block';
        } else {
            elements.promptAnalysis.style.display = 'none';
        }
    } catch (error) {
        console.error('Analysis error:', error);
    }
}

// Debounced prompt analysis
function debouncedAnalyze() {
    clearTimeout(state.analysisTimeout);
    state.analysisTimeout = setTimeout(() => {
        const prompt = elements.promptInput.value.trim();
        if (prompt && state.documentUploaded) {
            analyzePrompt(prompt);
        }
    }, 500);
}

// ===== LESSON FLOW STATE MACHINE =====

/**
 * Transition to a new lesson step with validation
 */
function transitionToStep(newStep) {
    console.log(`Transitioning from ${state.currentStep} to ${newStep}`);
    state.currentStep = newStep;
    
    // Clear highlights when transitioning
    unhighlightAll();
}

/**
 * Start the lesson flow
 */
function startLesson() {
    if (!state.submodule.welcome_message) return;
    
    transitionToStep(LessonStep.WELCOME);
    addTutorMessage(state.submodule.welcome_message);
    
    // Move to upload step after welcome
    setTimeout(() => {
        requestDocumentUpload();
    }, 1500);
}

/**
 * Request document upload from user
 */
function requestDocumentUpload() {
    if (state.currentStep !== LessonStep.WELCOME) return;
    
    transitionToStep(LessonStep.AWAITING_UPLOAD);
    
    if (state.submodule.upload_prompt) {
        addTutorMessage(state.submodule.upload_prompt);
    }
    
    // Highlight sample button (preferred option)
    setTimeout(() => {
        highlightElement(elements.useSampleBtn);
    }, 500);
}

/**
 * Handle successful document upload
 */
function onDocumentUploaded() {
    if (state.currentStep !== LessonStep.AWAITING_UPLOAD) return;
    
    transitionToStep(LessonStep.AWAITING_PROMPT);
    state.documentUploaded = true;
    
    // Show prompt guidance
    if (state.submodule.prompt_guidance) {
        setTimeout(() => {
            addTutorMessage(state.submodule.prompt_guidance);
            
            // Highlight the prompt input
            setTimeout(() => {
                highlightElement(elements.promptInput);
            }, 1000);
        }, 1000);
    }
}

/**
 * Provide intelligent feedback based on output quality
 */
function provideFeedback(hasConstraints, outputMetadata = {}) {
    if (state.currentStep !== LessonStep.REVIEWING_OUTPUT) return;
    
    state.promptAttempts++;
    
    if (hasConstraints) {
        // Success path - constraints met
        transitionToStep(LessonStep.QUIZ);
        
        setTimeout(() => {
            unhighlightAll();
            addTutorMessage(state.submodule.success_message || 'Excellent work!');
            
            // Show quiz after successful completion
            if (state.submodule.quiz) {
                setTimeout(() => {
                    addTutorMessage('Now let\'s test your understanding with a quick quiz!', true, state.submodule.quiz);
                }, 2000);
            } else {
                // No quiz, mark as complete
                onLessonComplete();
            }
        }, 1000);
    } else {
        // Needs improvement - provide progressive hints
        transitionToStep(LessonStep.AWAITING_PROMPT);
        
        setTimeout(() => {
            const message = state.submodule.retry_message || 'Good start! Try improving your prompt.';
            addTutorMessage(message);
            
            // Progressive hint system
            provideProgressiveHint();
            
            // Re-highlight the prompt input
            setTimeout(() => {
                highlightElement(elements.promptInput);
            }, 2000);
        }, 1500);
    }
}

/**
 * Progressive hint system - shows different tips based on attempts
 */
function provideProgressiveHint() {
    const attemptNumber = state.promptAttempts;
    
    // First attempt: Show the weak prompt tip
    if (attemptNumber === 1 && state.submodule.weak_prompt_tip && !state.hintsShown.includes('weak_tip')) {
        setTimeout(() => {
            addProactiveTip(state.submodule.weak_prompt_tip);
            state.hintsShown.push('weak_tip');
        }, 1500);
    }
    // Second attempt: More specific guidance
    else if (attemptNumber === 2 && !state.hintsShown.includes('second_attempt')) {
        setTimeout(() => {
            const specificGuidance = getSpecificGuidance(state.submoduleId);
            if (specificGuidance) {
                addProactiveTip(specificGuidance);
                state.hintsShown.push('second_attempt');
            }
        }, 1500);
    }
    // Third attempt: Very explicit example
    else if (attemptNumber >= 3 && !state.hintsShown.includes('example')) {
        setTimeout(() => {
            const example = getExamplePrompt(state.submoduleId);
            if (example) {
                addProactiveTip(`Here's an example structure you could use:\n\n${example}`);
                state.hintsShown.push('example');
            }
        }, 1500);
    }
}

/**
 * Get specific guidance based on submodule
 */
function getSpecificGuidance(submoduleId) {
    const guidance = {
        1: "Try starting your prompt with a phrase like '<strong>Using only the information in the document</strong>' or '<strong>Based solely on the provided text</strong>'.",
        2: "Remember to assign a specific role! Start with '<strong>You are a [specific expert/professional]</strong>' before giving instructions.",
        3: "Include '<strong>Let's think step by step</strong>' or '<strong>First... Then... Finally...</strong>' to trigger chain-of-thought reasoning.",
        4: "Combine all techniques: Start with a role, add constraints, and request step-by-step analysis."
    };
    
    return guidance[submoduleId] || null;
}

/**
 * Get example prompt based on submodule
 */
function getExamplePrompt(submoduleId) {
    const examples = {
        1: "<strong>Based only on the text provided</strong>, summarize the key points without adding any external information.",
        2: "<strong>You are an expert analyst.</strong> Review this document and provide insights from your professional perspective.",
        3: "<strong>Let's analyze this step by step:</strong>\n1. First, identify the main themes\n2. Then, examine the evidence\n3. Finally, draw conclusions",
        4: "<strong>You are a senior consultant.</strong> Using only the information provided, analyze this document step by step: First, identify key issues. Then, evaluate implications. Finally, provide recommendations."
    };
    
    return examples[submoduleId] || null;
}

/**
 * Handle lesson completion
 */
function onLessonComplete() {
    transitionToStep(LessonStep.COMPLETE);
    state.lessonComplete = true;
    
    // Unlock next submodule
    unlockNextSubmodule();
}

/**
 * Handle quiz answer selection
 */
async function handleQuizAnswer(selectedOption, allOptions, quizData) {
    if (state.currentStep !== LessonStep.QUIZ) return;
    
    const isCorrect = selectedOption.dataset.correct === 'true';
    const answerIndex = parseInt(selectedOption.dataset.index);
    
    // Disable all options
    allOptions.forEach(opt => opt.style.pointerEvents = 'none');
    
    if (isCorrect) {
        selectedOption.classList.add('correct');
        
        // Submit quiz answer
        try {
            await fetch('/prompting/api/quiz/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: `${state.moduleId}-${state.submoduleId}`,
                    answer_index: answerIndex,
                    session_id: state.sessionId
                })
            });
        } catch (error) {
            console.error('Quiz submission error:', error);
        }
        
        setTimeout(() => {
            addTutorMessage("Exactly right! You've mastered this concept. Great work on this lesson!");
            
            // Complete the lesson
            onLessonComplete();
        }, 1500);
    } else {
        selectedOption.classList.add('incorrect');
        const correctOption = Array.from(allOptions).find(opt => opt.dataset.correct === 'true');
        setTimeout(() => {
            correctOption.classList.add('correct');
            
            // Provide encouragement
            setTimeout(() => {
                addTutorMessage("Not quite, but you're learning! Review the lesson concepts and try again.");
            }, 1000);
        }, 500);
    }
}

/**
 * Unlock the next submodule
 */
function unlockNextSubmodule() {
    const nextSubmoduleId = state.submoduleId + 1;
    const tabs = document.querySelectorAll('.tab');
    
    let nextTab = null;
    tabs.forEach(tab => {
        if (parseInt(tab.dataset.submodule) === nextSubmoduleId) {
            tab.classList.remove('locked');
            nextTab = tab;
        }
    });
    
    if (nextTab) {
        setTimeout(() => {
            highlightElement(nextTab);
            addTutorMessage(`Excellent! You've unlocked the next lesson. Click on <strong>${nextTab.textContent.trim()}</strong> when you're ready to continue!`);
        }, 1000);
    } else {
        // No more lessons in this module
        setTimeout(() => {
            addTutorMessage("🎉 Congratulations! You've completed all lessons in this module. You're becoming a prompting expert!");
        }, 1000);
    }
}

// ===== SAMPLE DOCUMENT =====
async function loadSampleDocument() {
    console.log('loadSampleDocument called, step:', state.currentStep, 'doc uploaded:', state.documentUploaded);
    
    // Only allow if document hasn't been uploaded yet
    if (state.documentUploaded) {
        addTutorMessage("You've already uploaded a document. Continue with your prompt!");
        return;
    }
    
    // If not in the right step, transition to it
    if (state.currentStep !== LessonStep.AWAITING_UPLOAD) {
        console.log('Not in AWAITING_UPLOAD step, transitioning...');
        transitionToStep(LessonStep.AWAITING_UPLOAD);
    }
    
    unhighlightAll();
    
    // Show loading state
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
            // Hide upload section, show workspace
            elements.uploadSection.style.display = 'none';
            elements.workspaceChat.style.display = 'flex';
            elements.promptInputSection.style.display = 'block';
            
            // Show document with option to view full content
            const cleanPreview = data.preview.replace(/\s+/g, ' ').trim();
            addWorkspaceMessage(`
                <strong>📄 ${data.filename}</strong><br><br>
                <div style="margin: 1rem 0; padding: 1rem; background: var(--bg-tertiary); border-left: 3px solid var(--primary); border-radius: 6px;">
                    ${cleanPreview}
                </div>
                <button onclick="showFullDocument()" class="view-full-btn" style="margin-top: 0.5rem; padding: 0.5rem 1rem; background: var(--primary); color: white; border: none; border-radius: 6px; cursor: pointer; font-family: var(--font-body); font-size: 0.875rem; transition: all 0.2s ease;">
                    📖 View Full Document
                </button>
            `, false, true);
            
            // Store full content for viewing
            window.fullDocumentContent = data.full_content;
            
            // Trigger document uploaded flow
            onDocumentUploaded();
        } else {
            // Show error
            elements.useSampleBtn.disabled = false;
            elements.useSampleBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                Use Sample Document
            `;
            addTutorMessage(`Sorry, there was an error loading the sample: ${data.error}. Please try uploading your own document.`);
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

// Show full document in a modal-like view
window.showFullDocument = function() {
    if (!window.fullDocumentContent) return;
    
    // Parse markdown for the full document
    const formattedContent = parseMarkdown(window.fullDocumentContent);
    
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    `;
    
    modal.innerHTML = `
        <div style="
            background: var(--bg-primary);
            max-width: 900px;
            max-height: 85vh;
            overflow-y: auto;
            padding: 2.5rem;
            border-radius: 12px;
            position: relative;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        ">
            <button onclick="this.closest('div').parentElement.remove()" style="
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: var(--bg-secondary);
                color: var(--text-primary);
                border: none;
                width: 36px;
                height: 36px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.5rem;
                line-height: 1;
                transition: all 0.2s ease;
            " onmouseover="this.style.background='var(--primary)'; this.style.color='white';" onmouseout="this.style.background='var(--bg-secondary)'; this.style.color='var(--text-primary)';">×</button>
            <h2 style="font-family: var(--font-display); margin-bottom: 1.5rem; color: var(--primary); font-size: 1.5rem;">📄 Full Document</h2>
            <div class="markdown-content" style="
                font-family: var(--font-body);
                font-size: 0.938rem;
                line-height: 1.7;
                color: var(--text-primary);
            ">${formattedContent}</div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.remove();
    });
};

// ===== FILE UPLOAD =====
async function handleFileUpload(file) {
    if (!file) return;
    
    console.log('handleFileUpload called, step:', state.currentStep, 'doc uploaded:', state.documentUploaded);
    
    // Only allow if document hasn't been uploaded yet
    if (state.documentUploaded) {
        addTutorMessage("You've already uploaded a document. Continue with your prompt!");
        return;
    }
    
    // If not in the right step, transition to it
    if (state.currentStep !== LessonStep.AWAITING_UPLOAD) {
        console.log('Not in AWAITING_UPLOAD step, transitioning...');
        transitionToStep(LessonStep.AWAITING_UPLOAD);
    }
    
    unhighlightAll();
    
    // Show uploading state
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
            // Hide upload section, show workspace
            elements.uploadSection.style.display = 'none';
            elements.workspaceChat.style.display = 'flex';
            elements.promptInputSection.style.display = 'block';
            
            // Show document preview in workspace
            const cleanPreview = data.preview.replace(/\s+/g, ' ').trim();
            addWorkspaceMessage(`
                <strong>📄 ${data.filename}</strong><br><br>
                <div style="margin: 1rem 0; padding: 1rem; background: var(--bg-tertiary); border-left: 3px solid var(--primary); border-radius: 6px;">
                    ${cleanPreview}
                </div>
            `, false, true);
            
            // Trigger document uploaded flow
            onDocumentUploaded();
        } else {
            // Show error
            elements.uploadDocBtn.disabled = false;
            elements.uploadDocBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                Upload Document
            `;
            addTutorMessage(`Oops! There was an error: ${data.error}. Please try again with a PDF, DOCX, or TXT file.`);
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
            Upload Document
        `;
        addTutorMessage('Sorry, there was a connection error. Please make sure the server is running and try again.');
    }
}

// ===== GENERATE SUMMARY =====
async function handleGenerate() {
    const prompt = elements.promptInput.value.trim();
    
    // Validation
    if (!prompt) {
        highlightElement(elements.promptInput);
        addTutorMessage('Please type a prompt first!');
        return;
    }
    
    if (state.currentStep !== LessonStep.AWAITING_PROMPT) {
        addTutorMessage("Please wait for the current step to complete.");
        return;
    }
    
    if (!state.documentUploaded) {
        addTutorMessage('Please upload a document first!');
        return;
    }
    
    // Transition to generating state
    transitionToStep(LessonStep.GENERATING);
    elements.promptAnalysis.style.display = 'none';
    
    // Add user message to workspace
    addWorkspaceMessage(prompt, true);
    
    // Disable generate button
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<span class="loading-spinner"></span>';
    
    // Clear prompt input
    elements.promptInput.value = '';
    
    // Stream the response
    await streamWorkspaceSummary(prompt);
    
    // Re-enable generate button
    elements.generateBtn.disabled = false;
    elements.generateBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        Generate
    `;
}

// ===== HIGHLIGHTING =====
function highlightElement(element) {
    unhighlightAll();
    if (element) {
        element.classList.add('highlight-glow');
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function unhighlightAll() {
    document.querySelectorAll('.highlight-glow').forEach(el => {
        el.classList.remove('highlight-glow');
    });
}

// ===== RESIZABLE PANEL =====
function initResizePanel() {
    if (!elements.resizeHandle) return;
    
    let isResizing = false;
    
    elements.resizeHandle.addEventListener('mousedown', (e) => {
        isResizing = true;
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        
        const containerRect = elements.leftPanel.parentElement.getBoundingClientRect();
        const leftWidth = e.clientX - containerRect.left;
        const leftPercent = (leftWidth / containerRect.width) * 100;
        
        if (leftPercent > 25 && leftPercent < 75) {
            elements.leftPanel.style.width = `${leftPercent}%`;
        }
    });
    
    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });
}

// ===== EVENT LISTENERS =====
function initEventListeners() {
    // Chat input
    if (elements.sendButton) {
        elements.sendButton.addEventListener('click', async () => {
            const message = elements.chatInput.value.trim();
            if (message) {
                addUserMessage(message);
                elements.chatInput.value = '';
                await streamTutorChat(message, state.submodule.title || '');
            }
        });
    }
    
    if (elements.chatInput) {
        elements.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                elements.sendButton.click();
            }
        });
    }
    
    // Sample document
    if (elements.useSampleBtn) {
        elements.useSampleBtn.addEventListener('click', () => {
            console.log('Sample button clicked, current step:', state.currentStep);
            // Allow if in awaiting upload step OR if document not uploaded yet
            if (state.currentStep === LessonStep.AWAITING_UPLOAD || !state.documentUploaded) {
                loadSampleDocument();
            } else {
                console.warn('Sample button clicked but step is:', state.currentStep);
            }
        });
    }
    
    // File upload
    if (elements.uploadDocBtn) {
        elements.uploadDocBtn.addEventListener('click', () => {
            console.log('Upload button clicked, current step:', state.currentStep);
            // Allow if in awaiting upload step OR if document not uploaded yet
            if (state.currentStep === LessonStep.AWAITING_UPLOAD || !state.documentUploaded) {
                elements.fileInput.click();
            } else {
                console.warn('Upload button clicked but step is:', state.currentStep);
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
    
    // Prompt input
    if (elements.promptInput) {
        elements.promptInput.addEventListener('input', debouncedAnalyze);
        elements.promptInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                elements.generateBtn.click();
            }
        });
    }
    
    // Generate button
    if (elements.generateBtn) {
        elements.generateBtn.addEventListener('click', handleGenerate);
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
    console.log('Initializing Prompt Engineering Platform...');
    console.log('Session ID:', state.sessionId);
    console.log('Module:', state.moduleId);
    console.log('Submodule:', state.submoduleId);
    
    initEventListeners();
    initResizePanel();
    startLesson();
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
