"""
Module Descriptions for Introductory Dialog
Contains detailed descriptions for each module to display when module pages are opened
"""

MODULE_DESCRIPTIONS = {
    "foundations": {
        "id": "foundations",
        "number": 1,
        "title": "Foundations of Prompting",
        "description": """<p>Master the fundamentals of prompt engineering and prevent AI hallucination.</p>
<p>This foundational module teaches you essential techniques for effective AI communication:</p>
<ul>
<li><strong>Focused Summarization</strong> - Learn to constrain AI outputs and prevent hallucination by grounding responses in provided context</li>
<li><strong>Role Assignment</strong> - Discover how assigning specific roles to AI dramatically improves response quality and expertise</li>
<li><strong>Chain-of-Thought Reasoning</strong> - Guide AI through step-by-step reasoning processes for more accurate and thorough analysis</li>
<li><strong>Real-world Practice</strong> - Apply all foundation techniques together to complex scenarios and master comprehensive prompting</li>
</ul>
<p>By the end of this module, you'll understand how to write clear, effective prompts that produce reliable, accurate AI outputs.</p>""",
        "video_available": False
    },

    "advanced-patterns": {
        "id": "advanced-patterns",
        "number": 2,
        "title": "Advanced Prompting Patterns",
        "description": """<p>Master sophisticated prompting techniques for complex tasks.</p>
<p>This module builds on the foundations to teach advanced strategies:</p>
<ul>
<li><strong>Few-Shot Learning</strong> - Teach AI through examples for consistent, high-quality outputs that match your specific requirements</li>
<li><strong>Output Formatting</strong> - Control AI output structure with precise formatting instructions (JSON, tables, markdown, and more)</li>
<li><strong>Prompt Chaining</strong> - Break complex tasks into sequential prompts for better accuracy and manageable complexity</li>
<li><strong>Constraint Engineering</strong> - Master advanced constraint techniques using multiple constraint types for surgical precision over AI behavior</li>
</ul>
<p>These patterns enable you to handle sophisticated workflows and achieve production-ready results.</p>""",
        "video_available": False
    },

    "domain-specific": {
        "id": "domain-specific",
        "number": 3,
        "title": "Domain-Specific Prompting",
        "description": """<p>Apply prompting techniques to specific professional domains.</p>
<p>Learn to tailor your prompts for different professional contexts:</p>
<ul>
<li><strong>Technical Documentation</strong> - Generate and analyze technical documentation with appropriate depth, audience targeting, and formatting standards</li>
<li><strong>Business Analysis</strong> - Extract business insights and create strategic analyses that inform decision-making and consider stakeholder perspectives</li>
<li><strong>Creative Content</strong> - Generate creative, engaging content while maintaining quality, brand consistency, and target audience alignment</li>
<li><strong>Data Analysis</strong> - Analyze and interpret data using AI to identify trends, patterns, and extract actionable insights</li>
</ul>
<p>Each lesson teaches domain-specific best practices and considerations for professional-quality outputs.</p>""",
        "video_available": False
    },

    "advanced-techniques": {
        "id": "advanced-techniques",
        "number": 4,
        "title": "Advanced AI Techniques",
        "description": """<p>Master cutting-edge prompting strategies and optimization techniques.</p>
<p>Discover advanced methods for prompt engineering excellence:</p>
<ul>
<li><strong>Meta-Prompting</strong> - Have AI generate and refine its own prompts by leveraging its understanding to optimize instructions</li>
<li><strong>Prompt Optimization</strong> - Systematically improve prompt effectiveness through A/B testing and iterative refinement</li>
<li><strong>Context Management</strong> - Effectively manage conversation context and memory for coherent, consistent multi-turn interactions</li>
<li><strong>Error Handling & Recovery</strong> - Design robust prompts that anticipate and handle errors, edge cases, and ambiguous inputs gracefully</li>
</ul>
<p>These techniques make your prompts production-ready and reliable for real-world applications.</p>""",
        "video_available": False
    },

    "presentation-builder": {
        "id": "presentation-builder",
        "number": 5,
        "title": "AI-Powered Presentation Builder",
        "description": """<p>Learn to prompt AI to create professional HTML/CSS presentations from documents.</p>
<p>Transform any document into beautiful, interactive presentations:</p>
<ul>
<li><strong>Document Analysis & Information Extraction</strong> - Master prompting techniques to extract structured information from documents for slide-ready content</li>
<li><strong>Content Generation for Slides</strong> - Learn the critical skill of generating engaging, presentation-ready slide content with specific structure and constraints</li>
<li><strong>Content Refinement & Polish</strong> - Master the iterative process of refining AI-generated content through targeted, specific improvement prompts</li>
<li><strong>HTML/CSS Code Generation & Preview</strong> - Prompt AI to transform refined content into complete, working HTML/CSS presentation code with live preview</li>
</ul>
<p>By the end, you'll be able to create professional presentations from any document using AI-powered prompt engineering.</p>""",
        "video_available": False
    }
}


def get_module_description(module_id: str) -> dict | None:
    """Get description data for a specific module"""
    return MODULE_DESCRIPTIONS.get(module_id)


def get_all_module_descriptions() -> dict:
    """Get all module descriptions"""
    return MODULE_DESCRIPTIONS
