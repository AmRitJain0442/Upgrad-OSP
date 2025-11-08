/**
 * Gamma AI Presentation Tool - Learning Module
 * Teaches users how to use Gamma's interface and features
 */

// Gamma module state management
class GammaModule {
    constructor() {
        this.state = {
            mode: 'create', // create, edit, present
            currentSlide: 0,
            slides: [],
            theme: 'professional',
            aiGenerating: false
        };
        
        this.elements = {};
        this.init();
    }

    init() {
        this.cacheElements();
        this.setupEventListeners();
        this.loadSamplePresentation();
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

        // Show tutorial tip for current mode
        this.showModeTip(mode);
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
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Generate sample slides based on topic
        this.state.slides = [
            {
                id: 1,
                layout: 'title',
                content: {
                    title: topic,
                    subtitle: 'Generated by Gamma AI'
                }
            },
            {
                id: 2,
                layout: 'title-content',
                content: {
                    title: 'Introduction',
                    body: 'This presentation was generated using AI based on your topic.'
                }
            },
            {
                id: 3,
                layout: 'two-column',
                content: {
                    title: 'Key Points',
                    left: 'Point 1: Comprehensive coverage',
                    right: 'Point 2: AI-powered insights'
                }
            }
        ];

        this.renderSlides();
        this.showNotification('Presentation generated successfully!', 'success');
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
        this.showNotification(`Adding ${elementType} element...`, 'info');
        // Implementation for adding elements
    }

    openAiAssist() {
        const modal = document.getElementById('gammaAiModal');
        modal.style.display = 'flex';
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
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('gammaModule')) {
        window.gammaModule = new GammaModule();
    }
});
