"""
Comprehensive Prompt Engineering Curriculum
"""
from typing import List, Dict, Any


FULL_CURRICULUM = [
    {
        "id": "foundations",
        "title": "Foundations of Prompting",
        "description": "Master the fundamentals of prompt engineering and prevent AI hallucination",
        "submodules": [
            {
                "id": 1,
                "title": "Focused Summarization",
                "description": "Learn to constrain AI outputs and prevent hallucination",
                "welcome_message": "Welcome to your first lesson! We're going to learn how to get an AI to write a summary without it making up facts.",
                "upload_prompt": "First, choose to use our sample document or upload your own on the right panel.",
                "prompt_guidance": "Great! Now, your goal is to summarize it. Try typing a prompt in the text box below the workspace.",
                "weak_prompt_tip": "Remember, we want to constrain the AI. A simple 'summarize' prompt might cause it to add external info. Try adding a rule, like '<strong>Based only on the text provided</strong>' or '<strong>Do not use any external knowledge</strong>'.",
                "success_message": "Fantastic! See the difference? Your prompt gave the AI clear rules and constraints. That's the core skill of prompting!",
                "retry_message": "Good start! To make it even better and prevent any potential 'hallucination' (adding external facts), try adding a constraint like '<strong>Based only on the text provided</strong>' to your prompt.",
                "quiz": {
                    "question": "Why did we add that constraint to our prompt?",
                    "options": [
                        "To make the AI work faster",
                        "To prevent 'hallucination' (making up facts)",
                        "To make the summary longer",
                        "To make the AI sound smarter"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 2,
                "title": "Role Assignment",
                "description": "Learn to assign specific roles to AI for better outputs",
                "welcome_message": "In this lesson, you'll discover how assigning a specific role to AI dramatically improves response quality.",
                "upload_prompt": "Upload a document that you'd like analyzed from a specific perspective.",
                "prompt_guidance": "Try creating a prompt that assigns a role to the AI. For example: '<strong>You are an expert [profession]...</strong>'",
                "weak_prompt_tip": "Consider starting with a role assignment. Try: '<strong>You are a [specific expert]. Analyze this document and...</strong>'",
                "success_message": "Excellent! By assigning a role, you gave the AI context about what perspective and expertise to use.",
                "retry_message": "Good attempt! To improve, try explicitly stating what role the AI should take (e.g., 'You are a technical reviewer...').",
                "quiz": {
                    "question": "What's the main benefit of role assignment in prompts?",
                    "options": [
                        "It makes the AI respond faster",
                        "It provides context and expertise perspective",
                        "It reduces token usage",
                        "It makes responses shorter"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 3,
                "title": "Chain-of-Thought Reasoning",
                "description": "Guide AI through step-by-step reasoning processes",
                "welcome_message": "Let's learn how to make AI 'think' through problems step by step, improving accuracy dramatically.",
                "upload_prompt": "Upload a document with complex information or a problem to analyze.",
                "prompt_guidance": "Ask the AI to break down its analysis into steps. Use phrases like '<strong>Let's think step by step</strong>' or '<strong>First, analyze... Then, conclude...</strong>'",
                "weak_prompt_tip": "Try adding '<strong>Let's think step by step</strong>' or '<strong>Break this down into steps</strong>' to your prompt.",
                "success_message": "Perfect! By requesting step-by-step reasoning, you got a more thorough and accurate analysis.",
                "retry_message": "Good start! To enhance reasoning, explicitly ask the AI to think through the problem step by step.",
                "quiz": {
                    "question": "Why does chain-of-thought prompting improve AI accuracy?",
                    "options": [
                        "It forces the AI to use more tokens",
                        "It breaks complex reasoning into manageable steps",
                        "It makes the AI work slower",
                        "It requires less computation"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 4,
                "title": "Real-world Practice",
                "description": "Apply all foundation techniques to complex scenarios",
                "welcome_message": "Time to combine everything! This lesson requires using constraints, role assignment, AND step-by-step reasoning.",
                "upload_prompt": "Upload a complex document that needs comprehensive analysis.",
                "prompt_guidance": "Create a comprehensive prompt using: 1) Role assignment, 2) Constraints, 3) Step-by-step instructions.",
                "weak_prompt_tip": "A strong prompt combines multiple techniques. Have you included: a role, constraints, and step-by-step guidance?",
                "success_message": "Outstanding! You've mastered the foundations by combining multiple prompting techniques effectively.",
                "retry_message": "You're on the right track! Try incorporating all three techniques: role, constraints, and structured reasoning.",
                "quiz": {
                    "question": "What makes a comprehensive prompt effective?",
                    "options": [
                        "Using as few words as possible",
                        "Combining role, constraints, and structure",
                        "Making it as long as possible",
                        "Using technical jargon"
                    ],
                    "correct_index": 1
                },
                "completed": False
            }
        ]
    },
    {
        "id": "advanced-patterns",
        "title": "Advanced Prompting Patterns",
        "description": "Master sophisticated prompting techniques for complex tasks",
        "submodules": [
            {
                "id": 1,
                "title": "Few-Shot Learning",
                "description": "Teach AI through examples for consistent outputs",
                "welcome_message": "Learn to teach AI through examples - one of the most powerful prompting techniques!",
                "upload_prompt": "Upload a document you want formatted or analyzed in a specific way.",
                "prompt_guidance": "Provide 2-3 examples of the desired output format before asking the AI to process your document.",
                "weak_prompt_tip": "Few-shot learning works best with clear examples. Show the AI what you want by providing sample inputs and outputs.",
                "success_message": "Brilliant! Examples are incredibly effective for teaching AI specific patterns and formats.",
                "retry_message": "Try including concrete examples that demonstrate the exact format or style you want.",
                "quiz": {
                    "question": "When is few-shot learning most valuable?",
                    "options": [
                        "When you want the AI to work faster",
                        "When you need consistent formatting or specific patterns",
                        "When you have very little data",
                        "When you want shorter responses"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 2,
                "title": "Output Formatting",
                "description": "Control AI output structure with precise formatting instructions",
                "welcome_message": "Learn to control exactly how AI structures its responses - JSON, tables, bullet points, and more.",
                "upload_prompt": "Upload data that needs to be restructured or formatted.",
                "prompt_guidance": "Specify the exact output format you need. Examples: '<strong>Format as JSON</strong>', '<strong>Create a table with columns...</strong>', '<strong>Use bullet points for...</strong>'",
                "weak_prompt_tip": "Be explicit about format! Try: '<strong>Output as a JSON object with keys...</strong>' or '<strong>Format as a markdown table with...</strong>'",
                "success_message": "Excellent! Precise formatting instructions ensure AI outputs are immediately usable.",
                "retry_message": "Good attempt! Be more specific about the structure - what format do you need? (JSON, table, list, etc.)",
                "quiz": {
                    "question": "Why is explicit output formatting important?",
                    "options": [
                        "It makes responses prettier",
                        "It ensures outputs are structured and immediately usable",
                        "It reduces processing time",
                        "It makes prompts shorter"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 3,
                "title": "Prompt Chaining",
                "description": "Break complex tasks into sequential prompts",
                "welcome_message": "Master the art of breaking down complex tasks into a chain of simpler, connected prompts.",
                "upload_prompt": "Upload a document requiring multi-stage analysis (e.g., summary, then sentiment, then recommendations).",
                "prompt_guidance": "Design a sequence: First prompt extracts info, second analyzes it, third generates recommendations based on analysis.",
                "weak_prompt_tip": "Complex tasks benefit from chaining. Try: '<strong>First, extract key points. Then, I'll ask you to analyze them.</strong>'",
                "success_message": "Perfect! Chaining prompts produces more accurate results than trying to do everything at once.",
                "retry_message": "Consider breaking this into stages. What should the AI do first, second, and third?",
                "quiz": {
                    "question": "What's the key advantage of prompt chaining?",
                    "options": [
                        "It's faster than single prompts",
                        "It breaks complexity into manageable, focused steps",
                        "It uses fewer tokens",
                        "It requires less planning"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 4,
                "title": "Constraint Engineering",
                "description": "Master advanced constraint techniques for precise control",
                "welcome_message": "Learn sophisticated constraint techniques to precisely control AI behavior and outputs.",
                "upload_prompt": "Upload a document requiring highly constrained analysis.",
                "prompt_guidance": "Use multiple constraint types: length limits, prohibited content, required elements, tone/style requirements.",
                "weak_prompt_tip": "Advanced constraints might include: '<strong>Limit to 100 words</strong>', '<strong>Avoid technical jargon</strong>', '<strong>Include at least 3 examples</strong>'",
                "success_message": "Outstanding! Multi-layered constraints give you surgical precision over AI outputs.",
                "retry_message": "Try adding more specific constraints about what to include, exclude, and how to structure the response.",
                "quiz": {
                    "question": "What makes constraint engineering 'advanced'?",
                    "options": [
                        "Using longer constraints",
                        "Combining multiple constraint types for precise control",
                        "Making constraints as restrictive as possible",
                        "Avoiding constraints altogether"
                    ],
                    "correct_index": 1
                },
                "completed": False
            }
        ]
    },
    {
        "id": "domain-specific",
        "title": "Domain-Specific Prompting",
        "description": "Apply prompting techniques to specific professional domains",
        "submodules": [
            {
                "id": 1,
                "title": "Technical Documentation",
                "description": "Generate and analyze technical documentation effectively",
                "welcome_message": "Learn to prompt AI for technical writing - clear, accurate, and properly structured documentation.",
                "upload_prompt": "Upload technical content that needs documentation or analysis.",
                "prompt_guidance": "Technical prompts need: audience specification, technical depth level, and formatting standards.",
                "weak_prompt_tip": "For technical docs, specify: '<strong>Write for [audience]</strong>', '<strong>Technical level: [beginner/intermediate/advanced]</strong>', '<strong>Include code examples</strong>'",
                "success_message": "Excellent! Well-prompted technical documentation is clear, accurate, and appropriately detailed.",
                "retry_message": "Consider specifying the target audience and technical depth you need.",
                "quiz": {
                    "question": "What's crucial for technical documentation prompts?",
                    "options": [
                        "Using complex technical jargon",
                        "Specifying audience and technical depth",
                        "Making prompts as short as possible",
                        "Avoiding code examples"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 2,
                "title": "Business Analysis",
                "description": "Extract business insights and create strategic analyses",
                "welcome_message": "Master prompting for business contexts - insights, recommendations, and strategic thinking.",
                "upload_prompt": "Upload business-related content (reports, data, proposals).",
                "prompt_guidance": "Business prompts should include: business context, stakeholder perspective, and decision-making focus.",
                "weak_prompt_tip": "Business analysis benefits from: '<strong>Consider [stakeholder] perspective</strong>', '<strong>Focus on actionable insights</strong>', '<strong>Include ROI/impact</strong>'",
                "success_message": "Great! Business-focused prompts produce actionable, stakeholder-relevant insights.",
                "retry_message": "Try adding business context and specifying what decisions this analysis should inform.",
                "quiz": {
                    "question": "What makes business analysis prompts effective?",
                    "options": [
                        "Using business buzzwords",
                        "Including context, stakeholders, and decision focus",
                        "Keeping analysis purely objective",
                        "Avoiding specific recommendations"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 3,
                "title": "Creative Content",
                "description": "Generate creative, engaging content with AI",
                "welcome_message": "Learn to prompt AI for creativity while maintaining quality and brand consistency.",
                "upload_prompt": "Upload content briefs, brand guidelines, or reference materials.",
                "prompt_guidance": "Creative prompts need: tone/style specification, audience description, and creative constraints.",
                "weak_prompt_tip": "For creative content, try: '<strong>Tone: [playful/professional/inspiring]</strong>', '<strong>Target audience: [specific group]</strong>', '<strong>Brand voice: [description]</strong>'",
                "success_message": "Perfect! Balancing creativity with constraints produces engaging, on-brand content.",
                "retry_message": "Consider adding more detail about tone, audience, and creative direction.",
                "quiz": {
                    "question": "Why are constraints important in creative prompts?",
                    "options": [
                        "They limit AI creativity",
                        "They channel creativity toward specific goals and brand consistency",
                        "They make responses shorter",
                        "They're not important for creative work"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 4,
                "title": "Data Analysis",
                "description": "Analyze and interpret data using AI effectively",
                "welcome_message": "Master prompting for data analysis - insights, patterns, and statistical reasoning.",
                "upload_prompt": "Upload datasets, statistical reports, or data that needs interpretation.",
                "prompt_guidance": "Data analysis prompts should specify: analysis type, metrics of interest, and interpretation depth.",
                "weak_prompt_tip": "For data analysis, include: '<strong>Identify trends in [specific metric]</strong>', '<strong>Compare [A] vs [B]</strong>', '<strong>Explain statistical significance</strong>'",
                "success_message": "Excellent! Well-crafted data prompts extract meaningful insights and actionable patterns.",
                "retry_message": "Try being more specific about what metrics, patterns, or comparisons you want analyzed.",
                "quiz": {
                    "question": "What's essential for effective data analysis prompts?",
                    "options": [
                        "Using complex statistical terminology",
                        "Specifying analysis type, metrics, and desired insights",
                        "Keeping prompts very short",
                        "Avoiding interpretation"
                    ],
                    "correct_index": 1
                },
                "completed": False
            }
        ]
    },
    {
        "id": "advanced-techniques",
        "title": "Advanced AI Techniques",
        "description": "Master cutting-edge prompting strategies and optimization",
        "submodules": [
            {
                "id": 1,
                "title": "Meta-Prompting",
                "description": "Have AI generate and refine its own prompts",
                "welcome_message": "Discover meta-prompting - using AI to create better prompts for itself!",
                "upload_prompt": "Upload a complex document or task description.",
                "prompt_guidance": "Ask AI to first analyze the task and generate an optimal prompt for it, then execute that prompt.",
                "weak_prompt_tip": "Meta-prompting: '<strong>First, create the best possible prompt to [task]. Then execute that prompt.</strong>'",
                "success_message": "Brilliant! Meta-prompting leverages AI's understanding to optimize its own instructions.",
                "retry_message": "Try asking the AI to design the prompt first, then execute it.",
                "quiz": {
                    "question": "What's the power of meta-prompting?",
                    "options": [
                        "It's faster than regular prompting",
                        "AI optimizes its own instructions based on task understanding",
                        "It uses fewer tokens",
                        "It avoids needing examples"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 2,
                "title": "Prompt Optimization",
                "description": "Systematically improve prompt effectiveness",
                "welcome_message": "Learn to iteratively refine prompts for optimal results through systematic testing.",
                "upload_prompt": "Upload content for analysis with multiple prompting approaches.",
                "prompt_guidance": "Test variations: different role assignments, constraint combinations, and structural approaches.",
                "weak_prompt_tip": "Optimization involves A/B testing different approaches. Try multiple versions and compare results.",
                "success_message": "Perfect! Systematic optimization turns good prompts into great ones.",
                "retry_message": "Consider testing alternative formulations and comparing their effectiveness.",
                "quiz": {
                    "question": "What's key to prompt optimization?",
                    "options": [
                        "Making prompts as long as possible",
                        "Systematic testing and comparison of variations",
                        "Using the same prompt for everything",
                        "Avoiding iteration"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 3,
                "title": "Context Management",
                "description": "Effectively manage conversation context and memory",
                "welcome_message": "Master managing AI context across multi-turn conversations for consistency.",
                "upload_prompt": "Upload related documents that require contextual awareness.",
                "prompt_guidance": "Maintain context by referencing previous information and building on established understanding.",
                "weak_prompt_tip": "Context management: '<strong>Based on our previous discussion about [topic]...</strong>' or '<strong>Referring to the earlier analysis...</strong>'",
                "success_message": "Excellent! Effective context management maintains coherence across complex interactions.",
                "retry_message": "Try explicitly referencing and building on previous context in your prompt.",
                "quiz": {
                    "question": "Why is context management important?",
                    "options": [
                        "It makes individual prompts shorter",
                        "It maintains coherence and consistency across interactions",
                        "It reduces the need for examples",
                        "It makes AI work faster"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 4,
                "title": "Error Handling & Recovery",
                "description": "Design prompts that anticipate and handle errors gracefully",
                "welcome_message": "Learn to build robust prompts that handle edge cases and ambiguous inputs.",
                "upload_prompt": "Upload potentially ambiguous or incomplete documents.",
                "prompt_guidance": "Include fallback instructions: what to do if info is missing, unclear, or contradictory.",
                "weak_prompt_tip": "Robust prompts include: '<strong>If information is unclear, explain what's missing</strong>' or '<strong>If data contradicts, note the discrepancy</strong>'",
                "success_message": "Outstanding! Anticipating errors makes prompts production-ready and reliable.",
                "retry_message": "Consider adding instructions for handling missing or ambiguous information.",
                "quiz": {
                    "question": "Why include error handling in prompts?",
                    "options": [
                        "To make prompts longer",
                        "To ensure reliable, production-ready behavior with imperfect inputs",
                        "To make AI work slower",
                        "To avoid using AI altogether"
                    ],
                    "correct_index": 1
                },
                "completed": False
            }
        ]
    },
    {
        "id": "presentation-builder",
        "title": "AI-Powered Presentation Builder",
        "description": "Learn to prompt AI to create professional HTML/CSS presentations from documents",
        "submodules": [
            {
                "id": 1,
                "title": "Document Analysis & Information Extraction",
                "description": "Master prompting techniques to extract structured information from documents",
                "welcome_message": "Welcome to the Presentation Builder! In this module, you'll learn to transform any document into a beautiful HTML/CSS presentation. Let's start by learning how to extract key information from documents using smart prompts.",
                "upload_prompt": "Upload a document you want to convert into a presentation. It could be a report, article, or any text-based content (PDF, DOCX, or TXT).",
                "prompt_guidance": "Now, let's extract the key information. Try prompting the AI to identify: <strong>main topics, key points, supporting details, and structure</strong>. Example: 'Analyze this document and extract the main sections with their key points in a structured format.'",
                "weak_prompt_tip": "For better extraction, be specific! Try: '<strong>Extract from this document: 1) Main title/topic, 2) 3-5 key sections with headings, 3) 2-3 bullet points per section, 4) Any important data or quotes</strong>'",
                "success_message": "Excellent! You've successfully extracted structured information. Notice how being specific about what you want (sections, points, format) gives you organized output perfect for slides!",
                "retry_message": "Good start! To get better structured data for slides, try asking for: specific number of sections, bullet points per section, and clear formatting.",
                "quiz": {
                    "question": "Why is structured extraction important for presentation creation?",
                    "options": [
                        "It makes the AI work faster",
                        "It organizes content into slide-ready sections and points",
                        "It reduces the document size",
                        "It removes unnecessary information"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 2,
                "title": "Content Generation for Slides",
                "description": "Master the art of prompting AI to create engaging, presentation-ready slide content",
                "welcome_message": "Welcome to Lesson 2! Now that you can extract information, let's learn the critical skill of **generating actual slide content**. You'll discover how to prompt AI to create titles, bullet points, and descriptions that work perfectly in presentations. The key is being specific about structure and constraints!",
                "upload_prompt": "Upload a document you want to transform into slide content. This could be a report, article, research paper, or any content-rich document (PDF, DOCX, or TXT).",
                "prompt_guidance": "Now, let's generate slide content! Try prompting the AI with this structure: '<strong>Create presentation slide content from this document. Generate 5-7 slides, each with: 1) A compelling title (max 8 words), 2) 3-4 bullet points (each under 15 words), 3) A brief explanation (2-3 sentences). Make it engaging and easy to present.</strong>'",
                "weak_prompt_tip": "🎯 **Pro Tips for Better Slide Content:**\n\n• **Specify exact numbers**: 'Create 6 slides' instead of 'several slides'\n• **Set length constraints**: 'titles under 8 words', 'bullets under 15 words'\n• **Define the format**: What should each slide contain?\n• **Add style guidelines**: 'professional tone', 'action-oriented bullets', 'include real examples'\n• **Request variety**: 'use different slide types: overview, key points, comparison, conclusion'\n\n**Example Strong Prompt:**\n'<strong>Based on this document, create 6 presentation slides:\n- Slide 1: Title slide (main topic + subtitle)\n- Slides 2-5: Content slides (catchy title + 3 bullet points + key insight)\n- Slide 6: Summary/Call-to-action\nKeep titles under 8 words, bullets under 15 words. Use active voice and include specific data/examples from the document.</strong>'",
                "success_message": "🎉 **Excellent work!** You've generated presentation-ready content! Notice how being specific about:\n• **Structure** (title + bullets + notes)\n• **Quantities** (exact number of slides and points)\n• **Constraints** (word limits)\n• **Style** (engaging, action-oriented)\n\n...created content that fits perfectly into slides! This is the foundation of AI-powered presentation creation.",
                "retry_message": "Good start! To generate professional slide content, make sure your prompt includes:\n✓ Exact number of slides wanted\n✓ What each slide should contain (title, bullets, notes)\n✓ Length constraints (word limits for titles and bullets)\n✓ Style preferences (professional, conversational, technical)\n\nTry again with these elements!",
                "quiz": {
                    "question": "What's the MOST important factor when prompting AI to generate slide content?",
                    "options": [
                        "Using complex technical language",
                        "Asking for as much text as possible",
                        "Specifying clear structure, format, and length constraints",
                        "Letting AI decide everything for maximum creativity"
                    ],
                    "correct_index": 2
                },
                "completed": False
            },
            {
                "id": 3,
                "title": "Content Refinement & Polish",
                "description": "Master the iterative process of refining AI-generated slide content for perfection",
                "welcome_message": "🎨 Welcome to Lesson 3! Now you have slide content from Lesson 2, but **great presentations are never created in one shot**. In this lesson, you'll learn the critical skill of **refining and polishing** your content through targeted prompts. You'll discover how to make specific improvements, validate accuracy, and ensure your slides tell a compelling story!",
                "upload_prompt": "Continue with the same document from Lesson 2, or upload a new document if you want to start fresh with different content.",
                "prompt_guidance": "Time to refine! Look at your generated content and prompt the AI to improve it. Try: '<strong>Review and refine the slide content:\n1) Make slide titles more compelling and action-oriented\n2) Ensure each bullet point is under 12 words and starts with a strong verb\n3) Add specific examples or data from the document where possible\n4) Verify all information is accurate to the source document\n5) Ensure logical flow from one slide to the next</strong>'",
                "weak_prompt_tip": "🎯 **Refinement Prompting Strategies:**\n\n**For Better Clarity:**\n'<strong>Simplify slide 2: Replace technical jargon with plain language, make bullets more concrete</strong>'\n\n**For Better Engagement:**\n'<strong>Make slide 3 more compelling: Add a powerful statistic from the document, use active voice, create urgency</strong>'\n\n**For Better Flow:**\n'<strong>Improve transitions: Add a connecting phrase at the end of slide 2 that leads into slide 3, ensure narrative continuity</strong>'\n\n**For Better Accuracy:**\n'<strong>Validate slide 4: Check all facts against the source document, replace general statements with specific data points, cite exact figures</strong>'\n\n**For Better Impact:**\n'<strong>Enhance slide 5: Move the strongest point to the top, add a real-world example, make the call-to-action clearer</strong>'\n\n**Pro Tip:** Be specific about WHICH slide, WHICH element, and WHAT to change!",
                "success_message": "🌟 **Brilliant refinement!** You've mastered the art of iterative improvement! Notice how your targeted, specific prompts transformed good content into **great content**. You learned to:\n\n✓ **Target specific elements** (titles, bullets, data)\n✓ **Apply clear criteria** (word count, accuracy, impact)\n✓ **Validate against source** (ensuring accuracy)\n✓ **Improve narrative flow** (transitions, story arc)\n✓ **Enhance engagement** (stronger verbs, compelling examples)\n\nThis iterative refinement is what separates amateur presentations from professional ones!",
                "retry_message": "Good attempt at refinement! To make your improvements more effective, try being more specific:\n\n❌ Avoid: 'Make it better'\n✅ Instead: 'Shorten bullet 2 on slide 3 to 10 words and add a percentage from the document'\n\n❌ Avoid: 'Improve the flow'\n✅ Instead: 'Add a transition sentence at the end of slide 2 that introduces the concept in slide 3'\n\n❌ Avoid: 'Make it more interesting'\n✅ Instead: 'Replace the generic example with the specific case study mentioned in paragraph 4 of the document'\n\nBe precise about WHAT to change and HOW to change it!",
                "quiz": {
                    "question": "What's the key to effective content refinement prompting?",
                    "options": [
                        "Asking AI to 'make it better' without specifics",
                        "Targeting specific slides/elements with clear, actionable changes",
                        "Completely regenerating all content from scratch",
                        "Accepting the first output without iteration"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 4,
                "title": "HTML/CSS Code Generation & Preview",
                "description": "Master prompting AI to generate complete, working presentation code with live preview",
                "welcome_message": "🚀 Welcome to the final lesson - **Code Generation**! This is where everything comes together. You'll learn to prompt the AI to transform your refined content into **complete, working HTML/CSS presentation code**. The best part? You'll see your presentation come to life in the **live preview window** below! This lesson teaches you to be specific about structure, styling, interactivity, and user experience.",
                "upload_prompt": "Continue with the same document and refined content from previous lessons, or upload a new document to create a fresh presentation.",
                "prompt_guidance": "Time to generate the code! Prompt the AI to create a complete HTML/CSS presentation. Try: '<strong>Generate a complete HTML/CSS presentation with the following specifications:\n\n**Structure:**\n- Full-screen slides with centered content\n- Clear navigation (Previous/Next buttons + slide numbers)\n- Progress indicator\n\n**Styling:**\n- Modern, clean design with a professional color scheme\n- Readable typography (titles: 2.5rem, body: 1.2rem)\n- Consistent spacing and alignment\n- Smooth fade transitions between slides\n\n**Interactivity:**\n- Click navigation buttons to move between slides\n- Keyboard controls (arrow keys, space bar)\n- Responsive for different screen sizes\n\n**Content:**\nInclude all the refined slide content we created (titles, bullet points, etc.)\n\nOutput the complete HTML with embedded CSS in <style> tags and JavaScript in <script> tags. Make it ready to run in a browser.</strong>'",
                "weak_prompt_tip": "💡 **Pro Tips for Code Generation:**\n\n**Be Specific About Structure:**\n'<strong>Create a single HTML file with: 1) DOCTYPE and proper HTML5 structure, 2) Each slide in a <section class=\"slide\"> element, 3) Navigation container with prev/next buttons, 4) Current slide indicator</strong>'\n\n**Define the Visual Design:**\n'<strong>CSS requirements: 1) Full viewport height slides, 2) Flexbox centered content, 3) Color scheme: dark background (#1a1a1a) with red accents (#ef4444), 4) Font: system sans-serif, 5) Smooth 0.5s transitions, 6) Hidden slides with opacity 0</strong>'\n\n**Specify Interactions:**\n'<strong>JavaScript functionality: 1) Show only current slide (others hidden), 2) Next/Prev button handlers, 3) Keyboard navigation (ArrowLeft, ArrowRight, Space), 4) Update slide counter (e.g., \"3 / 7\"), 5) Disable Prev on first slide, Next on last slide</strong>'\n\n**Request Complete Code:**\n'<strong>Output: Single self-contained HTML file with all CSS and JavaScript inline. No external dependencies. Ready to save as .html and open in any browser.</strong>'\n\n**Example Complete Prompt:**\n'<strong>Create a complete presentation from the refined content:\n\nHTML Structure: <!DOCTYPE html>, full HTML5 boilerplate, multiple <section class=\"slide\"> elements\nCSS: Embedded in <style>, fullscreen slides, modern design, smooth transitions  \nJavaScript: Embedded in <script>, navigation logic, keyboard controls\nDesign: Dark theme, red accents, professional typography, responsive\nFeatures: Next/Prev buttons, slide counter, keyboard navigation, smooth animations\n\nMake it production-ready and fully functional. Output the complete code.</strong>'",
                "success_message": "🎉 **AMAZING WORK!** You've successfully generated a **complete, working presentation**! \n\n✨ **Look at the preview window below** - your presentation is now live and interactive!\n\n**What You Accomplished:**\n✓ Generated semantic HTML structure for multiple slides\n✓ Created professional CSS styling with your design specifications\n✓ Implemented JavaScript for navigation and interactivity\n✓ Made it responsive and production-ready\n\n**Why It Worked:**\nYou were specific about:\n- Structure (HTML elements, classes)\n- Design (colors, fonts, layout)\n- Functionality (navigation, keyboard controls)\n- Output format (self-contained, ready to run)\n\nThis is the power of precise prompting! You can now create professional presentations from any document using AI. 🚀",
                "retry_message": "Good attempt! To generate production-ready code that appears in the preview, make sure your prompt includes:\n\n✓ **Complete structure** - HTML boilerplate, slide sections, navigation\n✓ **Embedded styling** - CSS in <style> tags, all design specifications\n✓ **Full interactivity** - JavaScript in <script> tags for navigation\n✓ **Self-contained** - No external files, everything inline\n✓ **Specific design** - Colors, fonts, spacing, transitions\n✓ **Ready to run** - Works when copied directly to a .html file\n\nThe more specific you are about technical requirements, the better the generated code!",
                "quiz": {
                    "question": "What's the most critical factor for generating working presentation code?",
                    "options": [
                        "Asking for the longest code possible",
                        "Specifying structure, styling, interactivity, and output format clearly",
                        "Using technical jargon to sound professional",
                        "Requesting separate HTML, CSS, and JS files"
                    ],
                    "correct_index": 1
                },
                "completed": False
            }
        ]
    }
]


def get_curriculum() -> List[Dict[str, Any]]:
    """Get the complete curriculum structure"""
    return FULL_CURRICULUM


def get_module(module_id: str) -> Dict[str, Any] | None:
    """Get a specific module by ID"""
    for module in FULL_CURRICULUM:
        if module["id"] == module_id:
            return module
    return None


def get_submodule(module_id: str, submodule_id: int) -> Dict[str, Any] | None:
    """Get a specific submodule"""
    module = get_module(module_id)
    if not module:
        return None
    
    for submodule in module["submodules"]:
        if submodule["id"] == submodule_id:
            return submodule
    return None
