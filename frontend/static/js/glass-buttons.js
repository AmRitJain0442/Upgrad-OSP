// Glass Button JavaScript - Pure JS Implementation
// Handles interactive effects for glass and metal buttons

class GlassButton {
  constructor(element) {
    this.button = element;
    this.init();
  }

  init() {
    // Add ripple effect on click
    this.button.addEventListener('click', (e) => this.createRipple(e));
    
    // Add pointer tracking for enhanced glass effect
    this.button.addEventListener('pointermove', (e) => this.updateGlassEffect(e));
    this.button.addEventListener('pointerleave', () => this.resetGlassEffect());
  }

  createRipple(event) {
    const ripple = document.createElement('span');
    const rect = this.button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple-animation 600ms ease-out;
      pointer-events: none;
      z-index: 5;
    `;

    this.button.appendChild(ripple);

    ripple.addEventListener('animationend', () => {
      ripple.remove();
    });
  }

  updateGlassEffect(event) {
    const rect = this.button.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;

    // Update gradient position based on mouse
    this.button.style.setProperty('--mouse-x', `${x}%`);
    this.button.style.setProperty('--mouse-y', `${y}%`);
  }

  resetGlassEffect() {
    this.button.style.setProperty('--mouse-x', '50%');
    this.button.style.setProperty('--mouse-y', '50%');
  }
}

class MetalButton {
  constructor(element) {
    this.wrapper = element;
    this.button = element.querySelector('.metal-btn-content');
    this.isPressed = false;
    this.isHovered = false;
    this.isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    this.init();
  }

  init() {
    // Mouse events
    this.wrapper.addEventListener('mousedown', () => this.handlePress());
    this.wrapper.addEventListener('mouseup', () => this.handleRelease());
    this.wrapper.addEventListener('mouseleave', () => this.handleLeave());
    this.wrapper.addEventListener('mouseenter', () => this.handleEnter());

    // Touch events
    this.wrapper.addEventListener('touchstart', () => this.handlePress(), { passive: true });
    this.wrapper.addEventListener('touchend', () => this.handleRelease());
    this.wrapper.addEventListener('touchcancel', () => this.handleRelease());
  }

  handlePress() {
    this.isPressed = true;
    this.updateState();
  }

  handleRelease() {
    this.isPressed = false;
    this.updateState();
  }

  handleLeave() {
    this.isPressed = false;
    this.isHovered = false;
    this.updateState();
  }

  handleEnter() {
    if (!this.isTouchDevice) {
      this.isHovered = true;
      this.updateState();
    }
  }

  updateState() {
    // Transform effects are handled by CSS :active and :hover
    // This is just for additional shine effect
    const shine = this.wrapper.querySelector('.metal-btn-shine');
    if (shine) {
      shine.style.opacity = this.isPressed ? '0.2' : '0';
    }
  }
}

// Auto-initialize all glass and metal buttons
function initGlassButtons() {
  // Initialize liquid glass buttons
  const glassButtons = document.querySelectorAll('.liquid-glass-btn');
  glassButtons.forEach(button => {
    new GlassButton(button);
  });

  // Initialize metal buttons
  const metalButtons = document.querySelectorAll('.metal-btn');
  metalButtons.forEach(button => {
    new MetalButton(button);
  });

  // Add ripple animation to stylesheet if not exists
  if (!document.getElementById('glass-button-animations')) {
    const style = document.createElement('style');
    style.id = 'glass-button-animations';
    style.textContent = `
      @keyframes ripple-animation {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }

      .liquid-glass-btn {
        --mouse-x: 50%;
        --mouse-y: 50%;
      }

      .liquid-glass-btn::after {
        background: radial-gradient(
          circle at var(--mouse-x) var(--mouse-y),
          rgba(255, 255, 255, 0.2) 0%,
          rgba(255, 255, 255, 0.1) 30%,
          rgba(255, 255, 255, 0.05) 50%,
          rgba(255, 255, 255, 0.15) 100%
        );
      }
    `;
    document.head.appendChild(style);
  }

  // Create SVG filter for liquid glass effect
  createGlassFilter();
}

function createGlassFilter() {
  if (document.getElementById('glass-svg-filter')) return;

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.id = 'glass-svg-filter';
  svg.classList.add('liquid-glass-filter');
  svg.innerHTML = `
    <defs>
      <filter
        id="container-glass"
        x="0%"
        y="0%"
        width="100%"
        height="100%"
        colorInterpolationFilters="sRGB"
      >
        <!-- Generate turbulent noise for distortion -->
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.05 0.05"
          numOctaves="1"
          seed="1"
          result="turbulence"
        />

        <!-- Blur the turbulence pattern slightly -->
        <feGaussianBlur in="turbulence" stdDeviation="2" result="blurredNoise" />

        <!-- Displace the source graphic with the noise -->
        <feDisplacementMap
          in="SourceGraphic"
          in2="blurredNoise"
          scale="70"
          xChannelSelector="R"
          yChannelSelector="B"
          result="displaced"
        />

        <!-- Apply overall blur on the final result -->
        <feGaussianBlur in="displaced" stdDeviation="4" result="finalBlur" />

        <!-- Output the result -->
        <feComposite in="finalBlur" in2="finalBlur" operator="over" />
      </filter>
    </defs>
  `;
  document.body.appendChild(svg);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initGlassButtons);
} else {
  initGlassButtons();
}

// Export for manual initialization
window.GlassButton = GlassButton;
window.MetalButton = MetalButton;
window.initGlassButtons = initGlassButtons;
