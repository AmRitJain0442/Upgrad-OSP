"""Generate sample documents with Gemini"""
import asyncio
import os
import json
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

provider = GoogleProvider(api_key=api_key)
model = GoogleModel("gemini-flash-lite-latest", provider=provider)
agent = Agent(model=model)

SAMPLES_DIR = Path("frontend/static/samples")
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

async def gen_doc(name, prompt):
    print(f"Generating {name}...")
    try:
        result = await agent.run(prompt)
        (SAMPLES_DIR / name).write_text(result.output)
        print(f"✓ {name} ({len(result.output)} chars)")
        return name, result.output
    except Exception as e:
        print(f"✗ {name}: {e}")
        return name, None

async def main():
    print("Generating sample documents...")
    print(f"Model: gemini-flash-lite-latest\n{'='*60}")
    
    tasks = [
        gen_doc("general_article.txt", """Write exactly 650 clean, well-formatted words about remote work evolution in tech.

Title: The Evolution of Remote Work in Tech

Opening paragraph (80 words): Describe pre-2020 office culture - daily commutes, open floor plans, conference rooms, the ritual of 9-to-5.

Section - The Pandemic Shift (120 words): How COVID-19 forced rapid change, initial struggles with video calls and home setups, surprising productivity discoveries, companies realizing remote work viability.

Section - Key Benefits (150 words): Elaborate each with examples:
* Schedule and location flexibility  
* Eliminated commute saves time and money
* Improved work-life balance and mental health
* Access to global talent beyond geography
* Better focus and deep work without interruptions
* Cost savings for both companies and workers

Section - Challenges (150 words): Detail each with real scenarios:
* Communication barriers and timezone coordination
* Company culture and spontaneous collaboration loss
* Technology issues and security concerns
* Work-life boundary blurring and burnout
* Isolation and loneliness impacts

Current State (80 words): Statistics like "73 percent prefer hybrid", company policies, industry trends from major tech firms.

Future Outlook (70 words): Permanent workplace changes, hybrid model evolution, office redesigns.

Use clear professional journalism style. Vary sentence structure."""),

        gen_doc("technical_api_doc.txt", """Write exactly 750 words of clean technical documentation for UserAuth API v2.1.

API Overview (100 words): Purpose, audience, version 2.1, base URL https://api.example.com/v1, JSON responses, HTTPS only, 99.9 percent uptime.

Authentication (120 words): Bearer tokens, JWT format, 24-hour expiration, how to include in headers, example format, security best practices.

POST /auth/register (150 words):
- Purpose: Create user account
- Parameters: email (required, unique), password (required, min 8 chars with uppercase/lowercase/number), username (required, 3-20 alphanumeric), full_name (optional)
- Request JSON example
- Response 201 success with user_id, token, created_at
- Response 400 validation error
- Response 409 duplicate email
- Full JSON examples for each

POST /auth/login (150 words):
- Purpose: Authenticate user
- Parameters: email (required), password (required), remember_me (optional boolean)
- Request JSON example  
- Response 200 success with token, user object, expires_at
- Response 401 invalid credentials
- Response 429 rate limited
- Full JSON examples

GET /auth/user (120 words):
- Purpose: Get user profile
- Requires Bearer token
- No body
- Response 200 with full profile JSON
- Response 401 unauthorized
- Response 404 not found
- Examples

Error Handling (60 words): Standard format, status codes, error codes, message display.

Rate Limiting (50 words): 1000/hour limit, response headers, 429 handling, backoff strategy.

Professional technical writing. Complete JSON examples."""),

        gen_doc("business_report.txt", """Write exactly 700 words: Q3 2024 Business Report for TechStart Inc.

Header:
Company: TechStart Inc.
Period: Q3 2024 (July-September)
Prepared: Strategic Analysis Team  
Date: October 15, 2024

Executive Summary (100 words): Overall strong quarter, revenue growth, customer expansion, operational challenges, Q4 strategic direction.

Financial Performance (140 words):
Q3 Metrics:
- Revenue: 2.4 million (up 15 percent YoY from 2.08M)
- MRR: 800K
- Gross Margin: 78 percent
- Operating Expenses: 1.9M
- Net Profit: 500K
- Cash: 4.2M
- Burn Rate: 150K/month (improved)
Analyze trends, compare to Q2, explain revenue drivers.

Customer Metrics (120 words):
- Active Customers: 1,250 (up 22 percent)
- New Acquired: 180
- Churned: 25
- Churn Rate: 8 percent (industry 10 percent)
- ACV: 1,920 dollars
- LTV: 8,640 dollars
- CAC: 1,200 dollars
- LTV:CAC Ratio: 7.2:1
Analyze health and growth implications.

Key Achievements (120 words):
- Enterprise Plan launched: 400K ARR
- European expansion: UK, Germany, 45 customers
- SOC 2 Type II compliance achieved
- AI analytics feature: 85 percent adoption
- CloudTech Solutions partnership
- Support response: 4 hours to 45 minutes
Detail impact and value of each.

Challenges (100 words):
- VentureSoft competition pressure
- Developer hiring delays (3 roles, 4+ months)
- Enterprise integration complexities
- Infrastructure costs: 120K vs budgeted 90K
- Support team capacity issues
Explain operational impact and mitigation.

Recommendations (80 words):
1. Hire 2 enterprise sales reps
2. Migrate to reserved cloud instances (30 percent savings)
3. Prioritize top 5 enterprise features
4. Partner with recruitment agency
5. Proactive customer success program
Provide rationale for each.

Q4 Outlook (40 words): Target 2.8M revenue (17 percent growth), 1,450 customers (16 percent growth), focus areas, expected challenges.

Formal business style. Data-driven. Specific numbers."""),

        gen_doc("creative_brief.txt", """Write exactly 650 words: Social Media Campaign Creative Brief

Header:
Campaign: EcoTech Future
Client: GreenTech Solutions
Duration: Jan 15 - Mar 31, 2025
Budget: 75,000 dollars
Agency: Creative Minds Digital

Target Audience (100 words):
Primary: Urban professionals 28-42, household income 75K-150K, tech-savvy early adopters, environmentally conscious, active on Instagram/LinkedIn/sustainable blogs, value quality over price, household tech decision-makers.

Secondary: Millennials/Gen Z 25-35, follow sustainability influencers, engaged in climate discussions, seeking carbon footprint reduction.

Objectives (80 words):
1. Increase brand awareness 40 percent
2. Drive 10,000 landing page visits
3. Generate 2,500 qualified leads for EcoHome devices
4. Grow social followers 25 percent
5. Position as sustainable tech innovation leader
Measurable success in engagement, leads, sentiment.

Key Messages (120 words):
1. "Technology That Gives Back to Earth" - Reduce environmental impact, save 40 percent energy, reduce carbon by 2 tons annually
2. "Innovation Without Compromise" - Cutting-edge features, premium experience, green powered, join 50,000+ users
3. "Your Future, Powered Sustainably" - Personal climate impact, environmental legacy, small changes, collective impact
Evoke aspiration with concrete benefits.

Tone & Voice (90 words):
INSPIRATIONAL: Uplift without preaching. Show possibilities not guilt. "Imagine", "together we can", "future looks bright"
AUTHENTIC: Real stories, genuine data, transparent challenges. No greenwashing. Show journey.
ACCESSIBLE: Simple explanations, achievable sustainability, "You don't have to be perfect, just participate"
Balance: 60 percent inspirational, 30 percent educational, 10 percent urgency.

Content Deliverables (140 words):
Instagram (10 posts):
- 3 product showcases in real homes
- 2 customer testimonials with metrics
- 2 behind-scenes manufacturing
- 2 educational infographics on savings
- 1 launch announcement

Blogs (5 articles, 1200-1500 words):
1. True Cost of Traditional Tech Environmental Impact
2. Case Study: Johnson Family 45 Percent Energy Reduction
3. Smart Home Sustainability Complete Guide
4. 5 Green Technology Myths Debunked
5. Sustainable Living 2025 Trends

Videos (3, 60-90 seconds):
1. Real home product demo
2. Customer journey testimonial
3. Sustainable manufacturing process

Visual Style (80 words):
Colors: Sage Green, Sky Blue, Warm Earth Tone, Clean White. 70 percent light backgrounds for cleanliness.
Imagery: Natural lighting, real homes not stock, people naturally interacting with tech, nature elements, authentic unposed moments, high quality not overly polished.

Call-to-Action (30 words):
Primary: Calculate Your Impact (interactive savings tool)
Secondary: Join the Movement (newsletter with tips)
Tertiary: Explore EcoHome (product pages)

Success Metrics (40 words):
1. Engagement: 4.5 percent average
2. Leads: 2,500 qualified, 15 percent to demos
3. Sentiment: 30 percent increase positive mentions
4. Traffic: 10,000 unique visitors
5. Growth: 25 percent followers, 80 percent retention

Professional creative brief style."""),

        gen_doc("tutorial_content.txt", """Write exactly 700 words: Git Version Control Tutorial for Beginners

Title: Getting Started with Git Version Control

Introduction (90 words): Explain what Git is - distributed version control system tracking code changes. Why essential: collaboration, history tracking, experimentation safety, professional standard. Who uses it: developers, designers, writers, anyone tracking file changes. Created by Linus Torvalds in 2005. Now industry standard with millions of users. This tutorial covers fundamentals to get you productive quickly.

Prerequisites (60 words):
Before starting ensure you have:
- Git installed (download from git-scm.com)
- Command line/terminal basic familiarity
- Text editor (VS Code, Sublime, Atom, or any preferred)
- Basic computer file system understanding
- Willingness to learn command line tools

Step-by-Step Guide (350 words):

Step 1 - Initialize Repository (45 words):
Command: git init
Creates new Git repository in current directory. Makes hidden .git folder containing all version history. Run once per project. Creates empty repository ready for tracking changes. Now your folder is Git-aware and can track file versions.

Step 2 - Check Status (40 words):
Command: git status
Shows current repository state. Lists untracked files (not yet managed by Git), modified files, staged changes ready for commit. Most-used Git command. Run frequently to understand what's happening. Clean output means no changes.

Step 3 - Add Files to Staging (50 words):
Command: git add filename.txt or git add . (adds all files)
Moves files to staging area. Staging area is preparation zone before committing. Allows selecting specific changes to save. Like putting items in shopping cart before checkout. Staged files ready for permanent snapshot. Can unstage with git reset filename.

Step 4 - Commit Changes (55 words):
Command: git commit -m "Descriptive message here"
Creates permanent snapshot of staged changes. Commit message describes what changed and why. Good messages crucial for team collaboration and future reference. Example: "Add user login validation" not "fixes". Each commit gets unique identifier (hash). Commits form project history timeline.

Step 5 - View History (40 words):
Command: git log
Shows commit history with dates, authors, messages, commit hashes. Use git log --oneline for compact view. Navigate history to understand project evolution. Useful for finding when bugs introduced or features added. Press Q to exit.

Step 6 - Create Branch (40 words):
Command: git branch feature-name
Creates new branch for isolated development. Master/main branch stays stable while experimenting. Branches are lightweight, create freely. List all branches with git branch. Current branch marked with asterisk.

Step 7 - Switch Branches (40 words):
Command: git checkout branch-name or git switch branch-name (newer)
Changes working directory to different branch. Files update to match branch state. Safe experimentation without affecting main code. Modern Git uses switch command for clarity.

Step 8 - Merge Branches (40 words):
Command: git merge feature-name (while on main branch)
Integrates changes from feature branch into current branch. Git automatically combines changes. Conflicts occur if same lines modified - must resolve manually. After successful merge, feature branch can be deleted.

Common Commands Reference (80 words):
| Command | Purpose |
| git clone URL | Copy remote repository locally |
| git pull | Download latest changes from remote |
| git push | Upload local commits to remote |
| git diff | Show changes not yet staged |
| git reset | Unstage files or undo commits |

These five plus the eight above cover 90 percent of daily Git usage.

Tips for Beginners (60 words):
1. Commit often with clear messages - small frequent commits better than large rare ones
2. Always check git status before committing to verify changes
3. Use branches for new features - keep main branch stable and deployable
4. Write commit messages in present tense: "Add feature" not "Added feature"
5. Don't commit sensitive data like passwords or API keys

Next Steps (30 words):
Learn: Remote repositories (GitHub, GitLab), pull requests, collaboration workflows, advanced branching strategies, merge conflict resolution, Git hooks, rebasing, cherry-picking.

Clean instructional style. Include command examples."""),

        gen_doc("complex_scenario.txt", """Write exactly 750 words: Complex Business Scenario Requiring Multi-faceted Analysis

Title: Product Launch Decision Dilemma at DataFlow Inc.

Company Background (120 words):
DataFlow Inc. is a B2B SaaS company founded in early 2021, currently employing 50 people across engineering, sales, and customer success. The company provides a cloud-based data analytics platform helping mid-market companies visualize and analyze their business data. Annual Recurring Revenue currently stands at 5 million dollars with 180 active enterprise clients paying average of 28,000 dollars per year. Growth rate has been steady at 25 percent annually. Company has raised 8 million in Series A funding with 3.2 million remaining in the bank. Primary investors pushing for acceleration to justify Series B raise next year. Main competitors include established players like Tableau and emerging startups.

The Situation (100 words):
Leadership team faces critical decision: which of two potential new products to develop. Board meeting scheduled in two weeks requires definitive choice with detailed justification. Resources only sufficient for one product launch. Decision will define company direction for next 18 months and significantly impact Series B fundraising prospects. Engineering team already stretched thin maintaining current platform while pushing new features. Sales team reporting customer requests split between both options. Delay means missing market opportunities, but wrong choice could waste critical resources and momentum. Stakes exceptionally high for young company.

Option A - AI-Powered Analytics Assistant (150 words):
Development Timeline: 6 months to MVP, 9 months to full release
Estimated Cost: 800,000 dollars including ML engineers (2 hires), infrastructure, training data
Market Size: Approximately 5,000 potential customers in existing target segment
Expected Revenue: Year 1 projection 2 million ARR, Year 2 projection 4.5 million
Pricing Model: Premium add-on at 500 dollars per month per user
Customer Demand: 60 percent of customer requests mention AI capabilities
Technical Requirements: Machine learning team (need to hire), significant compute costs, ongoing model training
Strategic Benefits: Differentiates from competitors, aligns with industry trends, potential PR value
Risks: Highly competitive space with OpenAI, Google entering market. Technology complexity high. Customer expectations may exceed capabilities.

Option B - Mobile Application (150 words):
Development Timeline: 4 months to iOS/Android MVP, 6 months to feature parity
Estimated Cost: 500,000 dollars including mobile developers (1 hire), design, testing
Market Size: 12,000 potential customers (current plus adjacent segments)
Expected Revenue: Year 1 projection 1.2 million ARR, Year 2 projection 2.8 million
Pricing Model: Included with existing plans, drives new customer acquisition
Customer Demand: 40 percent of customer requests specifically mention mobile access
Technical Requirements: Mobile developers (can leverage existing backend), app store management
Strategic Benefits: Expands market reach, matches competitor features (table stakes), improves user engagement
Risks: Mobile development complex with platform differences. Requires ongoing maintenance for OS updates. Could cannibalize desktop usage without growing revenue proportionally.

Business Constraints (120 words):
Financial Constraints:
- Total available budget: 1 million maximum (must reserve buffer)
- Current burn rate: 200,000 per month
- Investor pressure to show path to profitability

Human Resource Constraints:
- Engineering team: 8 developers currently at 90 percent capacity
- Cannot hire more than 2 additional engineers within budget
- Training new hires takes 2-3 months productivity loss
- Existing team morale concerns about overwork

Market Constraints:
- Customer requests split 60/40 favoring AI but mobile considered more urgent
- Competitors launching similar features (need speed to market)
- Sales team needs new features for Q1 renewals (3 months)

Stakeholder Opinions (110 words):
CEO Position: Favors AI Assistant for strategic differentiation and press value. Concerns about execution risk but believes it justifies higher Series B valuation. Willing to accept longer timeline.

CTO Position: Prefers Mobile App as more achievable with current team. Worries AI project scope will creep and timeline extend to 12+ months. Values execution certainty over ambition.

Head of Sales: Strongly advocates Mobile App. Reports losing deals due to lack of mobile access. Needs quick wins for upcoming renewal cycle. Views AI as "nice to have" versus mobile "must have".

This scenario requires analyzing: financial projections, risk assessment, resource allocation, market timing, stakeholder management, and long-term strategy.

Present clear facts. No obvious correct answer. Force critical thinking."""),

        gen_doc("policy_document.txt", """Write exactly 650 words: Formal Company Remote Work Policy

TITLE: Remote Work Policy
COMPANY: TechCorp Global
EFFECTIVE: January 1, 2025
VERSION: 2.0

Policy Statement (80 words):
This policy establishes guidelines for remote work arrangements at TechCorp Global. Purpose is enabling flexible work while maintaining productivity, collaboration, and company culture. Remote work is a privilege based on role requirements, performance, and business needs. This policy applies to all employees globally. Managers retain discretion for team-specific requirements. Policy subject to periodic review and modification. Employees must acknowledge and comply with all terms. Violations may result in termination of remote privileges or employment.

Eligibility Criteria (100 words):
Roles Eligible for Remote Work:
- Software Engineers and Developers
- Data Analysts and Scientists
- Product Managers
- Marketing and Content Specialists
- Customer Success Managers (with geographic restrictions)

Eligibility Requirements:
- Minimum 6 months tenure demonstrating competence
- Current performance rating "Meets Expectations" or higher
- Role does not require regular physical presence (labs, hardware, facilities)
- Manager approval required
- Completed remote work training program
- Home workspace meeting company standards

Ineligible roles: Facilities, IT hardware support, laboratory technicians, roles requiring specialized on-site equipment.

Remote Work Arrangement Types (110 words):
1. Fully Remote: Employee works 100 percent from home or approved remote location. Must reside in approved states/countries for legal/tax compliance. Requires executive approval. Annual office visits may be required.

2. Hybrid Schedule: Employee splits time between office and remote. Standard hybrid: minimum 2 days in-office per week (Tuesday-Thursday preferred). Specific days determined with manager based on team needs and collaboration requirements. Advance notice required for schedule changes.

3. Temporary Remote: Short-term arrangements up to 3 months for special circumstances (family care, relocation, medical). Manager approval sufficient. Requires documented end date and transition plan.

Requirements for Remote Workers (120 words):
Workspace Requirements:
- Dedicated workspace free from distractions
- Ergonomic desk and chair meeting safety standards
- Adequate lighting and ventilation
- Professional background for video calls

Technology Requirements:
- Reliable high-speed internet minimum 50 Mbps download, 10 Mbps upload
- Company-provided laptop (no personal devices for work)
- Webcam and headset for meetings
- VPN access mandatory for all work activities
- Multi-factor authentication enabled
- Home network security: WPA2/WPA3 encryption, updated router firmware

Availability Requirements:
- Online and responsive during core business hours: 9 AM - 3 PM EST
- Attend all scheduled meetings via video (camera on)
- Respond to messages within 1 hour during core hours
- Maintain calendar with accurate availability

Performance Expectations (90 words):
Remote employees held to same performance standards as office-based staff. Expectations include:
- Meeting all deadlines and deliverables as assigned
- Participating actively in team meetings and collaboration
- Maintaining communication with manager and teammates
- Completing work with quality meeting company standards
- Adhering to all company policies and code of conduct
- Documenting work appropriately in company systems

Performance reviews conducted quarterly. Failure to meet expectations may result in return-to-office requirement or other corrective actions per standard policies.

Equipment & Stipends (80 words):
Company Provided:
- Laptop computer (standard model for role)
- Monitor, keyboard, mouse upon request
- Software licenses as required for role

Employee Stipend:
- 500 dollars annually for home office equipment/improvements
- Reimbursement for office supplies within policy limits
- Internet subsidy: 50 dollars monthly for primary internet service

Equipment remains company property. Must be returned upon termination. Loss or damage may result in replacement charges.

Communication Guidelines (70 words):
1. Default to asynchronous communication (email, Slack) for non-urgent matters
2. Use video calls for complex discussions, brainstorming, sensitive topics
3. Document decisions in writing (meeting notes, decision logs)
4. Respond to messages within expected timeframes
5. Set status appropriately (available, in meeting, away)
6. Use shared calendars for transparency

Formal professional policy language. Clear rules."""),
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"\n{'='*60}\nComplete: {sum(1 for _, c in results if c)}/5 generated")
    
    # Create mapping
    mapping = {
        "foundations-1": "general_article.txt", "foundations-2": "general_article.txt",
        "foundations-3": "complex_scenario.txt", "foundations-4": "business_report.txt",
        "advanced-patterns-1": "tutorial_content.txt", "advanced-patterns-2": "data_analysis.txt",
        "advanced-patterns-3": "business_report.txt", "advanced-patterns-4": "policy_document.txt",
        "domain-specific-1": "technical_api_doc.txt", "domain-specific-2": "business_report.txt",
        "domain-specific-3": "creative_brief.txt", "domain-specific-4": "data_analysis.txt",
        "advanced-techniques-1": "complex_scenario.txt", "advanced-techniques-2": "general_article.txt",
        "advanced-techniques-3": "business_report.txt", "advanced-techniques-4": "technical_api_doc.txt",
    }
    (SAMPLES_DIR / "document_mapping.json").write_text(json.dumps(mapping, indent=2))
    print("✓ Mapping created")

if __name__ == "__main__":
    asyncio.run(main())
