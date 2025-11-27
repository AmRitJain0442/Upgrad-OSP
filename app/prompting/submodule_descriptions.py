"""
Comprehensive Submodule Descriptions
Contains detailed information for each submodule to display in intro dialogs
"""

SUBMODULE_DESCRIPTIONS = {
    # Module 1: Foundations of Prompting
    "foundations_1": {
        "module_number": 1,
        "submodule_number": 1,
        "module_title": "Foundations of Prompting",
        "submodule_title": "Focused Summarization",
        "description": "Learn how to prevent AI from making up facts or adding external information. You'll master the technique of constraining AI outputs using phrases like 'based only on the text provided' to eliminate hallucination and keep responses grounded in your source material.",
        "key_learning": "How to use constraints to prevent AI from adding external knowledge or fabricated information",
        "why_important": "Without proper constraints, AI can confidently state incorrect facts or add information from its training data. This technique ensures your AI outputs are accurate and trustworthy.",
        "real_world_use": "Use this when summarizing documents, reports, or data where accuracy is critical - like legal documents, medical records, or financial reports where every fact must come from the source."
    },
    "foundations_2": {
        "module_number": 1,
        "submodule_number": 2,
        "module_title": "Foundations of Prompting",
        "submodule_title": "Role Assignment",
        "description": "Discover how assigning specific roles to AI dramatically changes response quality and perspective. By starting prompts with 'You are an expert [profession]...', you give AI the context it needs to adopt appropriate expertise and terminology.",
        "key_learning": "How to use role assignment to control AI's perspective, expertise level, and response style",
        "why_important": "Generic prompts get generic responses. Role assignment makes AI adopt the right lens - technical, creative, analytical - dramatically improving relevance and depth.",
        "real_world_use": "Use this when you need specialized analysis. For code reviews, assign 'senior software engineer'. For content writing, assign 'creative copywriter'. For business analysis, assign 'strategic consultant'."
    },
    "foundations_3": {
        "module_number": 1,
        "submodule_number": 3,
        "module_title": "Foundations of Prompting",
        "submodule_title": "Chain-of-Thought Reasoning",
        "description": "Learn to guide AI through step-by-step reasoning processes using phrases like 'Let's think step by step' or 'First... Then... Finally...'. This technique dramatically improves accuracy on complex problems by breaking reasoning into manageable steps.",
        "key_learning": "How to use chain-of-thought prompting to improve AI accuracy on complex analytical tasks",
        "why_important": "Complex problems solved in one step often contain logical errors. Step-by-step reasoning forces AI to show its work, catches mistakes early, and produces more reliable conclusions.",
        "real_world_use": "Use this for complex analysis like debugging code, evaluating business decisions, or analyzing multi-factor problems where you need to trace the reasoning process and verify each step."
    },
    "foundations_4": {
        "module_number": 1,
        "submodule_number": 4,
        "module_title": "Foundations of Prompting",
        "submodule_title": "Real-world Practice",
        "description": "Put it all together! This lesson challenges you to combine role assignment, constraints, and step-by-step reasoning in a single comprehensive prompt. Learn to build multi-layered prompts that leverage all foundation techniques simultaneously.",
        "key_learning": "How to combine multiple prompting techniques (role, constraints, chain-of-thought) for maximum effectiveness",
        "why_important": "Real-world tasks rarely need just one technique. Professional prompt engineering requires combining multiple strategies to handle complex, nuanced requirements.",
        "real_world_use": "Use this comprehensive approach for high-stakes tasks like preparing executive reports, conducting thorough research, or building AI systems where accuracy, expertise, and structured reasoning are all essential."
    },

    # Module 2: Advanced Prompting Patterns
    "advanced-patterns_1": {
        "module_number": 2,
        "submodule_number": 1,
        "module_title": "Advanced Prompting Patterns",
        "submodule_title": "Few-Shot Learning",
        "description": "Master teaching AI through examples. Provide 2-3 samples of your desired output format, and AI learns the pattern. This is one of the most powerful techniques for achieving consistent formatting, style, and structure across multiple outputs.",
        "key_learning": "How to use example-based learning to achieve consistent formatting and style in AI outputs",
        "why_important": "Describing format in words is hard and error-prone. Showing examples is precise and unambiguous - AI sees exactly what you want and replicates it perfectly.",
        "real_world_use": "Use this when you need consistent output format across many items - like formatting product descriptions, converting data to specific JSON schemas, or maintaining style consistency in content generation."
    },
    "advanced-patterns_2": {
        "module_number": 2,
        "submodule_number": 2,
        "module_title": "Advanced Prompting Patterns",
        "submodule_title": "Output Formatting",
        "description": "Learn to specify exact output structures: JSON objects with specific keys, markdown tables with defined columns, numbered lists, bullet hierarchies. Master the art of making AI outputs immediately usable without manual reformatting.",
        "key_learning": "How to specify precise output formats (JSON, tables, lists) that require no post-processing",
        "why_important": "Manual reformatting wastes time and introduces errors. Specifying format upfront means AI outputs drop directly into your workflows, APIs, or pipelines.",
        "real_world_use": "Use this when building AI pipelines where outputs feed into other systems - like extracting data to JSON for APIs, generating CSV reports for spreadsheets, or creating structured documentation."
    },
    "advanced-patterns_3": {
        "module_number": 2,
        "submodule_number": 3,
        "module_title": "Advanced Prompting Patterns",
        "submodule_title": "Prompt Chaining",
        "description": "Learn to break complex tasks into a sequence of focused prompts: first extract information, then analyze it, then generate recommendations. Each prompt builds on the previous output, creating a powerful multi-stage analysis pipeline.",
        "key_learning": "How to decompose complex tasks into sequential prompts that build on each other",
        "why_important": "Trying to do everything in one prompt often produces shallow results. Chaining creates depth - each stage can focus fully on its specific task without juggling multiple objectives.",
        "real_world_use": "Use this for multi-stage workflows like document analysis (extract → summarize → identify issues → recommend solutions) or content creation (brainstorm → outline → draft → refine)."
    },
    "advanced-patterns_4": {
        "module_number": 2,
        "submodule_number": 4,
        "module_title": "Advanced Prompting Patterns",
        "submodule_title": "Constraint Engineering",
        "description": "Master sophisticated constraint techniques: length limits ('max 100 words'), tone requirements ('professional, no jargon'), required elements ('include 3 examples'), and exclusions ('avoid technical terms'). Learn to layer multiple constraints for surgical precision.",
        "key_learning": "How to combine multiple constraint types to achieve precise control over AI behavior",
        "why_important": "Single constraints are basic. Professional prompting requires layering multiple constraints to meet real-world requirements around length, tone, content, and style simultaneously.",
        "real_world_use": "Use this for content that must meet strict specifications - like social media posts (character limits, tone, hashtags), regulatory content (required disclosures, prohibited claims), or technical documentation (audience-appropriate language)."
    },

    # Module 3: Domain-Specific Prompting
    "domain-specific_1": {
        "module_number": 3,
        "submodule_number": 1,
        "module_title": "Domain-Specific Prompting",
        "submodule_title": "Technical Documentation",
        "description": "Learn to prompt AI for clear, accurate technical writing. Master specifying target audience (beginner/intermediate/advanced), technical depth, code examples, and documentation standards. Create docs that developers actually want to read.",
        "key_learning": "How to specify audience level, technical depth, and documentation structure for developer-focused content",
        "why_important": "Bad technical docs cause confusion and support burden. Well-prompted docs match audience expertise, include relevant examples, and follow conventions developers expect.",
        "real_world_use": "Use this when creating API documentation, SDK guides, README files, or internal technical specs where clarity and accuracy directly impact developer productivity."
    },
    "domain-specific_2": {
        "module_number": 3,
        "submodule_number": 2,
        "module_title": "Domain-Specific Prompting",
        "submodule_title": "Business Analysis",
        "description": "Master prompting for business contexts: include stakeholder perspectives, focus on actionable insights, specify decision criteria, and emphasize ROI/impact. Learn to extract business value, not just information.",
        "key_learning": "How to prompt for stakeholder-focused insights that drive business decisions",
        "why_important": "Business stakeholders don't want raw analysis - they want 'so what?' and 'what should we do?'. Prompting for decision-focused insights makes AI output immediately actionable.",
        "real_world_use": "Use this for executive briefings, strategic recommendations, market analysis, or investment decisions where outputs must be framed around business impact and next actions."
    },
    "domain-specific_3": {
        "module_number": 3,
        "submodule_number": 3,
        "module_title": "Domain-Specific Prompting",
        "submodule_title": "Creative Content",
        "description": "Learn to balance creativity with control. Master specifying tone (playful/professional/inspiring), target audience, brand voice, and creative direction while maintaining quality and consistency. Get engaging content that stays on-brand.",
        "key_learning": "How to direct creative content generation while maintaining brand consistency and quality",
        "why_important": "Unconstrained creative AI produces inconsistent, off-brand content. Learning to channel creativity with clear direction produces engaging content that fits your brand identity.",
        "real_world_use": "Use this for marketing copy, social media content, blog posts, or ad campaigns where you need creative, engaging content that aligns with brand voice and connects with your target audience."
    },
    "domain-specific_4": {
        "module_number": 3,
        "submodule_number": 4,
        "module_title": "Domain-Specific Prompting",
        "submodule_title": "Data Analysis",
        "description": "Master prompting for data insights: specify analysis type (trend analysis, comparison, correlation), metrics of interest, and interpretation depth. Learn to extract meaningful patterns and statistical insights from data.",
        "key_learning": "How to prompt for specific analytical techniques, metrics, and statistically sound interpretations",
        "why_important": "Generic data prompts miss important patterns and produce shallow insights. Specifying analytical techniques and metrics ensures thorough, accurate analysis.",
        "real_world_use": "Use this when analyzing datasets, A/B test results, user behavior metrics, or sales data where you need to identify trends, compare segments, or find statistically significant patterns."
    },

    # Module 4: Advanced AI Techniques
    "advanced-techniques_1": {
        "module_number": 4,
        "submodule_number": 1,
        "module_title": "Advanced AI Techniques",
        "submodule_title": "Meta-Prompting",
        "description": "Discover the power of having AI optimize its own instructions. Ask AI to first design the perfect prompt for a task, then execute that prompt. This leverages AI's understanding to create better prompts than you might write manually.",
        "key_learning": "How to use AI to generate and refine its own prompts based on task analysis",
        "why_important": "AI understands what instructions work best for its own architecture. Meta-prompting taps into this knowledge to create more effective prompts than manual trial-and-error.",
        "real_world_use": "Use this for complex or unfamiliar tasks where you're not sure how to structure the prompt. Let AI analyze the task and design optimal instructions before executing."
    },
    "advanced-techniques_2": {
        "module_number": 4,
        "submodule_number": 2,
        "module_title": "Advanced AI Techniques",
        "submodule_title": "Prompt Optimization",
        "description": "Learn systematic optimization: test multiple prompt variations, compare results, identify what works. Master A/B testing different role assignments, constraint combinations, and structural approaches to find the highest-performing prompts.",
        "key_learning": "How to systematically test and refine prompts through variation and comparison",
        "why_important": "First-draft prompts are rarely optimal. Systematic testing reveals what improvements actually matter versus what's just different. This turns good prompts into great ones.",
        "real_world_use": "Use this for high-value, repeated tasks like customer support responses, content generation templates, or data extraction pipelines where optimizing prompt performance has compounding benefits."
    },
    "advanced-techniques_3": {
        "module_number": 4,
        "submodule_number": 3,
        "module_title": "Advanced AI Techniques",
        "submodule_title": "Context Management",
        "description": "Master managing context across multi-turn conversations. Learn to reference previous information, build on established understanding, and maintain coherence. Essential for complex interactions that span multiple prompts.",
        "key_learning": "How to maintain context and continuity across multi-turn AI conversations",
        "why_important": "Each prompt in isolation loses valuable context. Managing context maintains coherence, avoids repetition, and enables progressively deeper analysis as conversations unfold.",
        "real_world_use": "Use this for iterative work like code refactoring across multiple files, document editing with multiple revision rounds, or research where each prompt should build on previous insights."
    },
    "advanced-techniques_4": {
        "module_number": 4,
        "submodule_number": 4,
        "module_title": "Advanced AI Techniques",
        "submodule_title": "Error Handling & Recovery",
        "description": "Learn to build robust prompts that handle edge cases: what to do when information is missing, unclear, contradictory, or incomplete. Include fallback instructions that make prompts production-ready.",
        "key_learning": "How to anticipate and handle errors, missing information, and edge cases in prompts",
        "why_important": "Real-world inputs are messy. Production prompts must handle imperfect data gracefully rather than producing garbage outputs or hallucinating missing information.",
        "real_world_use": "Use this for production AI systems processing user inputs, automated workflows handling varied data quality, or any application where robustness matters more than perfect-case performance."
    },

    # Module 5: AI-Powered Presentation Builder
    "presentation-builder_1": {
        "module_number": 5,
        "submodule_number": 1,
        "module_title": "AI-Powered Presentation Builder",
        "submodule_title": "Document Analysis & Information Extraction",
        "description": "Learn to extract structured information from documents for presentations. Master prompting for main topics, key sections with headings, bullet points per section, and important data. Transform unstructured text into slide-ready structured content.",
        "key_learning": "How to extract and organize document content into presentation-ready structure",
        "why_important": "Presentations need structured hierarchy: sections, points, and supporting details. Learning to extract with this structure saves hours of manual organization.",
        "real_world_use": "Use this when converting reports, articles, or research papers into presentations. Extract key information already organized into sections and bullet points ready for slides."
    },
    "presentation-builder_2": {
        "module_number": 5,
        "submodule_number": 2,
        "module_title": "AI-Powered Presentation Builder",
        "submodule_title": "Content Generation for Slides",
        "description": "Master generating actual slide content with precise specifications: compelling titles (max 8 words), concise bullets (under 15 words), specific number of slides, and clear structure. Learn to constrain content to fit presentation format perfectly.",
        "key_learning": "How to generate slide-formatted content with word limits, quantities, and structure",
        "why_important": "Slides have strict constraints - too much text kills presentations. Learning to generate content that fits these constraints saves massive editing time.",
        "real_world_use": "Use this to transform any document into 5-7 slide presentations with properly formatted titles, bullets, and explanations that work perfectly in presentation software."
    },
    "presentation-builder_3": {
        "module_number": 5,
        "submodule_number": 3,
        "module_title": "AI-Powered Presentation Builder",
        "submodule_title": "Content Refinement & Polish",
        "description": "Master iterative refinement through targeted prompts. Learn to improve specific elements: make titles more compelling, simplify bullets, add data from source, verify accuracy, improve flow. Transform good content into great presentations through precise, targeted improvements.",
        "key_learning": "How to use targeted refinement prompts to iteratively improve specific slide elements",
        "why_important": "First drafts are never perfect. Professional presentations require refinement: stronger titles, clearer bullets, better flow. Learning to refine systematically produces polished results.",
        "real_world_use": "Use this to elevate presentation quality: strengthen weak slides, ensure accuracy against source material, improve narrative flow, and add compelling examples or data points."
    },
    "presentation-builder_4": {
        "module_number": 5,
        "submodule_number": 4,
        "module_title": "AI-Powered Presentation Builder",
        "submodule_title": "HTML/CSS Code Generation & Preview",
        "description": "Learn to prompt AI to generate complete, working HTML/CSS/JavaScript presentation code. Master specifying structure (slides, navigation), styling (colors, fonts, layout), interactivity (buttons, keyboard controls), and output format (self-contained, ready to run).",
        "key_learning": "How to generate production-ready presentation code with specific structure, design, and functionality",
        "why_important": "Vague code prompts produce broken or incomplete results. Learning to specify technical requirements precisely generates working code that needs minimal fixes.",
        "real_world_use": "Use this to create custom HTML presentations from documents: specify exact design requirements, navigation features, and responsive behavior to generate working presentations you can immediately deploy."
    }
}


def get_submodule_description(module_id: str, submodule_id: int) -> dict | None:
    """Get description data for a specific submodule"""
    key = f"{module_id}_{submodule_id}"
    return SUBMODULE_DESCRIPTIONS.get(key)


def get_all_submodule_descriptions() -> dict:
    """Get all submodule descriptions"""
    return SUBMODULE_DESCRIPTIONS
