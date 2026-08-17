"""CareerPilot AI — Demo data for offline / fallback mode."""

from __future__ import annotations


def get_demo_cv_analysis() -> dict:
    """Return sample CV analysis payload."""
    return {
        "name": "Alexandra Chen",
        "email": "alexandra.chen@email.com",
        "phone": "+44 7700 900123",
        "top_qualification": "MSc Computer Science — Imperial College London",
        "skills": [
            "Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL",
            "AWS", "Docker", "Kubernetes", "Data Analysis", "NLP",
            "React", "TypeScript", "Git", "Agile/Scrum", "REST APIs",
            "Pandas", "Scikit-learn", "Deep Learning", "Statistics",
            "Communication", "Problem Solving", "Team Leadership",
        ],
        "education": [
            {
                "degree": "MSc Computer Science",
                "institution": "Imperial College London",
                "year": "2022 – 2023",
                "details": "Distinction — Specialisation in Machine Learning & AI",
            },
            {
                "degree": "BEng Software Engineering",
                "institution": "University of Manchester",
                "year": "2018 – 2022",
                "details": "First Class Honours — Dean's List",
            },
        ],
        "experience": [
            {
                "title": "Machine Learning Engineer",
                "company": "TechVision Labs",
                "period": "Jun 2023 – Present",
                "description": "Built production ML pipelines serving 2M+ users. Led model deployment on AWS SageMaker.",
            },
            {
                "title": "Data Science Intern",
                "company": "FinTech Global",
                "period": "Jun 2022 – Sep 2022",
                "description": "Developed fraud detection models achieving 94% precision. Automated reporting dashboards.",
            },
            {
                "title": "Software Developer",
                "company": "StartupHub",
                "period": "Jul 2021 – May 2022",
                "description": "Full-stack development with React and Python. Shipped 3 major product features.",
            },
        ],
    }


def get_demo_recommendations() -> list[dict]:
    """Return sample job recommendations."""
    return [
        {
            "rank": 1,
            "title": "Senior Machine Learning Engineer",
            "company": "DeepMind",
            "location": "London, UK",
            "industry": "Artificial Intelligence",
            "match_score": 94,
            "salary": "£95,000 – £130,000",
            "required_skills": ["Python", "TensorFlow", "Deep Learning", "PyTorch", "AWS"],
            "missing_skills": ["C++", "Research Publications"],
            "description": "Join our world-class research team building next-generation AI systems. You'll work on cutting-edge deep learning models and deploy them at scale.",
        },
        {
            "rank": 2,
            "title": "AI Product Engineer",
            "company": "Microsoft",
            "location": "Reading, UK",
            "industry": "Technology",
            "match_score": 88,
            "salary": "£80,000 – £110,000",
            "required_skills": ["Python", "Azure", "NLP", "REST APIs", "Agile/Scrum"],
            "missing_skills": ["C#", ".NET"],
            "description": "Shape the future of Copilot products. Build intelligent features used by millions of enterprise customers worldwide.",
        },
        {
            "rank": 3,
            "title": "Data Scientist",
            "company": "Revolut",
            "location": "London, UK (Hybrid)",
            "industry": "FinTech",
            "match_score": 82,
            "salary": "£70,000 – £95,000",
            "required_skills": ["Python", "SQL", "Statistics", "Machine Learning", "Data Analysis"],
            "missing_skills": ["R", "Tableau"],
            "description": "Drive data-informed decisions across product, risk, and marketing teams in one of Europe's fastest-growing fintechs.",
        },
        {
            "rank": 4,
            "title": "ML Platform Engineer",
            "company": "Spotify",
            "location": "London, UK",
            "industry": "Media & Entertainment",
            "match_score": 76,
            "salary": "£75,000 – £100,000",
            "required_skills": ["Python", "Kubernetes", "Docker", "AWS", "ML Pipelines"],
            "missing_skills": ["Java", "Scala", "Kafka"],
            "description": "Build and maintain the ML infrastructure powering personalised recommendations for 500M+ users.",
        },
        {
            "rank": 5,
            "title": "Junior AI Researcher",
            "company": "University of Oxford",
            "location": "Oxford, UK",
            "industry": "Academia",
            "match_score": 58,
            "salary": "£35,000 – £45,000",
            "required_skills": ["Research Publications", "Python", "Deep Learning", "Statistics"],
            "missing_skills": ["PhD", "Research Publications", "LaTeX"],
            "description": "Contribute to groundbreaking NLP research in the university's AI lab. PhD preferred but exceptional MSc candidates considered.",
        },
    ]


def get_demo_insights() -> dict:
    """Return sample career insights."""
    return {
        "top_industries": [
            {"name": "Artificial Intelligence", "count": 42, "percentage": 28},
            {"name": "FinTech", "count": 31, "percentage": 21},
            {"name": "Technology", "count": 28, "percentage": 19},
            {"name": "Healthcare Tech", "count": 18, "percentage": 12},
            {"name": "E-Commerce", "count": 15, "percentage": 10},
            {"name": "Consulting", "count": 10, "percentage": 7},
            {"name": "Other", "count": 6, "percentage": 4},
        ],
        "missing_skills": [
            {"name": "C++", "demand": 85},
            {"name": "Research Publications", "demand": 78},
            {"name": "Java", "demand": 72},
            {"name": "Kubernetes (Advanced)", "demand": 68},
            {"name": "System Design", "demand": 65},
            {"name": "Go", "demand": 58},
            {"name": "MLOps", "demand": 55},
        ],
        "salary": {
            "average": 87500,
            "minimum": 45000,
            "maximum": 145000,
            "distribution": [
                {"range": "£40-60k", "count": 12},
                {"range": "£60-80k", "count": 28},
                {"range": "£80-100k", "count": 35},
                {"range": "£100-120k", "count": 18},
                {"range": "£120k+", "count": 7},
            ],
        },
    }


def get_demo_cover_letter(job: dict, candidate: dict) -> str:
    """Generate a sample cover letter for a job recommendation."""
    name = candidate.get("name", "Candidate")
    company = job.get("company", "the company")
    title = job.get("title", "the position")

    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {title} position at {company}. With a Master's degree in Computer Science from Imperial College London and hands-on experience building production machine learning systems at TechVision Labs, I am confident in my ability to contribute meaningfully to your team.

During my current role as a Machine Learning Engineer, I have designed and deployed ML pipelines serving over 2 million users, with expertise spanning Python, TensorFlow, PyTorch, and cloud infrastructure on AWS. My work on fraud detection models during my internship at FinTech Global achieved 94% precision — demonstrating both my technical depth and business impact orientation.

What particularly excites me about {company} is the opportunity to work at the intersection of cutting-edge research and real-world application. My skills in deep learning, NLP, and scalable system design align closely with the requirements of this role, and I am eager to bring my passion for AI innovation to your organisation.

I would welcome the opportunity to discuss how my background and enthusiasm can contribute to {company}'s continued success. Thank you for considering my application.

Warm regards,
{name}"""


def get_demo_scam_analysis(is_legitimate: bool = True) -> dict:
    """Return sample scam detection results."""
    if is_legitimate:
        return {
            "legitimate_pct": 87,
            "fraudulent_pct": 13,
            "risk_level": "safe",
            "risk_label": "SAFE",
            "risk_icon": "✅",
            "details": [
                "Company verified on Companies House registry",
                "Salary range aligns with market rates",
                "Professional job description with clear requirements",
                "No requests for upfront payment or personal financial info",
            ],
            "flags": [],
        }
    return {
        "legitimate_pct": 22,
        "fraudulent_pct": 78,
        "risk_level": "high",
        "risk_label": "HIGH RISK",
        "risk_icon": "🚨",
        "details": [
            "Unverified company with no online presence",
            "Unrealistic salary for entry-level position",
            "Requests for bank details before interview",
            "Poor grammar and generic job description",
        ],
        "flags": [
            "Upfront payment requested",
            "No company website found",
            "Contact via personal email only",
            "Vague job responsibilities",
        ],
    }
