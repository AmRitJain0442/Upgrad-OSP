# Aurora Background - Vanilla CSS/JS Implementation

## Overview
A pure CSS/JavaScript implementation of the Aurora Background effect, compatible with FastAPI + Jinja2 templates. No React, Tailwind, or TypeScript required.

## Files Created

```
frontend/
├── static/
│   ├── css/
│   │   └── aurora-background.css    # Aurora effect styles
│   └── js/
│       └── aurora-background.js     # Aurora controller class
└── templates/
    └── aurora-demo.html             # Demo page
```

## Quick Start

### 1. View the Demo
Visit: `http://localhost:8000/aurora-demo`

### 2. Basic Usage in Your Templates

```html
{% extends "base.html" %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', path='/css/aurora-background.css') }}">
{% endblock %}

{% block content %}
<!-- Add data-aurora-background to any container -->
<div id="myAurora" data-aurora-background>
  <h1>Your Content Here</h1>
  <p>Content will be automatically wrapped and animated</p>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', path='/js/aurora-background.js') }}"></script>
{% endblock %}
```

## Features

### ✨ Visual Effects
- **Animated aurora gradient** - Smooth 60s animation cycle
- **Dual-layer effects** - Primary and secondary gradients with blend modes
- **Blur and glow** - 10px blur filter for soft glow effect
- **Color palette** - Blue, indigo, and violet gradient colors

### 🌓 Dark Mode Support
- **Auto-detection** - Respects system preference
- **Manual toggle** - Programmatic control via JavaScript
- **Keyboard shortcut** - Ctrl/Cmd + D to toggle
- **Smooth transitions** - CSS transitions between modes

### 🎬 Content Animation
- **Fade-in effect** - Content fades in from bottom (0.8s)
- **Intersection Observer** - Animates when scrolled into view
- **Customizable delay** - 0.3s delay by default

### 📐 Responsive Design
- **Mobile-friendly** - Adapts text sizes for small screens
- **Flexbox layout** - Centers content vertically and horizontally
- **Full viewport** - min-height: 100vh

## Configuration Options

### Data Attributes (Auto-initialization)

```html
<div id="aurora" 
     data-aurora-background 
     data-aurora-radial="true"          <!-- Show radial gradient mask -->
     data-aurora-dark-mode="false"      <!-- Force dark/light mode -->
     data-aurora-animate="true"         <!-- Animate content on load -->
     data-aurora-auto-detect="true">    <!-- Auto-detect dark mode -->
  <!-- Your content -->
</div>
```

### JavaScript API

```javascript
// Create instance manually
const aurora = new AuroraBackground('myAurora', {
  showRadialGradient: true,
  darkMode: false,
  animateContent: true,
  autoDetectDarkMode: true
});

// Control methods
aurora.enableDarkMode();
aurora.disableDarkMode();
aurora.toggleDarkMode();
aurora.destroy();  // Clean up
```

## Advanced Examples

### Example 1: Landing Page with Aurora

```html
{% extends "base.html" %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', path='/css/aurora-background.css') }}">
<style>
  .hero-title {
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1rem;
  }
  
  .hero-subtitle {
    font-size: 1.5rem;
    opacity: 0.8;
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .cta-button {
    background: #ef4444;
    color: white;
    padding: 1rem 2rem;
    border-radius: 50px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  
  .cta-button:hover {
    transform: scale(1.1);
  }
</style>
{% endblock %}

{% block content %}
<div id="hero" data-aurora-background data-aurora-radial="true">
  <div class="hero-title">
    Master Prompt Engineering
  </div>
  <div class="hero-subtitle">
    Learn AI interaction with hands-on lessons and real-time guidance
  </div>
  <button class="cta-button" onclick="location.href='/prompting/'">
    Start Learning
  </button>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', path='/js/aurora-background.js') }}"></script>
{% endblock %}
```

### Example 2: Section Background (Partial Height)

```html
<style>
  .aurora-section {
    min-height: 60vh;  /* Not full viewport */
  }
</style>

<div id="features" class="aurora-section" data-aurora-background>
  <h2>Platform Features</h2>
  <div class="features-grid">
    <!-- Feature cards -->
  </div>
</div>
```

### Example 3: Multiple Aurora Sections

```html
<!-- Each section has its own aurora effect -->
<div id="aurora1" data-aurora-background data-aurora-radial="true">
  <h1>Section 1</h1>
</div>

<div id="aurora2" data-aurora-background data-aurora-radial="false">
  <h1>Section 2</h1>
</div>

<!-- All initialize automatically -->
```

### Example 4: Programmatic Control

```javascript
// Initialize with custom settings
const aurora = new AuroraBackground('mySection', {
  showRadialGradient: false,
  darkMode: true,
  animateContent: false
});

// Add dark mode toggle button
document.getElementById('toggleBtn').addEventListener('click', () => {
  aurora.toggleDarkMode();
});

// Clean up when navigating away
window.addEventListener('beforeunload', () => {
  aurora.destroy();
});
```

## Integration with Existing Pages

### Adding Aurora to Workflow Page

```html
<!-- frontend/templates/prompting/workflow.html -->
{% extends "base.html" %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', path='/css/workflow.css') }}">
<link rel="stylesheet" href="{{ url_for('static', path='/css/aurora-background.css') }}">
{% endblock %}

{% block content %}
<!-- Wrap entire workflow in aurora -->
<div id="workflowAurora" data-aurora-background data-aurora-animate="false">
  <div class="workflow-container">
    <!-- Existing workflow content -->
  </div>
</div>
{% endblock %}
```

### Adding Aurora to Course Module Page

```html
<!-- Add aurora to background of module page -->
<div id="moduleHero" data-aurora-background data-aurora-radial="true">
  <div class="module-header">
    <h1>{{ module.title }}</h1>
    <p>{{ module.description }}</p>
  </div>
</div>

<!-- Rest of module content outside aurora -->
<div class="module-content">
  <!-- Lessons, etc. -->
</div>
```

## Customization

### Custom Colors

```css
/* Override aurora color palette */
:root {
  --aurora-blue-500: #your-color;
  --aurora-blue-400: #your-color;
  --aurora-blue-300: #your-color;
  --aurora-indigo-300: #your-color;
  --aurora-violet-200: #your-color;
}
```

### Custom Animation Speed

```css
/* Make animation faster/slower */
.aurora-gradient {
  animation: aurora-move 30s linear infinite;  /* Changed from 60s */
}
```

### Custom Blur Amount

```css
.aurora-gradient {
  filter: blur(20px);  /* Changed from 10px */
}
```

### Disable Radial Mask

```html
<!-- Remove radial gradient mask -->
<div data-aurora-background data-aurora-radial="false">
```

## Performance Considerations

### Optimizations Applied
- ✅ `will-change: transform` - GPU acceleration hint
- ✅ `transform: translateZ(0)` - Force GPU rendering
- ✅ `backface-visibility: hidden` - Prevent flicker
- ✅ CSS animations (not JS) - Hardware accelerated
- ✅ `pointer-events: none` - Aurora doesn't block interactions

### Best Practices
- Use aurora on hero sections, not entire pages
- Limit to 1-2 aurora sections per page
- Consider disabling on mobile for better performance
- Test on lower-end devices

## Browser Compatibility

### Supported Browsers
- ✅ Chrome/Edge 88+
- ✅ Firefox 85+
- ✅ Safari 14+
- ✅ Opera 74+

### Fallback for Old Browsers
```css
/* Add fallback background */
.aurora-background {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Aurora effect only for modern browsers */
@supports (mix-blend-mode: difference) {
  .aurora-gradient {
    /* Aurora styles */
  }
}
```

## Troubleshooting

### Issue: Aurora not showing
**Solution:** Ensure both CSS and JS files are loaded:
```html
<link rel="stylesheet" href="/static/css/aurora-background.css">
<script src="/static/js/aurora-background.js"></script>
```

### Issue: Content not animating
**Solution:** Make sure container has an ID:
```html
<div id="myAurora" data-aurora-background>
```

### Issue: Dark mode not working
**Solution:** Check browser support for `prefers-color-scheme`:
```javascript
// Manually toggle instead
aurora.toggleDarkMode();
```

### Issue: Performance issues on mobile
**Solution:** Disable animations on mobile:
```css
@media (max-width: 768px) {
  .aurora-gradient,
  .aurora-gradient::after {
    animation: none !important;
  }
}
```

## Comparison to React Version

| Feature | React Version | Vanilla JS Version |
|---------|---------------|-------------------|
| Aurora animation | ✅ | ✅ |
| Dark mode | ✅ | ✅ |
| Auto-initialization | ❌ | ✅ |
| Dependencies | React, Tailwind, framer-motion | None |
| Bundle size | ~150KB | ~10KB |
| Setup time | 30+ min | 2 min |
| Learning curve | High | Low |

## Next Steps

1. **View the demo**: http://localhost:8000/aurora-demo
2. **Try integrating** into your existing pages
3. **Customize colors** to match your brand
4. **Add to landing page** for visual impact

## Support

For issues or questions:
- Check the demo page for working example
- Review JavaScript console for errors
- Ensure all files are in correct paths
- Test in latest Chrome/Firefox first
