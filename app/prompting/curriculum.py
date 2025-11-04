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
                "description": "Learn to prompt AI to generate presentation-ready content",
                "welcome_message": "Great job on extraction! Now let's learn to prompt the AI to generate actual slide content - titles, descriptions, and talking points for each slide.",
                "upload_prompt": "Upload your document or continue with the previous one.",
                "prompt_guidance": "Now prompt the AI to generate slide content. Try: '<strong>Based on this document, create content for 5-7 presentation slides. For each slide provide: 1) A catchy title, 2) 3-4 concise bullet points, 3) A brief speaker note</strong>'",
                "weak_prompt_tip": "Make your prompt more specific! Include: exact number of slides, format for each slide (title + bullets), length constraints (e.g., 'keep bullets under 15 words'), and any style preferences (professional, casual, technical).",
                "success_message": "Perfect! You've generated presentation-ready content. Notice how specifying the structure (title, bullets, notes) and constraints (number, length) creates content that fits perfectly into slides!",
                "retry_message": "Good attempt! For better slide content, specify: how many slides, what goes on each slide (title/bullets/notes), and any length or style constraints.",
                "quiz": {
                    "question": "What makes a good prompt for slide content generation?",
                    "options": [
                        "Asking for as much detail as possible",
                        "Being vague to let AI be creative",
                        "Specifying structure, format, and constraints clearly",
                        "Only requesting titles without details"
                    ],
                    "correct_index": 2
                },
                "completed": False
            },
            {
                "id": 3,
                "title": "Content Refinement & Validation",
                "description": "Learn to iterate and refine AI-generated content through prompting",
                "welcome_message": "Now let's learn the most important skill: refining AI output! You'll learn to validate content, spot issues, and prompt the AI to make specific improvements.",
                "upload_prompt": "Continue with your previous document or upload a new one.",
                "prompt_guidance": "Review the generated content and prompt for refinements. Try: '<strong>Review slide 3: make the bullets more concise, add a statistic if available in the document, and ensure it flows from slide 2</strong>'",
                "weak_prompt_tip": "For precise refinements, use prompts like: '<strong>For slide [number]: 1) Shorten bullet 2 to under 10 words, 2) Replace generic terms with specific examples from the document, 3) Add a transition phrase connecting to the next slide</strong>'",
                "success_message": "Excellent refinement! You've learned to give specific, actionable feedback. This iterative process ensures your presentation content is accurate, concise, and flows well!",
                "retry_message": "Good refinement attempt! Be more specific about what to change: which slide, which bullet, what exactly to modify, and what the goal is (shorter, more specific, better flow, etc.).",
                "quiz": {
                    "question": "Why is iterative refinement crucial for AI-generated presentations?",
                    "options": [
                        "It makes the process take longer",
                        "It ensures accuracy, conciseness, and proper flow",
                        "It's only needed for technical content",
                        "It's optional if the first output looks good"
                    ],
                    "correct_index": 1
                },
                "completed": False
            },
            {
                "id": 4,
                "title": "HTML/CSS Code Generation",
                "description": "Master prompting AI to generate professional presentation code",
                "welcome_message": "Time for the magic! You'll learn to prompt the AI to convert your refined content into beautiful HTML/CSS presentation code that works right in your browser.",
                "upload_prompt": "Continue with your refined presentation content.",
                "prompt_guidance": "Prompt the AI to generate code. Try: '<strong>Generate HTML and CSS code for a presentation with the following requirements: 1) Clean, modern design with slide navigation, 2) Responsive layout, 3) Smooth transitions between slides, 4) Include all the content we created. Use semantic HTML and modular CSS.</strong>'",
                "weak_prompt_tip": "For better code generation, specify: '<strong>Create an HTML/CSS presentation with: 1) Full-screen slides with centered content, 2) Navigation buttons (prev/next/slide numbers), 3) Smooth fade transitions, 4) Dark theme with accent colors, 5) Mobile-responsive, 6) Include keyboard controls (arrow keys). Output complete code ready to run.</strong>'",
                "success_message": "Outstanding! You've generated a complete presentation! The AI created HTML structure and CSS styling because you specified exactly what features you wanted. Your presentation is now ready to preview!",
                "retry_message": "Good start! For production-ready code, specify: design style, navigation features, transitions, responsiveness, color scheme, and any interactive elements you want.",
                "quiz": {
                    "question": "What makes a code generation prompt effective?",
                    "options": [
                        "Just asking for 'HTML and CSS'",
                        "Specifying features, design, interactions, and technical requirements",
                        "Requesting the most complex code possible",
                        "Avoiding technical details to keep it simple"
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
