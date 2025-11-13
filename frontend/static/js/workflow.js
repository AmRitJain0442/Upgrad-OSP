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
            questionDiv.innerHTML = `
                <label>${question.question}</label>
                ${question.context ? `<p class="question-context">${question.context}</p>` : ''}
                <textarea 
                    id="answer-${index}" 
                    rows="3" 
                    placeholder="Your answer..."
                    data-question="${question.question}"
                ></textarea>
            `;
            container.appendChild(questionDiv);
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
            stepDiv.innerHTML = `
                <div class="step-node" data-step-index="${index}">
                    <div class="step-number">${index + 1}</div>
                    <div class="step-header">
                        <div class="step-title">${step.title}</div>
                        <div class="step-time">${step.estimated_time}</div>
                    </div>
                    <p class="step-description">${step.description}</p>
                    <div class="step-tool">
                        AI Tool: ${step.ai_tool}
                    </div>
                    <div class="step-expand">
                        Click to view prompts, tips, pros & cons
                    </div>
                </div>
            `;

            stepDiv.querySelector('.step-node').addEventListener('click', () => {
                this.showStepDetails(step);
            });

            treeContainer.appendChild(stepDiv);
        });
    }

    showStepDetails(step) {
        const modal = document.getElementById('stepModal');
        const detailsContainer = document.getElementById('stepDetails');

        detailsContainer.innerHTML = `
            <h2>${step.title}</h2>
            <p style="color: #64748b; margin-bottom: 2rem;">${step.description}</p>

            <div class="detail-section">
                <h3>AI Tool</h3>
                <div style="padding: 1rem; background: #f8fafc; border-radius: 8px;">
                    <strong>${step.ai_tool}</strong>
                    ${step.tool_url ? `<br><a href="${step.tool_url}" target="_blank" style="color: #ef4444;">Visit tool</a>` : ''}
                </div>
            </div>

            <div class="detail-section">
                <h3>Prompts to Use</h3>
                <ul class="detail-list">
                    ${step.prompts.map(prompt => `<li>${prompt}</li>`).join('')}
                </ul>
            </div>

            <div class="detail-section">
                <h3>Tips</h3>
                <ul class="detail-list">
                    ${step.tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>

            <div class="detail-section">
                <h3>Pros</h3>
                <ul class="detail-list pros-list">
                    ${step.pros.map(pro => `<li>${pro}</li>`).join('')}
                </ul>
            </div>

            <div class="detail-section">
                <h3>Cons</h3>
                <ul class="detail-list cons-list">
                    ${step.cons.map(con => `<li>${con}</li>`).join('')}
                </ul>
            </div>

            ${step.alternatives && step.alternatives.length > 0 ? `
                <div class="detail-section">
                    <h3>Alternative Tools</h3>
                    <div class="alternatives-grid">
                        ${step.alternatives.map(alt => `
                            <div class="alternative-item">
                                <div class="alternative-name">${alt.tool}</div>
                                <div>${alt.reason}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        `;

        modal.style.display = 'block';
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
