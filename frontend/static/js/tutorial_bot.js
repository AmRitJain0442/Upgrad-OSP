/**
 * Tutorial Bot - Interactive Learning Guide
 * Points to UI elements and provides contextual guidance
 */

class TutorialBot {
    constructor() {
        this.currentStep = 0;
        this.isActive = false;
        this.tutorialSteps = [];
        this.elements = {
            bot: null,
            bubble: null,
            pointer: null,
            overlay: null
        };
        
        this.init();
    }

    init() {
        this.createBotElements();
        this.setupEventListeners();
        
        // Check if user has seen tutorial
        const hasSeenTutorial = localStorage.getItem('hasSeenTutorial');
        if (!hasSeenTutorial) {
            setTimeout(() => this.startTutorial(), 1000);
        }
    }

    createBotElements() {
        // Create overlay
        this.elements.overlay = document.createElement('div');
        this.elements.overlay.id = 'tutorialOverlay';
        this.elements.overlay.className = 'tutorial-overlay';
        this.elements.overlay.style.display = 'none';
        document.body.appendChild(this.elements.overlay);

        // Create bot character
        this.elements.bot = document.createElement('div');
        this.elements.bot.id = 'tutorialBot';
        this.elements.bot.className = 'tutorial-bot';
        this.elements.bot.innerHTML = `
            <div class="bot-character">
                <div class="bot-face">
                    <div class="bot-eyes">
                        <div class="bot-eye left"></div>
                        <div class="bot-eye right"></div>
                    </div>
                    <div class="bot-mouth"></div>
                </div>
            </div>
        `;
        document.body.appendChild(this.elements.bot);

        // Create speech bubble
        this.elements.bubble = document.createElement('div');
        this.elements.bubble.id = 'tutorialBubble';
        this.elements.bubble.className = 'tutorial-bubble';
        this.elements.bubble.innerHTML = `
            <div class="bubble-content">
                <p class="bubble-text"></p>
                <div class="bubble-actions">
                    <button class="bubble-btn skip-btn">Skip Tutorial</button>
                    <button class="bubble-btn next-btn">Next</button>
                </div>
            </div>
            <div class="bubble-tail"></div>
        `;
        document.body.appendChild(this.elements.bubble);

        // Create pointer arrow
        this.elements.pointer = document.createElement('div');
        this.elements.pointer.id = 'tutorialPointer';
        this.elements.pointer.className = 'tutorial-pointer';
        this.elements.pointer.innerHTML = `
            <svg width="40" height="40" viewBox="0 0 40 40">
                <path d="M20,10 L30,20 L20,30 L20,23 L10,23 L10,17 L20,17 Z" fill="#ef4444" stroke="#dc2626" stroke-width="2"/>
            </svg>
        `;
        document.body.appendChild(this.elements.pointer);
    }

    setupEventListeners() {
        const nextBtn = this.elements.bubble.querySelector('.next-btn');
        const skipBtn = this.elements.bubble.querySelector('.skip-btn');

        nextBtn.addEventListener('click', () => this.nextStep());
        skipBtn.addEventListener('click', () => this.endTutorial());
        this.elements.overlay.addEventListener('click', () => this.nextStep());
    }

    defineTutorialSteps() {
        let moduleId = 'general';
        
        if (window.location.pathname.includes('gamma-tool')) {
            moduleId = 'gamma-tool';
        } else if (window.location.pathname.includes('presentation-builder')) {
            moduleId = 'presentation-builder';
        }
        
        // Use external tutorial steps if available, otherwise use defaults
        if (moduleId === 'gamma-tool' && window.gammaTutorialSteps) {
            this.tutorialSteps = window.gammaTutorialSteps;
        } else if (moduleId === 'presentation-builder' && window.presentationTutorialSteps) {
            this.tutorialSteps = window.presentationTutorialSteps;
        } else if (window.generalTutorialSteps) {
            this.tutorialSteps = window.generalTutorialSteps;
        } else {
            // Fallback default steps
            this.tutorialSteps = [
                {
                    target: '#leftPanel',
                    position: 'right',
                    message: "👋 Welcome! I'm your AI learning companion. Let me show you around!",
                    highlight: '#leftPanel'
                },
                {
                    target: '#rightPanel',
                    position: 'left',
                    message: "This is your workspace where you'll interact with AI. Let's start learning! 🚀",
                    highlight: '#rightPanel'
                }
            ];
        }
    }

    startTutorial() {
        this.defineTutorialSteps();
        this.isActive = true;
        this.currentStep = 0;
        this.showStep(0);
        this.animateBotEntry();
    }

    showStep(stepIndex) {
        if (stepIndex >= this.tutorialSteps.length) {
            this.endTutorial();
            return;
        }

        const step = this.tutorialSteps[stepIndex];
        
        // Update bubble text
        const bubbleText = this.elements.bubble.querySelector('.bubble-text');
        bubbleText.innerHTML = step.message;

        // Update button text
        const nextBtn = this.elements.bubble.querySelector('.next-btn');
        nextBtn.textContent = stepIndex === this.tutorialSteps.length - 1 ? "Got it!" : "Next";

        // Show overlay
        this.elements.overlay.style.display = 'block';

        // Highlight target element
        if (step.highlight) {
            this.highlightElement(step.highlight);
        } else {
            this.clearHighlight();
        }

        // Position bot and bubble
        if (step.target) {
            this.positionNearTarget(step.target, step.position);
        } else {
            this.positionCenter();
        }

        // Animate bot
        this.animateBot();
    }

    positionNearTarget(selector, position) {
        const target = document.querySelector(selector);
        if (!target) {
            this.positionCenter();
            return;
        }

        const rect = target.getBoundingClientRect();
        const botRect = this.elements.bot.getBoundingClientRect();
        const bubbleRect = this.elements.bubble.getBoundingClientRect();

        let botX, botY, bubbleX, bubbleY, pointerX, pointerY;

        switch (position) {
            case 'right':
                botX = rect.right + 20;
                botY = rect.top + (rect.height / 2) - (botRect.height / 2);
                bubbleX = botX + botRect.width + 10;
                bubbleY = botY - 20;
                pointerX = rect.right + 5;
                pointerY = rect.top + (rect.height / 2) - 20;
                break;
            case 'left':
                botX = rect.left - botRect.width - 20;
                botY = rect.top + (rect.height / 2) - (botRect.height / 2);
                bubbleX = botX - bubbleRect.width - 10;
                bubbleY = botY - 20;
                pointerX = rect.left - 45;
                pointerY = rect.top + (rect.height / 2) - 20;
                break;
            case 'top':
                botX = rect.left + (rect.width / 2) - (botRect.width / 2);
                botY = rect.top - botRect.height - 20;
                bubbleX = botX - 50;
                bubbleY = botY - bubbleRect.height - 10;
                pointerX = rect.left + (rect.width / 2) - 20;
                pointerY = rect.top - 45;
                break;
            case 'bottom':
                botX = rect.left + (rect.width / 2) - (botRect.width / 2);
                botY = rect.bottom + 20;
                bubbleX = botX - 50;
                bubbleY = botY + botRect.height + 10;
                pointerX = rect.left + (rect.width / 2) - 20;
                pointerY = rect.bottom + 5;
                break;
        }

        // Keep elements on screen
        botX = Math.max(10, Math.min(botX, window.innerWidth - botRect.width - 10));
        botY = Math.max(10, Math.min(botY, window.innerHeight - botRect.height - 10));
        bubbleX = Math.max(10, Math.min(bubbleX, window.innerWidth - bubbleRect.width - 10));
        bubbleY = Math.max(10, Math.min(bubbleY, window.innerHeight - bubbleRect.height - 10));

        this.elements.bot.style.left = `${botX}px`;
        this.elements.bot.style.top = `${botY}px`;
        this.elements.bubble.style.left = `${bubbleX}px`;
        this.elements.bubble.style.top = `${bubbleY}px`;
        this.elements.pointer.style.left = `${pointerX}px`;
        this.elements.pointer.style.top = `${pointerY}px`;
        this.elements.pointer.style.display = 'block';
    }

    positionCenter() {
        const botRect = this.elements.bot.getBoundingClientRect();
        const bubbleRect = this.elements.bubble.getBoundingClientRect();

        const botX = (window.innerWidth / 2) - (botRect.width / 2);
        const botY = (window.innerHeight / 2) - (botRect.height / 2) - 50;
        const bubbleX = (window.innerWidth / 2) - (bubbleRect.width / 2);
        const bubbleY = botY + botRect.height + 20;

        this.elements.bot.style.left = `${botX}px`;
        this.elements.bot.style.top = `${botY}px`;
        this.elements.bubble.style.left = `${bubbleX}px`;
        this.elements.bubble.style.top = `${bubbleY}px`;
        this.elements.pointer.style.display = 'none';
    }

    highlightElement(selector) {
        this.clearHighlight();
        const element = document.querySelector(selector);
        if (element) {
            element.classList.add('tutorial-highlight');
        }
    }

    clearHighlight() {
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });
    }

    animateBot() {
        this.elements.bot.style.animation = 'none';
        setTimeout(() => {
            this.elements.bot.style.animation = 'botBounce 0.6s ease';
        }, 10);
        
        // Add a subtle celebration for important steps
        const step = this.tutorialSteps[this.currentStep];
        if (step && step.message.includes('🎯')) {
            this.celebrateBot();
        }
    }

    animateBotEntry() {
        this.elements.bot.style.animation = 'botEntry 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        this.elements.bubble.style.animation = 'bubbleEntry 0.5s ease 0.3s backwards';
    }
    
    celebrateBot() {
        // Add sparkle effect
        const sparkles = document.createElement('div');
        sparkles.className = 'bot-sparkles';
        sparkles.innerHTML = '✨';
        this.elements.bot.appendChild(sparkles);
        
        setTimeout(() => sparkles.remove(), 1000);
    }

    nextStep() {
        this.currentStep++;
        this.showStep(this.currentStep);
    }

    endTutorial() {
        this.isActive = false;
        this.elements.overlay.style.display = 'none';
        this.elements.bot.style.animation = 'botExit 0.5s ease forwards';
        this.elements.bubble.style.animation = 'bubbleExit 0.5s ease forwards';
        this.elements.pointer.style.display = 'none';
        this.clearHighlight();
        
        localStorage.setItem('hasSeenTutorial', 'true');
        
        setTimeout(() => {
            this.elements.bot.style.display = 'none';
            this.elements.bubble.style.display = 'none';
        }, 500);
    }

    // Public method to restart tutorial
    restart() {
        this.elements.bot.style.display = 'block';
        this.elements.bubble.style.display = 'block';
        this.startTutorial();
    }
}

// Initialize tutorial bot when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.tutorialBot = new TutorialBot();
    });
} else {
    window.tutorialBot = new TutorialBot();
}

// Add global function to restart tutorial
window.restartTutorial = function() {
    if (window.tutorialBot) {
        localStorage.removeItem('hasSeenTutorial');
        window.tutorialBot.restart();
    }
};
