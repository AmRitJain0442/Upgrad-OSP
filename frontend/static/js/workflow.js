/**
 * Workflow Automation Module - Frontend JavaScript
 */

class WorkflowAutomation {
    constructor() {
        console.log('WorkflowAutomation constructor called');
        this.sessionId = this.generateSessionId();
        this.currentStep = 1;
        this.questions = [];
        this.answers = {};
        this.tools = [];
        this.roadmap = null;

        // Split screen state
        this.splitScreenActive = false;
        this.currentActiveStepIndex = null;
        this.dividerDragging = false;
        this.dividerStartX = 0;
        this.leftPanelStartWidth = 0;

        console.log('Initializing event listeners...');
        this.initializeEventListeners();
        console.log('Event listeners initialized');
    }

    generateSessionId() {
        return `workflow_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    initializeEventListeners() {
        // Task Discovery
        document.getElementById('discoverTaskBtn')?.addEventListener('click', () => this.discoverTask());
        document.getElementById('taskInput')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) this.discoverTask();
        });

        // Example tasks
        document.querySelectorAll('.example-task').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.getElementById('taskInput').value = e.target.dataset.task;
            });
        });

        // Submit answers
        document.getElementById('submitAnswersBtn')?.addEventListener('click', () => this.submitAnswers());

        // Generate roadmap
        document.getElementById('generateRoadmapBtn')?.addEventListener('click', () => this.generateRoadmap());

        // Export roadmap
        document.getElementById('exportRoadmapBtn')?.addEventListener('click', () => this.exportRoadmap());

        // Start over
        document.getElementById('startOverBtn')?.addEventListener('click', () => this.startOver());

        // Modal close
        document.querySelector('.close-modal')?.addEventListener('click', () => {
            document.getElementById('stepModal').style.display = 'none';
        });

        // Close modal on outside click
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('stepModal');
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        // Initialize split screen listeners
        this.initializeSplitScreenListeners();
    }

    initializeSplitScreenListeners() {
        // Close button
        document.getElementById('closeSplitBtn')?.addEventListener('click', () => {
            this.closeSplitView();
        });

        // ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.splitScreenActive) {
                this.closeSplitView();
            }
        });

        // Divider drag
        const divider = document.getElementById('splitDivider');
        if (divider) {
            divider.addEventListener('mousedown', (e) => this.startDividerDrag(e));
        }

        document.addEventListener('mousemove', (e) => this.onDividerDrag(e));
        document.addEventListener('mouseup', () => this.stopDividerDrag());
    }

    showLoader(buttonId) {
        const btn = document.getElementById(buttonId);
        if (btn) {
            btn.disabled = true;
            btn.querySelector('.btn-text').style.display = 'none';
            btn.querySelector('.btn-loader').style.display = 'inline-flex';
        }
    }

    hideLoader(buttonId) {
        const btn = document.getElementById(buttonId);
        if (btn) {
            btn.disabled = false;
            btn.querySelector('.btn-text').style.display = 'inline';
            btn.querySelector('.btn-loader').style.display = 'none';
        }
    }

    updateProgress(step) {
        this.currentStep = step;
        
        // Update progress bar
        document.querySelectorAll('.progress-step').forEach((stepEl, index) => {
            stepEl.classList.remove('active', 'completed');
            if (index + 1 < step) {
                stepEl.classList.add('completed');
            } else if (index + 1 === step) {
                stepEl.classList.add('active');
            }
        });

        // Show/hide sections
        document.querySelectorAll('.workflow-section').forEach(section => {
            section.classList.remove('active');
        });
        
        const sections = ['taskDiscoverySection', 'questionsSection', 'toolsSection', 'roadmapSection'];
        const activeSection = document.getElementById(sections[step - 1]);
        if (activeSection) {
            activeSection.classList.add('active');
        }
    }

    async discoverTask() {
        console.log('discoverTask called');
        const taskInput = document.getElementById('taskInput').value.trim();
        console.log('Task input:', taskInput);
        
        if (!taskInput) {
            alert('Please describe your task first');
            return;
        }

        this.showLoader('discoverTaskBtn');

        try {
            console.log('Sending request to /workflow/discover-task');
            const response = await fetch('/workflow/discover-task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_input: taskInput,
                    session_id: this.sessionId
                })
            });

            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`Failed to discover task: ${response.status}`);
            }

            const data = await response.json();
            console.log('Response data:', data);
            this.questions = data.questions;
            
            this.renderQuestions();
            this.updateProgress(2);

        } catch (error) {
            console.error('Error discovering task:', error);
            alert(`Failed to analyze your task: ${error.message}`);
        } finally {
            this.hideLoader('discoverTaskBtn');
        }
    }

    renderQuestions() {
        const container = document.getElementById('questionsContainer');
        container.innerHTML = '';

        this.questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question-item';
            
            // Build options HTML if available
            let optionsHtml = '';
            if (question.options && question.options.length > 0) {
                optionsHtml = `
                    <div class="question-options">
                        ${question.options.map((option, optIdx) => `
                            <button type="button" class="option-btn" data-question-index="${index}" data-option-value="${option}">
                                ${option}
                            </button>
                        `).join('')}
                    </div>
                `;
            }
            
            questionDiv.innerHTML = `
                <label>${question.question}</label>
                ${question.context ? `<p class="question-context">${question.context}</p>` : ''}
                ${optionsHtml}
                ${question.allow_custom !== false ? `
                    <textarea 
                        id="answer-${index}" 
                        rows="3" 
                        placeholder="${question.options && question.options.length > 0 ? 'Or type your own answer...' : 'Your answer...'}"
                        data-question="${question.question}"
                    ></textarea>
                ` : ''}
            `;
            container.appendChild(questionDiv);
        });

        // Add click handlers for option buttons
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const questionIndex = e.target.dataset.questionIndex;
                const optionValue = e.target.dataset.optionValue;
                
                // Deselect all buttons in this question
                const questionDiv = e.target.closest('.question-item');
                questionDiv.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
                
                // Select this button
                e.target.classList.add('selected');
                
                // Update textarea with selected value
                const textarea = document.getElementById(`answer-${questionIndex}`);
                if (textarea) {
                    textarea.value = optionValue;
                }
            });
        });

        // Show submit button
        document.getElementById('submitAnswersBtn').style.display = 'inline-flex';
    }

    async submitAnswers() {
        // Collect answers
        this.answers = {};
        const answerInputs = document.querySelectorAll('[id^="answer-"]');
        
        let allAnswered = true;
        answerInputs.forEach(input => {
            const answer = input.value.trim();
            if (!answer) {
                allAnswered = false;
            } else {
                this.answers[input.dataset.question] = answer;
            }
        });

        if (!allAnswered) {
            alert('Please answer all questions');
            return;
        }

        this.showLoader('submitAnswersBtn');

        try {
            // Submit answers
            await fetch(`/workflow/submit-answers?session_id=${this.sessionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.answers)
            });

            // Search for tools
            const response = await fetch(`/workflow/search-tools?session_id=${this.sessionId}`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to search tools');

            this.tools = await response.json();
            
            this.renderTools();
            this.updateProgress(3);

        } catch (error) {
            console.error('Error searching tools:', error);
            alert('Failed to find AI tools. Please try again.');
        } finally {
            this.hideLoader('submitAnswersBtn');
        }
    }

    renderTools() {
        const grid = document.getElementById('toolsGrid');
        grid.innerHTML = '';

        if (this.tools.length === 0) {
            grid.innerHTML = '<p>No tools found. Generating workflow anyway...</p>';
        } else {
            this.tools.forEach(tool => {
                const toolCard = document.createElement('div');
                toolCard.className = 'tool-card';
                toolCard.innerHTML = `
                    <div class="tool-header">
                        <div class="tool-name">${tool.tool_name}</div>
                        <div class="tool-pricing">${tool.pricing}</div>
                    </div>
                    <p class="tool-description">${tool.description}</p>
                    <div class="tool-use-case">
                        <strong>Use case:</strong> ${tool.use_case}
                    </div>
                    <a href="${tool.url}" target="_blank" class="tool-url">
                        Visit tool
                    </a>
                `;
                
                toolCard.addEventListener('click', () => {
                    window.open(tool.url, '_blank');
                });
                
                grid.appendChild(toolCard);
            });
        }

        // Show generate roadmap button
        document.getElementById('generateRoadmapBtn').style.display = 'inline-flex';
    }

    async generateRoadmap() {
        this.showLoader('generateRoadmapBtn');

        try {
            const response = await fetch(`/workflow/generate-roadmap?session_id=${this.sessionId}`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to generate roadmap');

            this.roadmap = await response.json();
            console.log('Full roadmap received:', this.roadmap);
            console.log('First step full data:', this.roadmap.steps[0]);
            
            this.renderRoadmap();
            this.updateProgress(4);

        } catch (error) {
            console.error('Error generating roadmap:', error);
            alert('Failed to generate workflow roadmap. Please try again.');
        } finally {
            this.hideLoader('generateRoadmapBtn');
        }
    }

    renderRoadmap() {
        if (!this.roadmap) return;

        // Update header
        document.getElementById('roadmapTitle').textContent = this.roadmap.task_title;
        document.getElementById('roadmapDifficulty').textContent = this.roadmap.difficulty_level;
        document.getElementById('roadmapTime').textContent = `Estimated: ${this.roadmap.total_estimated_time}`;

        // Render tree
        const treeContainer = document.getElementById('roadmapTree');
        treeContainer.innerHTML = '';

        this.roadmap.steps.forEach((step, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'tree-step';
            
            // Count alternatives for display
            const altCount = step.alternatives ? step.alternatives.length : 0;
            const altText = altCount > 0 ? `+${altCount} alternative${altCount > 1 ? 's' : ''}` : '';
            
            // Course recommendation if available
            console.log(`Step ${index + 1} course data:`, step.related_course);
            const courseHtml = step.related_course ? `
                <div class="step-course-card">
                    <div class="course-icon">→</div>
                    <div class="course-info">
                        <div class="course-label">RECOMMENDED COURSE</div>
                        <div class="course-title">${step.related_course.title}</div>
                        <div class="course-desc">${step.related_course.description}</div>
                    </div>
                    <a href="${step.related_course.url}" class="course-btn">LEARN →</a>
                </div>
            ` : '';
            
            stepDiv.innerHTML = `
                <div class="step-node" data-step-index="${index}">
                    <div class="step-number">${index + 1}</div>
                    <div class="step-header">
                        <div class="step-title">${step.title}</div>
                        <div class="step-time">${step.estimated_time}</div>
                    </div>
                    <p class="step-description">${step.description}</p>
                    <div class="step-tool">
                        <strong>${step.ai_tool}</strong>
                        ${altCount > 0 ? `<span class="alt-badge">${altText}</span>` : ''}
                    </div>
                    ${courseHtml}
                    <div class="step-actions">
                        <a href="${step.evaluator_link || '/evaluator/'}" class="step-action-btn evaluator-btn" target="_blank">
                            TEST YOUR PROMPT
                        </a>
                    </div>
                    <div class="step-expand">
                        Click to view prompts, tips, quiz & more →
                    </div>
                </div>
            `;

            // Prevent action buttons from triggering modal
            stepDiv.querySelectorAll('.step-action-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                });
            });

            stepDiv.querySelector('.step-node').addEventListener('click', (e) => {
                e.preventDefault();
                this.showStepDetails(step);
            });

            treeContainer.appendChild(stepDiv);
        });
    }

    showStepDetails(step) {
        const container = document.getElementById('splitScreenContainer');
        const detailsContainer = document.getElementById('stepDetails');
        const rightPanel = document.getElementById('rightPanel');

        // Activate split screen
        container.classList.add('split-active');
        this.splitScreenActive = true;

        // Restore saved split ratio
        const savedRatio = localStorage.getItem('workflowSplitRatio');
        if (savedRatio) {
            const leftPanel = document.getElementById('leftPanel');
            const leftPercentage = parseFloat(savedRatio);
            leftPanel.style.width = `${leftPercentage}%`;
            rightPanel.style.width = `${100 - leftPercentage}%`;
        }

        // Mark active node
        this.updateActiveNode(step);

        // Render content
        detailsContainer.innerHTML = `
            <h2>${step.title}</h2>
            <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.05rem; line-height: 1.7;">${step.description}</p>

            <div class="detail-section primary-tool-section">
                <h3>Primary Tool</h3>
                <div class="primary-tool-card">
                    <div class="tool-name-large">${step.ai_tool}</div>
                    ${step.tool_url ? `<a href="${step.tool_url}" target="_blank" class="tool-link-primary">Visit tool →</a>` : ''}
                </div>
            </div>

            ${step.related_course ? `
            <div class="detail-section course-detail-section">
                <h3>Recommended Course</h3>
                <div class="course-detail-card">
                    <div class="course-detail-header">
                        <div class="course-detail-title">${step.related_course.title}</div>
                        <a href="${step.related_course.url}" class="course-detail-btn">START COURSE →</a>
                    </div>
                    <p class="course-detail-desc">${step.related_course.description}</p>
                </div>
            </div>
            ` : ''}

            ${step.alternatives && step.alternatives.length > 0 ? `
            <div class="detail-section alternatives-section">
                <h3>Alternative Tools (${step.alternatives.length})</h3>
                <div class="alternatives-grid-enhanced">
                    ${step.alternatives.map(alt => `
                        <div class="alternative-card">
                            <div class="alt-header">
                                <span class="alt-tool-name">${alt.tool}</span>
                                ${alt.pricing ? `<span class="alt-pricing">${alt.pricing}</span>` : ''}
                            </div>
                            <p class="alt-reason">${alt.reason}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}

            ${step.prompts && step.prompts.length > 0 ? `
            <div class="detail-section prompts-section">
                <h3>Ready-to-Use Prompts</h3>
                <div class="prompts-container">
                    ${step.prompts.map((prompt, idx) => `
                        <div class="prompt-card" data-prompt-index="${idx}">
                            <div class="prompt-number">${idx + 1}</div>
                            <div class="prompt-text">${prompt.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
                            <div class="copy-hint">Click to copy</div>
                        </div>
                    `).join('')}
                </div>
                ${step.evaluator_link ? `
                <div class="evaluator-cta">
                    <div class="evaluator-icon">→</div>
                    <div class="evaluator-text">
                        <div class="evaluator-title">TEST YOUR PROMPT</div>
                        <div class="evaluator-subtitle">Use our AI Evaluator to analyze and improve your prompts</div>
                    </div>
                    <a href="${step.evaluator_link}" class="evaluator-btn">EVALUATE →</a>
                </div>
                ` : ''}
            </div>
            ` : ''}

            ${step.tips && step.tips.length > 0 ? `
            <div class="detail-section tips-section">
                <h3>Pro Tips</h3>
                <ul class="detail-list tips-list">
                    ${step.tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>
            ` : ''}

            <div class="pros-cons-grid">
                ${step.pros && step.pros.length > 0 ? `
                <div class="detail-section">
                    <h3>Pros</h3>
                    <ul class="detail-list pros-list">
                        ${step.pros.map(pro => `<li>${pro}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}

                ${step.cons && step.cons.length > 0 ? `
                <div class="detail-section">
                    <h3>Cons</h3>
                    <ul class="detail-list cons-list">
                        ${step.cons.map(con => `<li>${con}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            </div>

            ${step.quiz ? `
            <div class="detail-section quiz-section">
                <h3>Knowledge Check</h3>
                <div class="quiz-container">
                    <div class="quiz-question">${step.quiz.question}</div>
                    <div class="quiz-options">
                        ${step.quiz.options.map((option, idx) => `
                            <button class="quiz-option" data-option-index="${idx}">
                                <span class="option-letter">${String.fromCharCode(65 + idx)}</span>
                                <span class="option-text">${option}</span>
                            </button>
                        `).join('')}
                    </div>
                    <div class="quiz-feedback" style="display: none;"></div>
                </div>
            </div>
            ` : ''}
        `;

        // Scroll to top
        rightPanel.scrollTop = 0;

        // Initialize interactive features
        this.initializePromptCopy(detailsContainer);
        if (step.quiz) {
            this.initializeQuiz(detailsContainer, step);
        }
    }

    closeSplitView() {
        const container = document.getElementById('splitScreenContainer');
        container.classList.remove('split-active');
        this.splitScreenActive = false;
        this.currentActiveStepIndex = null;

        // Remove active highlight
        document.querySelectorAll('.step-node').forEach(node => {
            node.classList.remove('active');
        });
    }

    updateActiveNode(step) {
        // Remove all active classes
        document.querySelectorAll('.step-node').forEach(node => {
            node.classList.remove('active');
        });

        // Add active to clicked node
        const stepIndex = this.roadmap.steps.indexOf(step);
        const stepNode = document.querySelector(`.step-node[data-step-index="${stepIndex}"]`);
        if (stepNode) {
            stepNode.classList.add('active');
            this.currentActiveStepIndex = stepIndex;
            stepNode.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    startDividerDrag(e) {
        e.preventDefault();
        this.dividerDragging = true;
        this.dividerStartX = e.clientX;

        const leftPanel = document.getElementById('leftPanel');
        this.leftPanelStartWidth = leftPanel.offsetWidth;

        document.getElementById('splitDivider').classList.add('dragging');
        document.body.style.userSelect = 'none';
        document.body.style.cursor = 'col-resize';
    }

    onDividerDrag(e) {
        if (!this.dividerDragging) return;

        e.preventDefault();

        const container = document.getElementById('splitScreenContainer');
        const leftPanel = document.getElementById('leftPanel');
        const rightPanel = document.getElementById('rightPanel');

        const deltaX = e.clientX - this.dividerStartX;
        const containerWidth = container.offsetWidth;

        let newLeftWidth = this.leftPanelStartWidth + deltaX;

        // Enforce 30%-70% limits
        const minWidth = containerWidth * 0.3;
        const maxWidth = containerWidth * 0.7;
        newLeftWidth = Math.max(minWidth, Math.min(maxWidth, newLeftWidth));

        const leftPercentage = (newLeftWidth / containerWidth) * 100;
        const rightPercentage = 100 - leftPercentage;

        leftPanel.style.width = `${leftPercentage}%`;
        rightPanel.style.width = `${rightPercentage}%`;
    }

    stopDividerDrag() {
        if (!this.dividerDragging) return;

        this.dividerDragging = false;

        document.getElementById('splitDivider').classList.remove('dragging');
        document.body.style.userSelect = '';
        document.body.style.cursor = '';

        // Save ratio to localStorage
        const leftPanel = document.getElementById('leftPanel');
        const container = document.getElementById('splitScreenContainer');
        const ratio = (leftPanel.offsetWidth / container.offsetWidth) * 100;
        localStorage.setItem('workflowSplitRatio', ratio);
    }

    initializePromptCopy(container) {
        const promptCards = container.querySelectorAll('.prompt-card');
        promptCards.forEach(card => {
            card.addEventListener('click', function() {
                const promptText = this.querySelector('.prompt-text').textContent;
                navigator.clipboard.writeText(promptText).then(() => {
                    const copyHint = this.querySelector('.copy-hint');
                    copyHint.textContent = 'Copied!';
                    copyHint.style.color = '#10b981';
                    setTimeout(() => {
                        copyHint.textContent = 'Click to copy';
                        copyHint.style.color = '';
                    }, 2000);
                });
            });
        });
    }

    initializeQuiz(container, step) {
        const quizOptions = container.querySelectorAll('.quiz-option');
        const feedbackDiv = container.querySelector('.quiz-feedback');

        quizOptions.forEach((btn, idx) => {
            btn.addEventListener('click', () => {
                quizOptions.forEach(opt => opt.disabled = true);

                const isCorrect = idx === step.quiz.correct_index;

                if (isCorrect) {
                    btn.classList.add('correct');
                    feedbackDiv.innerHTML = `
                        <div class="feedback-correct">
                            <div>
                                <strong>Correct!</strong>
                                <p>${step.quiz.explanation}</p>
                            </div>
                        </div>
                    `;
                } else {
                    btn.classList.add('incorrect');
                    quizOptions[step.quiz.correct_index].classList.add('correct');
                    feedbackDiv.innerHTML = `
                        <div class="feedback-incorrect">
                            <div>
                                <strong>Not quite right.</strong>
                                <p>${step.quiz.explanation}</p>
                            </div>
                        </div>
                    `;
                }

                feedbackDiv.style.display = 'block';
            });
        });
    }

    exportRoadmap() {
        if (!this.roadmap) return;

        const exportData = {
            title: this.roadmap.task_title,
            description: this.roadmap.task_description,
            difficulty: this.roadmap.difficulty_level,
            total_time: this.roadmap.total_estimated_time,
            steps: this.roadmap.steps.map((step, index) => ({
                step_number: index + 1,
                title: step.title,
                description: step.description,
                ai_tool: step.ai_tool,
                tool_url: step.tool_url,
                estimated_time: step.estimated_time,
                prompts: step.prompts,
                tips: step.tips,
                pros: step.pros,
                cons: step.cons,
                alternatives: step.alternatives
            }))
        };

        // Create downloadable JSON
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `workflow-roadmap-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    async startOver() {
        if (!confirm('Are you sure you want to start over? This will clear your current workflow.')) {
            return;
        }

        try {
            // Clear session on backend
            await fetch(`/workflow/session/${this.sessionId}`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.error('Error clearing session:', error);
        }

        // Reset state
        this.sessionId = this.generateSessionId();
        this.questions = [];
        this.answers = {};
        this.tools = [];
        this.roadmap = null;

        // Clear inputs
        document.getElementById('taskInput').value = '';
        document.getElementById('questionsContainer').innerHTML = '';
        document.getElementById('toolsGrid').innerHTML = '';
        document.getElementById('roadmapTree').innerHTML = '';

        // Go back to step 1
        this.updateProgress(1);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing WorkflowAutomation...');
    window.workflowAutomation = new WorkflowAutomation();
    console.log('WorkflowAutomation initialized successfully');
});
