/**
 * Glowing Effect JavaScript Controller
 * Mouse-tracking glowing border effect
 */

class GlowingEffect {
  constructor(container, options = {}) {
    this.container = container;
    this.options = {
      blur: options.blur ?? 0,
      inactiveZone: options.inactiveZone ?? 0.01,
      proximity: options.proximity ?? 64,
      spread: options.spread ?? 40,
      borderWidth: options.borderWidth ?? 3,
      movementDuration: options.movementDuration ?? 2000,
      disabled: options.disabled ?? false,
      ...options
    };

    this.lastPosition = { x: 0, y: 0 };
    this.animationFrame = null;
    this.currentAngle = 0;
    this.targetAngle = 0;
    this.animating = false;

    if (!this.options.disabled) {
      this.init();
    }
  }

  init() {
    // Set CSS variables
    this.container.style.setProperty('--glowing-spread', this.options.spread);
    this.container.style.setProperty('--glowing-blur', `${this.options.blur}px`);
    this.container.style.setProperty('--glowing-border-width', `${this.options.borderWidth}px`);
    this.container.style.setProperty('--glowing-start', '0deg');
    this.container.style.setProperty('--glowing-active', '0');

    // Bind event handlers
    this.handlePointerMove = this.handlePointerMove.bind(this);
    this.handleScroll = this.handleScroll.bind(this);
    this.update = this.update.bind(this);

    // Add event listeners
    document.body.addEventListener('pointermove', this.handlePointerMove, { passive: true });
    window.addEventListener('scroll', this.handleScroll, { passive: true });
  }

  handlePointerMove(e) {
    this.lastPosition = { x: e.clientX, y: e.clientY };
    this.scheduleUpdate();
  }

  handleScroll() {
    this.scheduleUpdate();
  }

  scheduleUpdate() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
    this.animationFrame = requestAnimationFrame(this.update);
  }

  update() {
    const rect = this.container.getBoundingClientRect();
    const { left, top, width, height } = rect;
    const { x: mouseX, y: mouseY } = this.lastPosition;

    // Calculate center
    const centerX = left + width * 0.5;
    const centerY = top + height * 0.5;

    // Distance from center
    const distanceFromCenter = Math.hypot(
      mouseX - centerX,
      mouseY - centerY
    );

    // Inactive zone check
    const inactiveRadius = 0.5 * Math.min(width, height) * this.options.inactiveZone;
    
    if (distanceFromCenter < inactiveRadius) {
      this.container.style.setProperty('--glowing-active', '0');
      return;
    }

    // Proximity check
    const isActive =
      mouseX > left - this.options.proximity &&
      mouseX < left + width + this.options.proximity &&
      mouseY > top - this.options.proximity &&
      mouseY < top + height + this.options.proximity;

    this.container.style.setProperty('--glowing-active', isActive ? '1' : '0');

    if (!isActive) return;

    // Calculate angle
    const targetAngle = (180 * Math.atan2(mouseY - centerY, mouseX - centerX)) / Math.PI + 90;

    // Smooth angle transition
    if (!this.animating) {
      this.animateAngle(targetAngle);
    } else {
      this.targetAngle = targetAngle;
    }
  }

  animateAngle(targetAngle) {
    const startAngle = this.currentAngle;
    
    // Calculate shortest angle difference
    let angleDiff = ((targetAngle - startAngle + 180) % 360) - 180;
    const endAngle = startAngle + angleDiff;

    const startTime = performance.now();
    const duration = this.options.movementDuration;

    this.animating = true;

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function (cubic bezier approximation for [0.16, 1, 0.3, 1])
      const eased = this.easeOutExpo(progress);

      const currentAngle = startAngle + (endAngle - startAngle) * eased;
      this.currentAngle = currentAngle;
      
      this.container.style.setProperty('--glowing-start', `${currentAngle}deg`);

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        this.animating = false;
        // Check if we need to start a new animation
        if (Math.abs(this.targetAngle - this.currentAngle) > 5) {
          this.animateAngle(this.targetAngle);
        }
      }
    };

    requestAnimationFrame(animate);
  }

  easeOutExpo(t) {
    // Approximation of cubic-bezier(0.16, 1, 0.3, 1)
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }

  destroy() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
    document.body.removeEventListener('pointermove', this.handlePointerMove);
    window.removeEventListener('scroll', this.handleScroll);
  }
}

// Auto-initialize glowing effects
document.addEventListener('DOMContentLoaded', () => {
  const glowingElements = document.querySelectorAll('[data-glowing-effect]');
  
  glowingElements.forEach(element => {
    const options = {
      spread: parseInt(element.dataset.glowingSpread) || 40,
      proximity: parseInt(element.dataset.glowingProximity) || 64,
      inactiveZone: parseFloat(element.dataset.glowingInactiveZone) || 0.01,
      borderWidth: parseInt(element.dataset.glowingBorderWidth) || 3,
      movementDuration: parseInt(element.dataset.glowingDuration) || 2000,
      disabled: element.dataset.glowingDisabled === 'true'
    };

    element.glowingInstance = new GlowingEffect(element, options);
  });
});

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GlowingEffect;
}
