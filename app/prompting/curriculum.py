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
