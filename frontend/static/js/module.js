const chatContainer = document.getElementById('chatContainer');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const documentPreview = document.getElementById('documentPreview');
const previewContent = document.getElementById('previewContent');
const promptSection = document.getElementById('promptSection');
const promptInput = document.getElementById('promptInput');
const generateButton = document.getElementById('generateButton');
const summaryOutput = document.getElementById('summaryOutput');
const summaryContent = document.getElementById('summaryContent');
const exampleBtns = document.querySelectorAll('.example-btn');

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user-message' : 'ai-message'}`;
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${isUser ? 'YOU' : 'AI'}</div>
        <div class="message-content">
            <p>${content}</p>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    chatInput.value = '';
    
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            message: message,
            context: 'Document upload and summarization module'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            addMessage(data.response);
        } else if (data.error) {
            addMessage(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        addMessage(`Error: ${error.message}`);
    });
}

sendButton.addEventListener('click', sendChatMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatMessage();
});

uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('drag-over');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    uploadZone.innerHTML = `
        <div class="upload-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
        </div>
        <p class="upload-text">Uploading...</p>
    `;
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadZone.innerHTML = `
                <div class="upload-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                        <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                </div>
                <p class="upload-text">✓ ${data.filename} uploaded successfully!</p>
                <p class="upload-hint">Document ready for summarization</p>
            `;
            
            documentPreview.style.display = 'block';
            previewContent.textContent = data.preview;
            
            promptSection.style.display = 'block';
            
            addMessage(`Great! I've received your document "${data.filename}". Now you can experiment with different prompts to generate summaries. Try the example prompts or create your own!`);
        } else {
            uploadZone.innerHTML = `
                <div class="upload-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                </div>
                <p class="upload-text">Upload failed: ${data.error}</p>
                <p class="upload-hint">Click to try again</p>
            `;
        }
    })
    .catch(error => {
        uploadZone.innerHTML = `
            <div class="upload-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="15" y1="9" x2="9" y2="15"/>
                    <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
            </div>
            <p class="upload-text">Error: ${error.message}</p>
            <p class="upload-hint">Click to try again</p>
        `;
    });
}

exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        promptInput.value = btn.dataset.prompt;
    });
});

generateButton.addEventListener('click', () => {
    const prompt = promptInput.value.trim();
    if (!prompt) {
        addMessage('Please enter a prompt first!');
        return;
    }
    
    generateButton.disabled = true;
    generateButton.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10"/>
        </svg>
        Generating...
    `;
    
    fetch('/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
            summaryOutput.style.display = 'block';
            summaryContent.innerHTML = data.summary.replace(/\n/g, '<br>');
            
            addMessage('I\'ve generated a summary based on your prompt. Notice how the structure and detail of the summary changed based on how you crafted your prompt. This is the power of prompt engineering!');
        } else if (data.error) {
            addMessage(`Error generating summary: ${data.error}`);
        }
    })
    .catch(error => {
        addMessage(`Error: ${error.message}`);
    })
    .finally(() => {
        generateButton.disabled = false;
        generateButton.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            Generate Summary
        `;
    });
});
