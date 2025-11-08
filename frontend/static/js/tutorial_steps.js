/**
 * Presentation Builder Tutorial Steps
 * Extended tutorial specific to presentation builder workflow
 */

const presentationTutorialSteps = [
    {
        target: '#leftPanel .panel-header',
        position: 'right',
        message: "👋 **Welcome to the Presentation Builder!** I'm your AI learning companion. I'll guide you through creating amazing presentations using smart prompts!",
        highlight: '#leftPanel'
    },
    {
        target: '#leftPanel',
        position: 'right',
        message: "This **AI Tutor panel** on the left teaches you prompting strategies. Each lesson builds on the previous one - follow along step by step! 📚",
        highlight: '#leftPanel'
    },
    {
        target: '.submodule-tabs',
        position: 'bottom',
        message: "The course has **4 progressive lessons**:\n\n1️⃣ Document Analysis\n2️⃣ Content Generation\n3️⃣ Refinement & Polish\n4️⃣ Code Generation & Preview",
        highlight: '.submodule-tabs-container'
    },
    {
        target: '#rightPanel',
        position: 'left',
        message: "This is your **Workspace** - where the magic happens! You'll interact with AI, upload documents, and build your presentation here. ✨",
        highlight: '#rightPanel'
    },
    {
        target: '#uploadSection',
        position: 'top',
        message: "**Step 1:** Start by uploading a document (PDF, TXT, DOCX) or try a sample. This is the content we'll transform into slides! 📄",
        highlight: '#uploadSection'
    },
    {
        target: '#promptInput',
        position: 'top',
        message: "**Step 2:** Write your prompts here! The AI Tutor will teach you how to craft effective prompts. Be specific about what you want! 💬",
        highlight: '.prompt-input-section'
    },
    {
        target: '.generate-button',
        position: 'left',
        message: "**Step 3:** Hit this button to send your prompt! The AI will generate content based on your instructions. Watch the magic unfold! 🚀",
        highlight: '.generate-button'
    },
    {
        target: '#workspaceChat',
        position: 'top',
        message: "Results appear here in **real-time**! You'll see AI responses stream in as they're generated. This is where your presentation takes shape! 📊",
        highlight: '#workspaceChat'
    },
    {
        target: '.embedded-preview',
        position: 'top',
        message: "When you generate HTML/CSS code, it appears in this **Live Preview** window! See your presentation come to life instantly! 📺",
        highlight: '.embedded-preview'
    },
    {
        target: '#chatInput',
        position: 'top',
        message: "Have questions while learning? Use this chat to ask the AI Tutor anything! I'm here to help you master prompt engineering. 🤔",
        highlight: '.chat-input-container'
    },
    {
        target: null,
        position: 'center',
        message: "🎯 **Pro Tips for Success:**\n\n✅ Be specific in your prompts\n✅ Set clear constraints (word count, style)\n✅ Iterate and refine your results\n✅ Complete lessons in order\n✅ Experiment and have fun!\n\nReady to create amazing presentations? Let's go! 🚀",
        highlight: null
    }
];

const generalTutorialSteps = [
    {
        target: '#leftPanel .panel-header',
        position: 'right',
        message: "👋 **Welcome!** I'm your AI learning companion. This is the **AI Tutor** - your personal guide for mastering prompt engineering!",
        highlight: '#leftPanel'
    },
    {
        target: '#rightPanel .panel-header',
        position: 'left',
        message: "This is your **Workspace**. Here you'll practice prompting and see real-time AI responses! 🚀",
        highlight: '#rightPanel'
    },
    {
        target: '#chatInput',
        position: 'top',
        message: "Got questions? Just type here to chat with the AI Tutor. I'm here to help you learn! 💬",
        highlight: '.chat-input-container'
    },
    {
        target: null,
        position: 'center',
        message: "🎯 **Pro Tip:** The better your prompts, the better the results! Be specific, set constraints, and iterate. Ready to start learning? Let's go! 🚀",
        highlight: null
    }
];

// Export for use in tutorial_bot.js
if (typeof window !== 'undefined') {
    window.presentationTutorialSteps = presentationTutorialSteps;
    window.generalTutorialSteps = generalTutorialSteps;
}
