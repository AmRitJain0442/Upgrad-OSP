# Tutorial Bot Feature 🤖

## Overview
The Tutorial Bot is an interactive, animated floating guide that helps users learn the platform by pointing to UI elements and providing contextual guidance. It creates an engaging learning experience with a friendly character that moves around the screen and highlights important features.

## Features

### 🎭 Animated Character
- **Floating red bot** with animated face (eyes, mouth)
- Smooth animations: floating, bouncing, blinking, talking
- Entry/exit animations with rotation and scaling
- Celebration sparkles for important steps

### 💬 Interactive Speech Bubbles
- Clean, modern speech bubbles with gradient accent
- Support for markdown formatting (bold, lists, emojis)
- "Next" and "Skip Tutorial" buttons
- Responsive positioning based on screen size

### 🎯 Element Highlighting
- Pulsing red glow around highlighted elements
- Brings highlighted elements to front (z-index boost)
- Smooth transitions between highlights
- Overlay darkens background to focus attention

### 👉 Pointing Arrows
- Animated SVG arrows point to specific UI elements
- Pulsing animation for attention
- Automatically positioned based on tutorial step
- Hidden for center-screen messages

### 📚 Context-Aware Tutorials
- Different tutorial paths for different modules
- Presentation Builder: 11 comprehensive steps
- General modules: 4 basic steps
- External tutorial definition via `tutorial_steps.js`

### 💾 Persistent State
- Uses localStorage to track if user has seen tutorial
- Won't repeat automatically on subsequent visits
- Can be manually restarted via help button

### ❓ Help Button
- Fixed position button (bottom-right corner)
- Click to restart tutorial anytime
- Hover effects with rotation animation
- Question mark icon

## File Structure

```
frontend/static/
├── js/
│   ├── tutorial_bot.js         # Main bot logic and animations
│   └── tutorial_steps.js       # Tutorial step definitions
└── css/
    └── tutorial_bot.css        # All bot styling and animations

frontend/templates/
└── base.html                   # Includes bot scripts and help button
```

## How It Works

### 1. Initialization
```javascript
// Bot automatically initializes on page load
window.tutorialBot = new TutorialBot();

// Checks localStorage for 'hasSeenTutorial'
// If false, starts tutorial after 1 second delay
```

### 2. Tutorial Steps
Each step contains:
- `target`: CSS selector for element to point to (or null for center)
- `position`: 'right', 'left', 'top', 'bottom', or 'center'
- `message`: Text with markdown support
- `highlight`: CSS selector for element to highlight

Example:
```javascript
{
    target: '#uploadSection',
    position: 'top',
    message: "📄 Start by **uploading a document** or using a sample!",
    highlight: '#uploadSection'
}
```

### 3. Step Navigation
- User clicks "Next" button or overlay to advance
- Bot repositions to new target element
- Previous highlights are removed
- New element is highlighted and pointed to
- Speech bubble updates with new message

### 4. Positioning Logic
- Bot positions itself near target element based on `position` value
- Speech bubble positioned relative to bot
- Pointer arrow points from bot to target
- All elements kept within viewport bounds
- Responsive adjustments for mobile screens

## Customization

### Adding New Tutorial Steps

1. Edit `tutorial_steps.js`:
```javascript
const myCustomTutorial = [
    {
        target: '.my-element',
        position: 'right',
        message: "This is my custom step! 🎉",
        highlight: '.my-element'
    },
    // ... more steps
];

window.myCustomTutorial = myCustomTutorial;
```

2. Update `tutorial_bot.js` to use new steps:
```javascript
defineTutorialSteps() {
    if (window.myCustomTutorial) {
        this.tutorialSteps = window.myCustomTutorial;
    }
}
```

### Styling Customization

#### Change Bot Color
Edit `tutorial_bot.css`:
```css
.bot-character {
    background: linear-gradient(135deg, #your-color 0%, #your-color-light 100%);
}
```

#### Change Bubble Style
```css
.bubble-content {
    background: white;
    border-radius: 16px;
    /* Customize here */
}
```

#### Adjust Animations
```css
@keyframes botFloat {
    /* Modify animation timing and values */
}
```

## API Reference

### Global Functions

#### `restartTutorial()`
Manually restart the tutorial from beginning.
```javascript
// In browser console or onclick handler
restartTutorial();
```

#### `window.tutorialBot`
Access to the TutorialBot instance.
```javascript
// Check if tutorial is active
console.log(window.tutorialBot.isActive);

// Get current step
console.log(window.tutorialBot.currentStep);

// End tutorial programmatically
window.tutorialBot.endTutorial();
```

### Class Methods

#### `startTutorial()`
Begin tutorial from step 0. Automatically called on first visit.

#### `showStep(stepIndex)`
Display specific tutorial step.
```javascript
window.tutorialBot.showStep(2); // Jump to step 3
```

#### `nextStep()`
Advance to next tutorial step.

#### `endTutorial()`
End tutorial, hide bot, save state to localStorage.

#### `restart()`
Public method to restart tutorial (used by help button).

## Best Practices

### Writing Effective Messages
1. **Be concise**: Keep messages under 3 sentences
2. **Use emojis**: Makes messages friendly and scannable
3. **Use bold**: Highlight **key terms** with markdown
4. **Be specific**: Tell users exactly what to do
5. **Build progressively**: Each step should build on previous

### Example Good Messages
✅ "📄 Start by **uploading a document** or using a sample. This is the content we'll transform!"

✅ "This **AI Tutor panel** teaches you prompting strategies. Follow along step by step! 📚"

### Example Bad Messages
❌ "You can upload files here if you want to use the system."

❌ "This panel contains the artificial intelligence tutor component which provides educational guidance."

### Positioning Tips
- Use `'right'` for left-side elements (bot appears on right)
- Use `'left'` for right-side elements (bot appears on left)
- Use `'top'` for bottom elements
- Use `'bottom'` for top elements
- Use `'center'` with `target: null` for summary messages

### Highlight Carefully
- Only highlight the most relevant container
- Don't highlight entire panels unless necessary
- Highlight specific interactive elements when possible
- Use `null` for highlight on summary steps

## Browser Compatibility
- Chrome 90+: ✅ Full support
- Firefox 88+: ✅ Full support
- Safari 14+: ✅ Full support
- Edge 90+: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Performance
- Minimal performance impact
- CSS animations use GPU acceleration
- No heavy libraries or dependencies
- Lazy initialization (only starts when needed)
- Clean removal after tutorial ends

## Accessibility
- Keyboard navigation: Use Tab to focus buttons
- Screen readers: Aria labels could be added
- High contrast: Red gradient visible on dark backgrounds
- Skip option: Users can dismiss anytime

## Future Enhancements
- [ ] Add sound effects option
- [ ] Multi-language support
- [ ] Progress indicator (step X of Y)
- [ ] Branch tutorials based on user actions
- [ ] Tutorial completion tracking
- [ ] Tooltips for individual UI elements
- [ ] Voice narration option
- [ ] Tutorial search/jump to specific topic

## Troubleshooting

### Bot doesn't appear
1. Check browser console for errors
2. Verify `tutorial_bot.js` and `tutorial_steps.js` are loaded
3. Clear localStorage: `localStorage.removeItem('hasSeenTutorial')`
4. Refresh page

### Bot positioned incorrectly
1. Check target selector is valid
2. Ensure target element exists in DOM
3. Try different position value
4. Check for CSS conflicts affecting z-index

### Tutorial doesn't save state
1. Check localStorage is enabled in browser
2. Verify no browser extensions blocking storage
3. Check console for storage errors

### Animations not smooth
1. Check browser GPU acceleration is enabled
2. Reduce number of active animations
3. Test on different device/browser
4. Check for CSS conflicts

## Credits
- Designed for Upgrad OSP Platform
- Red gradient theme integration
- Inspired by modern onboarding experiences
- Built with vanilla JavaScript (no dependencies)
