/**
 * Aurora Background JavaScript Controller
 * Handles animations, dark mode, and interactivity
 */

class AuroraBackground {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error(`Aurora: Container with id "${containerId}" not found`);
      return;
    }

    this.options = {
      showRadialGradient: options.showRadialGradient ?? true,
      darkMode: options.darkMode ?? false,
      animateContent: options.animateContent ?? true,
      autoDetectDarkMode: options.autoDetectDarkMode ?? true,
      ...options
    };

    this.init();
  }

  init() {
    // Add aurora classes to container
    this.container.classList.add('aurora-background');

    // Create aurora effect elements
    this.createAuroraEffect();

    // Wrap existing content
    this.wrapContent();

    // Set up dark mode
    if (this.options.autoDetectDarkMode) {
      this.detectDarkMode();
    } else if (this.options.darkMode) {
      this.enableDarkMode();
    }

    // Add content animation
    if (this.options.animateContent) {
      this.animateContent();
    }

    // Set up event listeners
    this.setupEventListeners();
  }

  createAuroraEffect() {
    // Create effect container
    const effectContainer = document.createElement('div');
    effectContainer.className = 'aurora-effect';

    // Create gradient element
    const gradient = document.createElement('div');
    gradient.className = 'aurora-gradient';
    
    if (this.options.showRadialGradient) {
      gradient.classList.add('with-radial-mask');
    }

    effectContainer.appendChild(gradient);
    
    // Insert at the beginning of container
    this.container.insertBefore(effectContainer, this.container.firstChild);
  }

  wrapContent() {
    // Get all child nodes except the aurora effect
    const children = Array.from(this.container.children).filter(
      child => !child.classList.contains('aurora-effect')
    );

    // Create content wrapper if there are children
    if (children.length > 0) {
      const contentWrapper = document.createElement('div');
      contentWrapper.className = 'aurora-content';

      children.forEach(child => {
        contentWrapper.appendChild(child);
      });

      this.container.appendChild(contentWrapper);
      this.contentWrapper = contentWrapper;
    }
  }

  animateContent() {
    if (this.contentWrapper) {
      // Use Intersection Observer for scroll-based animation
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              this.contentWrapper.classList.add('animate-in');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.1 }
      );

      observer.observe(this.contentWrapper);
    }
  }

  detectDarkMode() {
    // Check system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (prefersDark) {
      this.enableDarkMode();
    }

    // Listen for changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (e.matches) {
        this.enableDarkMode();
      } else {
        this.disableDarkMode();
      }
    });
  }

  enableDarkMode() {
    this.container.classList.add('dark-mode');
    this.options.darkMode = true;
  }

  disableDarkMode() {
    this.container.classList.remove('dark-mode');
    this.options.darkMode = false;
  }

  toggleDarkMode() {
    if (this.options.darkMode) {
      this.disableDarkMode();
    } else {
      this.enableDarkMode();
    }
  }

  setupEventListeners() {
    // Optional: Add keyboard shortcut for dark mode toggle (Ctrl/Cmd + D)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        this.toggleDarkMode();
      }
    });
  }

  destroy() {
    // Clean up
    const effectContainer = this.container.querySelector('.aurora-effect');
    if (effectContainer) {
      effectContainer.remove();
    }

    this.container.classList.remove('aurora-background', 'dark-mode');
  }
}

// Auto-initialize aurora backgrounds with data attributes
document.addEventListener('DOMContentLoaded', () => {
  const auroraElements = document.querySelectorAll('[data-aurora-background]');
  
  auroraElements.forEach(element => {
    const options = {
      showRadialGradient: element.dataset.auroraRadial !== 'false',
      darkMode: element.dataset.auroraDarkMode === 'true',
      animateContent: element.dataset.auroraAnimate !== 'false',
      autoDetectDarkMode: element.dataset.auroraAutoDetect !== 'false'
    };

    // Store instance on element
    element.auroraInstance = new AuroraBackground(element.id, options);
  });
});

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AuroraBackground;
}
