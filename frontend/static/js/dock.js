// Apple-Style Dock Navigation - Pure JS
// Handles advanced magnification and interaction effects

class AppleDock {
  constructor(container) {
    this.container = container;
    this.items = Array.from(container.querySelectorAll('.dock-item'));
    this.wrapper = container.querySelector('.dock-wrapper');
    this.mouseX = Infinity;
    this.isHovered = false;
    
    this.init();
  }

  init() {
    // Track mouse movement on dock
    this.wrapper.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.wrapper.addEventListener('mouseleave', () => this.handleMouseLeave());
    
    // Track current page for active state
    this.updateActiveState();
    
    // Add click ripple effect
    this.items.forEach(item => {
      item.addEventListener('click', (e) => this.createRipple(e));
    });
  }

  handleMouseMove(e) {
    this.isHovered = true;
    const rect = this.wrapper.getBoundingClientRect();
    this.mouseX = e.clientX - rect.left;
    this.updateMagnification();
  }

  handleMouseLeave() {
    this.isHovered = false;
    this.mouseX = Infinity;
    this.resetMagnification();
  }

  updateMagnification() {
    const MAGNIFICATION = 1.4;
    const DISTANCE_THRESHOLD = 100;

    this.items.forEach(item => {
      const rect = item.getBoundingClientRect();
      const wrapperRect = this.wrapper.getBoundingClientRect();
      const itemCenter = rect.left - wrapperRect.left + rect.width / 2;
      const distance = Math.abs(this.mouseX - itemCenter);

      if (distance < DISTANCE_THRESHOLD) {
        const scale = 1 + (1 - distance / DISTANCE_THRESHOLD) * (MAGNIFICATION - 1);
        const translateY = -(scale - 1) * 20;
        item.style.transform = `scale(${scale}) translateY(${translateY}px)`;
      } else {
        item.style.transform = 'scale(1) translateY(0)';
      }
    });
  }

  resetMagnification() {
    this.items.forEach(item => {
      item.style.transform = 'scale(1) translateY(0)';
    });
  }

  updateActiveState() {
    const currentPath = window.location.pathname;
    
    this.items.forEach(item => {
      const link = item.querySelector('a');
      if (link) {
        const href = link.getAttribute('href');
        // Check if current path matches or starts with href
        if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
          item.classList.add('active');
        } else if (href === '/' && currentPath === '/landing') {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      }
    });
  }

  createRipple(event) {
    const item = event.currentTarget;
    const ripple = document.createElement('span');
    
    const rect = item.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 70%);
      border-radius: 50%;
      transform: scale(0);
      animation: dockRipple 0.6s ease-out;
      pointer-events: none;
      z-index: 0;
    `;

    item.appendChild(ripple);

    ripple.addEventListener('animationend', () => {
      ripple.remove();
    });
  }
}

// Add ripple animation to stylesheet
function addDockStyles() {
  if (!document.getElementById('dock-animations')) {
    const style = document.createElement('style');
    style.id = 'dock-animations';
    style.textContent = `
      @keyframes dockRipple {
        to {
          transform: scale(2);
          opacity: 0;
        }
      }

      .dock-item {
        overflow: hidden;
        position: relative;
      }

      .dock-icon {
        position: relative;
        z-index: 1;
      }
    `;
    document.head.appendChild(style);
  }
}

// Auto-initialize docks
function initializeDocks() {
  addDockStyles();
  
  document.querySelectorAll('.dock-container').forEach(container => {
    new AppleDock(container);
  });
  
  console.log('Apple-style dock initialized');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeDocks);
} else {
  initializeDocks();
}

// Export for manual initialization
window.AppleDock = AppleDock;
window.initializeDocks = initializeDocks;
