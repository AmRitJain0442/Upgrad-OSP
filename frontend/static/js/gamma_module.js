/**
 * Gamma AI Presentation Tool - Learning Module
 * Teaches users how to use Gamma's interface and features
 * Enhanced with dynamic teaching and real workflow simulation
 */

// Gamma module state management
class GammaModule {
    constructor() {
        this.state = {
            mode: 'create', // create, edit, present
            currentSlide: 0,
            slides: [],
            theme: 'professional',
            aiGenerating: false,
            tutorialActive: true,
            tutorialStep: 0,
            userProgress: {
                createdPresentation: false,
                editedSlide: false,
                changedTheme: false,
                addedElement: false,
                usedAiAssist: false,
                presented: false
            },
            interactionCount: 0,
            currentTool: null
        };
        
        this.elements = {};
        this.tutorialSteps = this.initializeTutorialSteps();
        this.tips = this.initializeTips();
        this.init();
    }
    
    initializeTutorialSteps() {
        return [
            {
                id: 'welcome',
                message: "👋 Welcome to Gamma! Let's create your first AI-powered presentation. Click on any creation option to start!",
                target: '.create-options',
                highlight: true,
                action: 'select-option'
            },
            {
                id: 'describe-topic',
                message: "📝 Great! Now describe what you want to create. Be specific - mention your topic, audience, and key points!",
                target: '#gammaTopicInput',
                highlight: true,
                action: 'type-topic'
            },
            {
                id: 'choose-style',
                message: "🎨 Choose how detailed you want your presentation. Each style creates different content!",
                target: '.ai-options',
                highlight: true,
                action: 'select-ai-option'
            },
            {
                id: 'generate',
                message: "✨ Perfect! Now click 'Generate with AI' and watch the magic happen!",
                target: '#gammaGenerateBtn',
                highlight: true,
                action: 'generate'
            },
            {
                id: 'explore-slides',
                message: "🎉 Amazing! Your presentation is ready. See the slides in the left panel? Click on any slide to view it!",
                target: '.gamma-sidebar',
                highlight: true,
                action: 'click-slide'
            },
            {
                id: 'edit-content',
                message: "✏️ Click directly on any text in the slide to edit it. Yes, it's that easy!",
                target: '#gammaCanvas',
                highlight: true,
                action: 'edit-text'
            },
            {
                id: 'try-themes',
                message: "🎨 Want to change the look? Try different themes from the right panel!",
                target: '#gammaThemeSelector',
                highlight: true,
                action: 'change-theme'
            },
            {
                id: 'add-element',
                message: "➕ Add images, videos, charts, and more! Click any element button to try it.",
                target: '.add-element-grid',
                highlight: true,
                action: 'add-element'
            },
            {
                id: 'ai-assist',
                message: "🤖 Need help? Click 'AI Assist' anytime to improve your content with AI!",
                target: '#gammaAiAssist',
                highlight: true,
                action: 'use-ai-assist'
            },
            {
                id: 'present',
                message: "🎬 Ready to present? Click 'Present' mode to see your work in full-screen!",
                target: '.gamma-mode-btn[data-mode="present"]',
                highlight: true,
                action: 'switch-present'
            }
        ];
    }
    
    initializeTips() {
        return {
            creation: [
                "💡 Tip: Paste in an outline or document to generate slides from existing content",
                "🎯 Pro Tip: Mention your target audience for better-tailored content",
                "✨ Did you know? You can generate presentations in 40+ languages!"
            ],
            editing: [
                "⌨️ Keyboard shortcut: Ctrl+Z to undo, Ctrl+Y to redo",
                "🎨 Pro Tip: Themes automatically adjust colors across all slides",
                "✨ Click and drag slide thumbnails to reorder them",
                "💡 Double-click images to replace them"
            ],
            aiFeatures: [
                "🤖 AI Assist can: rewrite, expand, simplify, or translate content",
                "🖼️ Generate custom images by describing what you want",
                "📊 Ask AI to create charts from your data",
                "✨ Use 'Make it more engaging' for better copy"
            ],
            presenting: [
                "🎤 Presenter mode shows notes only visible to you",
                "⏱️ Use the built-in timer to track your presentation",
                "📱 Control your presentation from your phone",
                "🔗 Share a live link that updates automatically"
            ]
        };
    }

    init() {
        this.cacheElements();
        this.setupEventListeners();
        this.setupPresentControls();
        this.loadSamplePresentation();
        this.startDynamicTutorial();
        this.showContextualTips();
        this.trackUserInteractions();
    }
    
    startDynamicTutorial() {
        // Show welcome tutorial after brief delay
        setTimeout(() => {
            this.showTutorialStep(0);
        }, 1500);
    }
    
    showTutorialStep(stepIndex) {
        if (!this.state.tutorialActive || stepIndex >= this.tutorialSteps.length) return;
        
        const step = this.tutorialSteps[stepIndex];
        this.state.tutorialStep = stepIndex;
        
        // Create floating tutorial tooltip
        const existingTooltip = document.querySelector('.gamma-tutorial-tooltip');
        if (existingTooltip) existingTooltip.remove();
        
        const tooltip = document.createElement('div');
        tooltip.className = 'gamma-tutorial-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-header">
                <span class="tooltip-title">Learning Gamma (${stepIndex + 1}/${this.tutorialSteps.length})</span>
                <button class="tooltip-close" onclick="window.gammaModule.dismissTutorial()">✕</button>
            </div>
            <div class="tooltip-content">
                <p>${step.message}</p>
            </div>
            <div class="tooltip-footer">
                <button class="tooltip-btn skip" onclick="window.gammaModule.skipTutorial()">Skip Tutorial</button>
                <button class="tooltip-btn next" onclick="window.gammaModule.nextTutorialStep()">Got it!</button>
            </div>
        `;
        
        document.body.appendChild(tooltip);
        
        // Position near target
        if (step.target) {
            this.positionTooltip(tooltip, step.target);
            if (step.highlight) {
                this.highlightElement(step.target);
            }
        }
        
        // Animate in
        setTimeout(() => tooltip.classList.add('show'), 100);
    }
    
    positionTooltip(tooltip, targetSelector) {
        const target = document.querySelector(targetSelector);
        if (!target) return;
        
        const rect = target.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        
        let top = rect.bottom + 10;
        let left = rect.left;
        
        // Keep tooltip on screen
        if (left + tooltipRect.width > window.innerWidth) {
            left = window.innerWidth - tooltipRect.width - 20;
        }
        
        if (top + tooltipRect.height > window.innerHeight) {
            top = rect.top - tooltipRect.height - 10;
        }
        
        tooltip.style.top = `${top}px`;
        tooltip.style.left = `${left}px`;
    }
    
    highlightElement(selector) {
        // Remove existing highlights
        document.querySelectorAll('.gamma-highlight').forEach(el => {
            el.classList.remove('gamma-highlight');
        });
        
        // Add new highlight
        const element = document.querySelector(selector);
        if (element) {
            element.classList.add('gamma-highlight');
        }
    }
    
    nextTutorialStep() {
        const currentStep = this.tutorialSteps[this.state.tutorialStep];
        
        // Check if user completed the action
        if (this.checkStepCompletion(currentStep)) {
            this.showTutorialStep(this.state.tutorialStep + 1);
        } else {
            // Show encouraging message
            this.showNotification(`Try ${currentStep.action.replace('-', ' ')}! 🎯`, 'info', 2000);
        }
    }
    
    checkStepCompletion(step) {
        // For now, allow manual progression
        // In real implementation, track actual user actions
        return true;
    }
    
    skipTutorial() {
        this.state.tutorialActive = false;
        this.dismissTutorial();
        this.showNotification('Tutorial skipped. Click ? button anytime for help!', 'info', 3000);
    }
    
    dismissTutorial() {
        const tooltip = document.querySelector('.gamma-tutorial-tooltip');
        if (tooltip) {
            tooltip.classList.remove('show');
            setTimeout(() => tooltip.remove(), 300);
        }
        
        document.querySelectorAll('.gamma-highlight').forEach(el => {
            el.classList.remove('gamma-highlight');
        });
    }
    
    showContextualTips() {
        // Show tips based on current mode
        setInterval(() => {
            if (!this.state.tutorialActive && Math.random() > 0.7) {
                let tipCategory = 'editing';
                if (this.state.mode === 'create') tipCategory = 'creation';
                else if (this.state.mode === 'present') tipCategory = 'presenting';
                
                const tips = this.tips[tipCategory];
                const randomTip = tips[Math.floor(Math.random() * tips.length)];
                
                this.showFloatingTip(randomTip);
            }
        }, 30000); // Every 30 seconds
    }
    
    showFloatingTip(message) {
        const tip = document.createElement('div');
        tip.className = 'gamma-floating-tip';
        tip.innerHTML = `
            <span class="tip-icon">💡</span>
            <span class="tip-text">${message}</span>
        `;
        
        document.body.appendChild(tip);
        
        setTimeout(() => tip.classList.add('show'), 100);
        setTimeout(() => {
            tip.classList.remove('show');
            setTimeout(() => tip.remove(), 300);
        }, 5000);
    }
    
    trackUserInteractions() {
        // Track interactions for adaptive learning
        document.addEventListener('click', (e) => {
            this.state.interactionCount++;
            
            // Provide contextual help based on interactions
            if (e.target.closest('.editable')) {
                if (!this.state.userProgress.editedSlide) {
                    this.state.userProgress.editedSlide = true;
                    this.showNotification('Great! You can edit any text directly like this! ✏️', 'success', 3000);
                }
            }
            
            if (e.target.closest('.add-element-btn')) {
                if (!this.state.userProgress.addedElement) {
                    this.state.userProgress.addedElement = true;
                    this.showFloatingTip('✨ Elements can be resized and repositioned by dragging!');
                }
            }
        });
    }

    cacheElements() {
        // Main sections
        this.elements.modeButtons = document.querySelectorAll('.gamma-mode-btn');
        this.elements.createPanel = document.getElementById('gammaCreate');
        this.elements.editPanel = document.getElementById('gammaEdit');
        this.elements.presentPanel = document.getElementById('gammaPresent');
        
        // Create mode elements
        this.elements.createOptions = document.querySelectorAll('.create-option-card');
        this.elements.topicInput = document.getElementById('gammaTopicInput');
        this.elements.generateBtn = document.getElementById('gammaGenerateBtn');
        this.elements.aiOptions = document.querySelectorAll('.ai-option');
        
        // Edit mode elements
        this.elements.slideList = document.getElementById('gammaSlideList');
        this.elements.canvas = document.getElementById('gammaCanvas');
        this.elements.themeSelector = document.getElementById('gammaThemeSelector');
        this.elements.layoutOptions = document.querySelectorAll('.layout-option');
        
        // Toolbar elements
        this.elements.textTools = document.querySelectorAll('.text-tool');
        this.elements.addElements = document.querySelectorAll('.add-element-btn');
        this.elements.aiAssist = document.getElementById('gammaAiAssist');
    }

    setupEventListeners() {
        // Mode switching
        this.elements.modeButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchMode(e.target.dataset.mode));
        });

        // Create mode
        this.elements.createOptions.forEach(card => {
            card.addEventListener('click', (e) => this.selectCreateOption(e.currentTarget.dataset.option));
        });

        if (this.elements.generateBtn) {
            this.elements.generateBtn.addEventListener('click', () => this.generatePresentation());
        }

        // Edit mode
        if (this.elements.themeSelector) {
            this.elements.themeSelector.addEventListener('change', (e) => this.changeTheme(e.target.value));
        }

        this.elements.layoutOptions.forEach(option => {
            option.addEventListener('click', (e) => this.applyLayout(e.currentTarget.dataset.layout));
        });

        this.elements.addElements.forEach(btn => {
            btn.addEventListener('click', (e) => this.addElement(e.currentTarget.dataset.element));
        });

        // AI Assist
        if (this.elements.aiAssist) {
            this.elements.aiAssist.addEventListener('click', () => this.openAiAssist());
        }
        
        // AI option selection
        this.elements.aiOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                this.elements.aiOptions.forEach(opt => opt.classList.remove('selected'));
                e.currentTarget.classList.add('selected');
                
                // Show tip about selected option
                const optionType = e.currentTarget.dataset.option;
                const tips = {
                    'concise': '📝 Concise creates 5-7 focused slides - perfect for quick presentations!',
                    'detailed': '📚 Detailed creates 10-15 comprehensive slides with in-depth content.',
                    'pitch': '🎯 Pitch Deck creates investor-ready slides following startup pitch format.',
                    'educational': '🎓 Educational creates teaching-focused slides with clear learning objectives.'
                };
                this.showFloatingTip(tips[optionType]);
                
                // Tutorial progress
                if (this.state.tutorialActive && this.state.tutorialStep === 2) {
                    setTimeout(() => this.showTutorialStep(3), 1500);
                }
            });
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Z for undo
            if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
                e.preventDefault();
                this.showFloatingTip('↶ Undo functionality');
            }
            
            // Ctrl/Cmd + Y for redo
            if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
                e.preventDefault();
                this.showFloatingTip('↷ Redo functionality');
            }
            
            // Arrow keys for slide navigation in present mode
            if (this.state.mode === 'present') {
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                    this.nextSlide();
                } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                    this.previousSlide();
                } else if (e.key === 'Escape') {
                    this.switchMode('edit');
                }
            }
            
            // F for fullscreen present
            if (e.key === 'f' && this.state.mode === 'edit') {
                e.preventDefault();
                this.switchMode('present');
            }
        });
        
        // Add slide button
        const addSlideBtn = document.querySelector('.add-slide-btn');
        if (addSlideBtn) {
            addSlideBtn.addEventListener('click', () => this.addNewSlide());
        }
    }
    
    addNewSlide() {
        const newSlide = {
            id: this.state.slides.length + 1,
            layout: 'title-content',
            content: {
                title: 'New Slide',
                body: 'Click to edit content...'
            }
        };
        
        this.state.slides.push(newSlide);
        this.renderSlides();
        this.selectSlide(this.state.slides.length - 1);
        this.showNotification('✨ New slide added!', 'success', 2000);
    }
    
    nextSlide() {
        if (this.state.currentSlide < this.state.slides.length - 1) {
            this.selectSlide(this.state.currentSlide + 1);
        }
    }
    
    previousSlide() {
        if (this.state.currentSlide > 0) {
            this.selectSlide(this.state.currentSlide - 1);
        }
    }

    switchMode(mode) {
        this.state.mode = mode;
        
        // Update active button
        this.elements.modeButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        // Show/hide panels
        this.elements.createPanel.style.display = mode === 'create' ? 'flex' : 'none';
        this.elements.editPanel.style.display = mode === 'edit' ? 'flex' : 'none';
        this.elements.presentPanel.style.display = mode === 'present' ? 'flex' : 'none';

        // Mode-specific actions
        if (mode === 'edit' && this.state.slides.length > 0) {
            this.renderSlides();
        } else if (mode === 'present') {
            this.enterPresentMode();
            this.state.userProgress.presented = true;
        }

        // Show tutorial tip for current mode
        this.showModeTip(mode);
        
        // Tutorial progress
        if (mode === 'present' && this.state.tutorialActive && this.state.tutorialStep === 9) {
            this.showNotification('🎉 Congratulations! You\'ve completed the Gamma tutorial!', 'success', 5000);
            this.state.tutorialActive = false;
            this.dismissTutorial();
        }
    }
    
    enterPresentMode() {
        // Update present panel with current slide
        const presentSlide = document.querySelector('.present-slide');
        if (presentSlide && this.state.slides.length > 0) {
            const currentSlide = this.state.slides[this.state.currentSlide];
            let content = '';
            
            if (currentSlide.layout === 'title') {
                content = `
                    <h1 style="font-size: 4rem; margin-bottom: 2rem;">${currentSlide.content.title}</h1>
                    <p style="font-size: 2rem; color: #6b7280;">${currentSlide.content.subtitle}</p>
                `;
            } else if (currentSlide.layout === 'title-content') {
                content = `
                    <h2 style="font-size: 3rem; margin-bottom: 2rem;">${currentSlide.content.title}</h2>
                    <p style="font-size: 1.5rem; line-height: 1.8;">${currentSlide.content.body}</p>
                `;
            } else {
                content = `
                    <h2 style="font-size: 3rem;">${currentSlide.content.title}</h2>
                `;
            }
            
            presentSlide.innerHTML = content;
        }
        
        // Show presentation controls tip
        setTimeout(() => {
            this.showFloatingTip('⌨️ Use arrow keys to navigate, ESC to exit');
        }, 1000);
    }
    
    // Update present controls
    setupPresentControls() {
        const prevBtn = document.querySelector('.present-btn[title="Previous"]');
        const nextBtn = document.querySelector('.present-btn[title="Next"]');
        const exitBtn = document.querySelector('.present-btn[title="Exit"]');
        
        if (prevBtn) prevBtn.addEventListener('click', () => this.previousSlide());
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextSlide());
        if (exitBtn) exitBtn.addEventListener('click', () => this.switchMode('edit'));
    }

    selectCreateOption(option) {
        this.elements.createOptions.forEach(card => {
            card.classList.toggle('selected', card.dataset.option === option);
        });

        // Show relevant input based on option
        const inputSection = document.getElementById('gammaInputSection');
        inputSection.style.display = 'block';
        
        this.updateTutorialMessage(option);
    }

    async generatePresentation() {
        const topic = this.elements.topicInput.value.trim();
        if (!topic) {
            this.showNotification('Please enter a topic or description', 'warning');
            return;
        }

        this.state.aiGenerating = true;
        this.elements.generateBtn.disabled = true;
        this.elements.generateBtn.innerHTML = '<span class="spinner"></span> Generating...';

        // Simulate AI generation
        await this.simulateAiGeneration(topic);

        this.state.aiGenerating = false;
        this.elements.generateBtn.disabled = false;
        this.elements.generateBtn.innerHTML = '✨ Generate with AI';

        // Switch to edit mode
        this.switchMode('edit');
    }

    async simulateAiGeneration(topic) {
        // Show generation progress
        this.showGenerationProgress();
        
        // Simulate realistic AI generation with progress updates
        await this.simulateGenerationSteps(topic);

        // Get selected AI option
        const selectedOption = document.querySelector('.ai-option.selected');
        const optionType = selectedOption ? selectedOption.dataset.option : 'concise';
        
        // Generate slides based on topic and option
        this.state.slides = this.generateSlideContent(topic, optionType);

        this.renderSlides();
        this.state.userProgress.createdPresentation = true;
        
        // Hide progress and show success
        this.hideGenerationProgress();
        this.showNotification('🎉 Your presentation is ready! Click any slide to start editing.', 'success', 4000);
        
        // Progress to next tutorial step
        if (this.state.tutorialActive && this.state.tutorialStep === 3) {
            setTimeout(() => this.showTutorialStep(4), 2000);
        }
    }
    
    showGenerationProgress() {
        const progress = document.createElement('div');
        progress.id = 'generationProgress';
        progress.className = 'generation-progress';
        progress.innerHTML = `
            <div class="progress-content">
                <div class="progress-spinner"></div>
                <h3>✨ Creating your presentation</h3>
                <p id="progressMessage">Analyzing your topic...</p>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
        `;
        document.body.appendChild(progress);
        setTimeout(() => progress.classList.add('show'), 100);
    }
    
    async simulateGenerationSteps(topic) {
        const steps = [
            { message: 'Analyzing your topic...', duration: 400, progress: 15 },
            { message: 'Researching key concepts...', duration: 500, progress: 30 },
            { message: 'Structuring content...', duration: 400, progress: 50 },
            { message: 'Generating slides...', duration: 500, progress: 70 },
            { message: 'Applying design...', duration: 300, progress: 85 },
            { message: 'Finalizing presentation...', duration: 400, progress: 100 }
        ];
        
        for (const step of steps) {
            document.getElementById('progressMessage').textContent = step.message;
            document.getElementById('progressFill').style.width = `${step.progress}%`;
            await new Promise(resolve => setTimeout(resolve, step.duration));
        }
    }
    
    hideGenerationProgress() {
        const progress = document.getElementById('generationProgress');
        if (progress) {
            progress.classList.remove('show');
            setTimeout(() => progress.remove(), 300);
        }
    }
    
    generateSlideContent(topic, optionType) {
        const slideCount = optionType === 'concise' ? 5 : optionType === 'detailed' ? 12 : 8;
        const slides = [];
        
        // Title slide
        slides.push({
            id: 1,
            layout: 'title',
            content: {
                title: topic,
                subtitle: `A comprehensive presentation on ${topic.toLowerCase()}`
            }
        });
        
        // Introduction slide
        slides.push({
            id: 2,
            layout: 'title-content',
            content: {
                title: 'Introduction',
                body: `Welcome to this presentation on ${topic}. We'll explore key concepts, insights, and actionable takeaways that matter most.`
            }
        });
        
        // Content slides based on option
        if (optionType === 'pitch') {
            slides.push(
                {
                    id: 3,
                    layout: 'title-content',
                    content: {
                        title: 'The Problem',
                        body: 'Every great solution starts with understanding the problem. Here\'s what we\'re solving...'
                    }
                },
                {
                    id: 4,
                    layout: 'title-content',
                    content: {
                        title: 'Our Solution',
                        body: 'We\'ve developed an innovative approach that addresses these challenges head-on.'
                    }
                },
                {
                    id: 5,
                    layout: 'two-column',
                    content: {
                        title: 'Market Opportunity',
                        left: '📈 Market Size\n$X billion TAM',
                        right: '🎯 Target Audience\nKey demographics'
                    }
                },
                {
                    id: 6,
                    layout: 'title-content',
                    content: {
                        title: 'Business Model',
                        body: 'Revenue streams, pricing strategy, and path to profitability.'
                    }
                },
                {
                    id: 7,
                    layout: 'title-content',
                    content: {
                        title: 'Traction & Milestones',
                        body: 'Early wins, customer feedback, and growth metrics that matter.'
                    }
                },
                {
                    id: 8,
                    layout: 'title-content',
                    content: {
                        title: 'The Ask',
                        body: 'Investment needed, use of funds, and expected outcomes.'
                    }
                }
            );
        } else if (optionType === 'educational') {
            for (let i = 3; i <= slideCount; i++) {
                const layouts = ['title-content', 'two-column'];
                const layout = layouts[Math.floor(Math.random() * layouts.length)];
                
                if (layout === 'title-content') {
                    slides.push({
                        id: i,
                        layout: layout,
                        content: {
                            title: `Concept ${i - 2}`,
                            body: `Key learning point about ${topic}. This section covers important details and examples to help understand the concept better.`
                        }
                    });
                } else {
                    slides.push({
                        id: i,
                        layout: layout,
                        content: {
                            title: `Understanding ${topic}`,
                            left: `✓ Key principle\n✓ Important fact\n✓ Core concept`,
                            right: `📝 Example\n📊 Data point\n🎯 Application`
                        }
                    });
                }
            }
        } else {
            // General content
            for (let i = 3; i <= slideCount - 1; i++) {
                slides.push({
                    id: i,
                    layout: i % 3 === 0 ? 'two-column' : 'title-content',
                    content: {
                        title: `Key Point ${i - 2}`,
                        body: i % 3 === 0 ? undefined : `Important insights about ${topic} that provide value and understanding.`,
                        left: i % 3 === 0 ? `• Benefit 1\n• Benefit 2\n• Benefit 3` : undefined,
                        right: i % 3 === 0 ? `• Feature 1\n• Feature 2\n• Feature 3` : undefined
                    }
                });
            }
        }
        
        // Conclusion slide
        slides.push({
            id: slideCount,
            layout: 'title-content',
            content: {
                title: 'Thank You',
                body: 'Questions? Let\'s discuss further.'
            }
        });
        
        return slides;
    }

    renderSlides() {
        this.elements.slideList.innerHTML = '';
        
        this.state.slides.forEach((slide, index) => {
            const slideEl = document.createElement('div');
            slideEl.className = `gamma-slide-thumb ${index === this.state.currentSlide ? 'active' : ''}`;
            slideEl.dataset.index = index;
            slideEl.innerHTML = `
                <div class="slide-number">${index + 1}</div>
                <div class="slide-preview">
                    <div class="slide-preview-content">${slide.content.title || 'Slide ' + (index + 1)}</div>
                </div>
            `;
            slideEl.addEventListener('click', () => this.selectSlide(index));
            this.elements.slideList.appendChild(slideEl);
        });

        this.renderCurrentSlide();
    }

    selectSlide(index) {
        this.state.currentSlide = index;
        this.renderSlides();
    }

    renderCurrentSlide() {
        const slide = this.state.slides[this.state.currentSlide];
        if (!slide) return;

        let html = '';
        switch (slide.layout) {
            case 'title':
                html = `
                    <div class="gamma-slide-content title-layout">
                        <h1 class="editable" contenteditable="true">${slide.content.title}</h1>
                        <p class="subtitle editable" contenteditable="true">${slide.content.subtitle}</p>
                    </div>
                `;
                break;
            case 'title-content':
                html = `
                    <div class="gamma-slide-content title-content-layout">
                        <h2 class="editable" contenteditable="true">${slide.content.title}</h2>
                        <p class="editable" contenteditable="true">${slide.content.body}</p>
                    </div>
                `;
                break;
            case 'two-column':
                html = `
                    <div class="gamma-slide-content two-column-layout">
                        <h2 class="editable" contenteditable="true">${slide.content.title}</h2>
                        <div class="columns">
                            <div class="column editable" contenteditable="true">${slide.content.left}</div>
                            <div class="column editable" contenteditable="true">${slide.content.right}</div>
                        </div>
                    </div>
                `;
                break;
        }

        this.elements.canvas.innerHTML = html;
    }

    changeTheme(theme) {
        this.state.theme = theme;
        this.elements.canvas.className = `gamma-canvas theme-${theme}`;
        this.showNotification(`Theme changed to ${theme}`, 'info');
    }

    applyLayout(layout) {
        if (this.state.slides[this.state.currentSlide]) {
            this.state.slides[this.state.currentSlide].layout = layout;
            this.renderCurrentSlide();
            this.showNotification(`Layout changed to ${layout}`, 'info');
        }
    }

    addElement(elementType) {
        const slide = this.state.slides[this.state.currentSlide];
        if (!slide) return;
        
        // Show element customization panel
        this.showElementPanel(elementType);
        
        // Add element to slide (visual representation)
        const canvas = document.getElementById('gammaCanvas');
        const elementDiv = document.createElement('div');
        elementDiv.className = 'gamma-element draggable';
        elementDiv.dataset.type = elementType;
        
        let content = '';
        switch (elementType) {
            case 'text':
                content = '<p class="editable" contenteditable="true">Click to edit text...</p>';
                break;
            case 'image':
                content = '<div class="image-placeholder">🖼️ Click to upload image</div>';
                break;
            case 'video':
                content = '<div class="video-placeholder">🎥 Click to embed video</div>';
                break;
            case 'chart':
                content = '<div class="chart-placeholder">📊 Click to create chart</div>';
                break;
            case 'table':
                content = '<div class="table-placeholder">📋 Click to create table</div>';
                break;
            case 'code':
                content = '<pre class="code-placeholder">💻 Click to add code</pre>';
                break;
        }
        
        elementDiv.innerHTML = content;
        canvas.querySelector('.gamma-slide-content').appendChild(elementDiv);
        
        this.showNotification(`${elementType} added! Click to customize it.`, 'success', 3000);
        
        // Tutorial progress
        if (!this.state.userProgress.addedElement) {
            this.state.userProgress.addedElement = true;
            this.showFloatingTip('💡 Drag elements to reposition them!');
        }
    }
    
    showElementPanel(elementType) {
        const tips = {
            text: 'Add text boxes for custom content. Use the toolbar to format.',
            image: 'Upload images or generate them with AI. Supports PNG, JPG, GIF.',
            video: 'Embed YouTube, Vimeo, or upload videos. Plays inline during presentation.',
            chart: 'Create bar, line, pie, or scatter charts from your data.',
            table: 'Organize data in rows and columns. Fully customizable.',
            code: 'Add syntax-highlighted code blocks. Supports 50+ languages.'
        };
        
        this.showFloatingTip(`📝 ${tips[elementType]}`);
    }

    openAiAssist() {
        const modal = document.getElementById('gammaAiModal');
        const textarea = modal.querySelector('textarea');
        
        // Pre-fill with helpful suggestions
        const currentSlide = this.state.slides[this.state.currentSlide];
        if (currentSlide) {
            textarea.placeholder = `Try asking:\n• Make this slide more engaging\n• Add bullet points about ${currentSlide.content.title}\n• Simplify this for a general audience\n• Create a visual diagram for this concept`;
        }
        
        modal.style.display = 'flex';
        textarea.focus();
        
        // Tutorial progress
        if (!this.state.userProgress.usedAiAssist) {
            this.state.userProgress.usedAiAssist = true;
            this.showFloatingTip('🤖 AI Assist can rewrite, expand, or translate your content!');
        }
    }
    
    async processAiAssist(request) {
        const modal = document.getElementById('gammaAiModal');
        const generateBtn = modal.querySelector('.gamma-btn-primary');
        
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner"></span> Thinking...';
        
        // Simulate AI processing
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const slide = this.state.slides[this.state.currentSlide];
        if (slide) {
            // Update slide content based on request
            if (request.toLowerCase().includes('engaging')) {
                slide.content.body = `✨ ${slide.content.body || slide.content.title} - Now with more engaging language and compelling examples!`;
            } else if (request.toLowerCase().includes('bullet')) {
                slide.content.body = `• Key point one\n• Important insight two\n• Critical takeaway three`;
            } else if (request.toLowerCase().includes('simplify')) {
                slide.content.body = `Simplified version: ${slide.content.title} explained in clear, easy-to-understand terms.`;
            }
            
            this.renderCurrentSlide();
        }
        
        generateBtn.disabled = false;
        generateBtn.innerHTML = 'Generate';
        modal.style.display = 'none';
        
        this.showNotification('✨ Content updated with AI!', 'success', 3000);
    }

    loadSamplePresentation() {
        // Load a sample presentation for demonstration
        this.state.slides = [
            {
                id: 1,
                layout: 'title',
                content: {
                    title: 'Welcome to Gamma',
                    subtitle: 'Learn AI-Powered Presentations'
                }
            }
        ];
    }

    showModeTip(mode) {
        const tips = {
            create: '💡 Start by choosing how you want to create: from scratch, with AI, or import content!',
            edit: '✏️ Use the toolbar to customize your slides. Click any text to edit directly!',
            present: '🎬 Present mode lets you share your presentation with animations and transitions!'
        };
        
        this.showNotification(tips[mode], 'info', 5000);
    }

    updateTutorialMessage(option) {
        const messages = {
            blank: '📝 Starting with a blank presentation gives you full creative control!',
            ai: '🤖 AI generation creates a complete presentation from your topic or document!',
            import: '📄 Import existing content from PowerPoint, PDF, or documents!'
        };
        
        if (messages[option]) {
            this.showNotification(messages[option], 'info', 4000);
        }
    }

    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `gamma-notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
    
    restartTutorial() {
        this.state.tutorialActive = true;
        this.state.tutorialStep = 0;
        this.state.userProgress = {
            createdPresentation: false,
            editedSlide: false,
            changedTheme: false,
            addedElement: false,
            usedAiAssist: false,
            presented: false
        };
        
        // Switch to create mode
        this.switchMode('create');
        
        // Show first tutorial step
        setTimeout(() => this.showTutorialStep(0), 500);
    }
    
    showProgressIndicator() {
        const progress = Object.values(this.state.userProgress).filter(v => v).length;
        const total = Object.keys(this.state.userProgress).length;
        const percentage = Math.round((progress / total) * 100);
        
        // Update or create progress indicator
        let indicator = document.querySelector('.gamma-progress-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'gamma-progress-indicator';
            document.body.appendChild(indicator);
        }
        
        indicator.innerHTML = `
            <div class="progress-circle">
                <svg width="40" height="40">
                    <circle cx="20" cy="20" r="18" fill="none" stroke="#e5e7eb" stroke-width="3"/>
                    <circle cx="20" cy="20" r="18" fill="none" stroke="#7c3aed" stroke-width="3" 
                            stroke-dasharray="${percentage * 1.13} 113" 
                            transform="rotate(-90 20 20)" 
                            style="transition: stroke-dasharray 0.5s ease"/>
                </svg>
                <span class="progress-text">${progress}/${total}</span>
            </div>
            <span class="progress-label">Skills Learned</span>
        `;
        
        indicator.style.display = 'flex';
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('gammaModule')) {
        window.gammaModule = new GammaModule();
        
        // Show progress indicator
        setInterval(() => {
            if (window.gammaModule) {
                window.gammaModule.showProgressIndicator();
            }
        }, 2000);
    }
});

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('gammaModule')) {
        window.gammaModule = new GammaModule();
    }
});
