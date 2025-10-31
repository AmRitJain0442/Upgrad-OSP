// Sample document content
const SAMPLE_DOCUMENT = `The Rise of Remote Work

The COVID-19 pandemic fundamentally transformed how millions of people work. Before 2020, remote work was a perk offered by progressive companies. Today, it has become a standard expectation for many professionals.

Key Benefits of Remote Work:
- Flexibility in schedule and location
- Reduced commuting time and costs
- Better work-life balance
- Access to global talent pools for employers
- Increased productivity for many workers

Challenges Faced:
- Communication barriers in distributed teams
- Difficulty maintaining company culture
- Technology and cybersecurity concerns
- Blurred boundaries between work and personal life
- Feelings of isolation for some employees

Studies show that 70% of workers want to continue working remotely at least part-time. Companies are adapting by adopting hybrid models that combine office and remote work. The future of work is likely to be more flexible than ever before.`;

// State management
let currentStep = 'welcome';
let documentUploaded = false;
let promptAttempts = 0;
let lessonComplete = false;

// DOM elements
const tutorChat = document.getElementById('tutorChat');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const uploadDocBtn = document.getElementById('uploadDocBtn');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('uploadSection');
const workspaceChat = document.getElementById('workspaceChat');
const promptInputSection = document.getElementById('promptInputSection');
const promptInput = document.getElementById('promptInput');
const generateBtn = document.getElementById('generateBtn');

// Utility functions
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
                            <div class="quiz-option" data-correct="${idx === quizData.correctIndex}" data-index="${idx}">
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
                    if (this.dataset.correct === 'true') {
                        this.classList.add('correct');
                        setTimeout(() => {
                            addTutorMessage("Exactly right! You've mastered the concept of constraints in prompting. Great work on this lesson!");
                            lessonComplete = true;
                            highlightElement(document.querySelector('.tab[data-submodule="2"]'));
                            addTutorMessage("Click on 'Submodule 2' when you're ready for your next challenge!");
                            document.querySelector('.tab[data-submodule="2"]').classList.remove('locked');
                        }, 1500);
                    } else {
                        this.classList.add('incorrect');
                        const correct = messageDiv.querySelector('.quiz-option[data-correct="true"]');
                        setTimeout(() => correct.classList.add('correct'), 500);
                    }
                    options.forEach(o => o.style.pointerEvents = 'none');
                });
            });
        }, 100);
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content">
                <p>${content}</p>
            </div>
        `;
    }
    
    tutorChat.appendChild(messageDiv);
    tutorChat.scrollTop = tutorChat.scrollHeight;
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
    tutorChat.appendChild(messageDiv);
    tutorChat.scrollTop = tutorChat.scrollHeight;
}

function addProactiveTip(tip) {
    const tipDiv = document.createElement('div');
    tipDiv.className = 'chat-message ai-message';
    tipDiv.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content">
            <div class="proactive-tip">
                <div class="tip-header">
                    Proactive Suggestion
                </div>
                <p>${tip}</p>
            </div>
        </div>
    `;
    tutorChat.appendChild(tipDiv);
    tutorChat.scrollTop = tutorChat.scrollHeight;
}

function parseMarkdown(text) {
    // Convert markdown to HTML with proper formatting
    let html = text;
    
    // Handle bold text **text**
    html = html.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Handle headings ### Heading
    html = html.replace(/^### (.+)$/gm, '<h3 class="response-heading">$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2 class="response-heading">$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1 class="response-heading">$1</h1>');
    
    // Handle line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    
    // Handle numbered lists
    html = html.replace(/^(\d+)\.\s+(.+)$/gm, '<div class="list-item"><span class="list-number">$1.</span> $2</div>');
    
    // Handle bullet points
    html = html.replace(/^[-*]\s+(.+)$/gm, '<div class="list-item"><span class="bullet">•</span> $1</div>');
    
    // Handle code blocks
    html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    // Wrap in paragraph if not already wrapped
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }
    
    return html;
}

function addWorkspaceMessage(content, isUser = false, skipParsing = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `workspace-message ${isUser ? 'user' : 'ai'}`;
    
    // Parse markdown for AI messages (unless skipParsing is true)
    let formattedContent = content;
    if (!isUser && !skipParsing) {
        formattedContent = parseMarkdown(content);
    }
    
    messageDiv.innerHTML = `
        <span class="message-label">${isUser ? 'You' : 'Workspace AI'}</span>
        <div class="workspace-bubble">${formattedContent}</div>
    `;
    workspaceChat.appendChild(messageDiv);
    workspaceChat.scrollTop = workspaceChat.scrollHeight;
}

function highlightElement(element) {
    document.querySelectorAll('.highlight-glow').forEach(el => {
        el.classList.remove('highlight-glow');
    });
    
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

// Lesson flow
function startLesson() {
    addTutorMessage("Welcome to your first lesson! We're going to learn how to get an AI to write a summary without it making up facts.");
    setTimeout(() => {
        addTutorMessage("First, please click the 'Upload Document' button on your right.");
        highlightElement(uploadDocBtn);
        currentStep = 'upload';
    }, 1500);
}

function handleDocumentUpload(file) {
    if (!file) return;
    
    unhighlightAll();
    
    // Show uploading state
    uploadDocBtn.disabled = true;
    uploadDocBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10" opacity="0.25"/>
            <path d="M12 2a10 10 0 0 1 10 10" opacity="0.75">
                <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>
        Uploading...
    `;
    
    // Create FormData and upload
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Hide upload section, show workspace
            uploadSection.style.display = 'none';
            workspaceChat.style.display = 'flex';
            promptInputSection.style.display = 'flex';
            
            documentUploaded = true;
            
            // Show document preview in workspace
            // Clean up preview text - remove excessive whitespace
            const cleanPreview = data.preview.replace(/\s+/g, ' ').trim();
            addWorkspaceMessage(`Document loaded: <strong>${data.filename}</strong><br><br>${cleanPreview}`, false, true);
            
            addTutorMessage(`Great! The document "${data.filename}" is loaded. Now, your goal is to summarize it. Try typing a prompt in the text box below the workspace.`);
            
            setTimeout(() => {
                highlightElement(promptInput);
                currentStep = 'prompt';
            }, 1500);
        } else {
            // Show error
            uploadDocBtn.disabled = false;
            uploadDocBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <path d="M14 2v6h6M12 18v-6M9 15l3-3 3 3"/>
                </svg>
                Upload Document
            `;
            addTutorMessage(`Oops! There was an error uploading your file: ${data.error}. Please try again with a PDF, DOCX, or TXT file.`);
        }
    })
    .catch(error => {
        uploadDocBtn.disabled = false;
        uploadDocBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <path d="M14 2v6h6M12 18v-6M9 15l3-3 3 3"/>
            </svg>
            Upload Document
        `;
        addTutorMessage(`Sorry, there was a connection error: ${error.message}. Please make sure the server is running and try again.`);
    });
}

function handlePromptTyping() {
    const text = promptInput.value.trim().toLowerCase();
    
    if (text.length > 10 && !text.includes('based on') && !text.includes('only') && !text.includes('external') && promptAttempts === 0) {
        promptAttempts++;
        unhighlightAll();
        addProactiveTip("Remember, we want to constrain the AI. A simple 'summarize' prompt might cause it to add external info. Try adding a rule, like '<strong>Based only on the text provided</strong>' or '<strong>Do not use any external knowledge</strong>'.");
    }
}

async function handleGenerate() {
    const prompt = promptInput.value.trim();
    if (!prompt) {
        addTutorMessage("Please type a prompt first!");
        return;
    }
    
    unhighlightAll();
    addWorkspaceMessage(prompt, true);
    
    const hasConstraints = prompt.toLowerCase().includes('based on') || 
                          prompt.toLowerCase().includes('only') || 
                          prompt.toLowerCase().includes('external') ||
                          prompt.toLowerCase().includes('provided');
    
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="3"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/></circle></svg>';
    
    // Actually call the API to summarize
    fetch('/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
            addWorkspaceMessage(data.summary, false);
            
            if (hasConstraints) {
                setTimeout(() => {
                    addTutorMessage("Fantastic! See the difference? Your prompt gave the AI clear rules and constraints. That's the core skill of prompting! You've successfully completed this task.");
                    
                    setTimeout(() => {
                        const quizData = {
                            question: "Why did we add that constraint to our prompt?",
                            options: [
                                "To make the AI work faster",
                                "To prevent 'hallucination' (making up facts)",
                                "To make the summary longer",
                                "To make the AI sound smarter"
                            ],
                            correctIndex: 1
                        };
                        addTutorMessage("Time for a quick quiz!", true, quizData);
                    }, 2000);
                }, 1000);
            } else {
                setTimeout(() => {
                    addTutorMessage("Good start! Notice the summary. To make it even better and prevent any potential 'hallucination' (adding external facts), try adding a constraint like '<strong>Based only on the text provided</strong>' to your prompt.");
                    setTimeout(() => {
                        highlightElement(promptInput);
                    }, 1500);
                }, 1500);
            }
        } else if (data.error) {
            addWorkspaceMessage(`Error: ${data.error}`, false);
            addTutorMessage("There was an error generating the summary. Make sure you have uploaded a document and the Gemini API is configured properly.");
        }
    })
    .catch(error => {
        addWorkspaceMessage(`Connection error: ${error.message}`, false);
        addTutorMessage("Sorry, I couldn't connect to the AI service. Please make sure the server is running and the Gemini API key is configured.");
    })
    .finally(() => {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>';
        promptInput.value = '';
    });
}

// Event listeners
uploadDocBtn.addEventListener('click', () => {
    if (currentStep === 'upload') {
        fileInput.click();
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) {
        handleDocumentUpload(e.target.files[0]);
    }
});

promptInput.addEventListener('input', () => {
    if (currentStep === 'prompt' && documentUploaded) {
        handlePromptTyping();
    }
});

generateBtn.addEventListener('click', handleGenerate);

sendButton.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (message) {
        addUserMessage(message);
        chatInput.value = '';
        
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: message,
                context: 'Focused Summarization lesson'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addTutorMessage(data.response);
            }
        })
        .catch(error => {
            addTutorMessage("Sorry, I'm having trouble connecting. Please try again.");
        });
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

promptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        generateBtn.click();
    }
});

// Tab navigation
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
        if (!this.classList.contains('locked')) {
            alert('Submodule ' + this.dataset.submodule + ' is under development!');
        }
    });
});

// Initialize
startLesson();
