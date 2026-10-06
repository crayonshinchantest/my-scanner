"""Resume-derived profile used to score how well a job matches you.

These keywords were extracted from Ajinkya Kolhe's current resume set
(Business Analyst / Digital Transformation / Consulting track — EY, IBM,
McKinsey, SCG, Glide Brands, IIM Visakhapatnam variants). Add or remove terms
here to tune matching — the more a job description overlaps with these, the
higher it scores.
"""

# Strong signals — weighted heavily when they appear in a job.
CORE_SKILLS = [
    "business analyst", "business analysis", "consultant", "consulting",
    "digital transformation", "business transformation", "transformation",
    "process improvement", "process transformation", "process mapping",
    "process mining", "process digitalization", "workflow automation",
    "solution design", "functional consultant", "implementation",
    "requirements gathering", "business requirements", "stakeholder management",
    "change management", "lean six sigma", "aris", "sop", "standardization",
    "business case", "feasibility", "program management", "pmo",
    "project coordination", "dependency tracking", "kpi", "dashboard",
    "mis", "management reporting", "erp", "sap", "power bi", "excel",
    "sql", "python", "data analysis", "analytics",
]

# Softer signals — nice to have, lightly weighted.
SUPPORTING = [
    "mba", "iim", "stakeholder", "cross-functional", "cross functional",
    "roadmap", "leadership", "presentation", "research", "market research",
    "operations", "strategy", "automation", "ai", "llm", "system integration",
    "data pipeline", "benchmarking", "vendor management", "procurement",
    "client management", "advisory", "problem solving", "structured thinking",
]

# If a job title contains any of these, it's clearly in your lane.
# Tier 1 (your stated primary targets) gets the heaviest weight via repeats
# in CORE_SKILLS matching; everything here still boosts the title score.
TITLE_BOOST = [
    "associate consultant", "consulting analyst", "business analyst",
    "technology consultant", "technology business analyst",
    "digital transformation", "transformation analyst",
    "solutions consultant", "functional consultant", "implementation consultant",
    "product analyst", "business systems analyst", "process transformation",
    "strategy analyst", "business strategy", "ceo office", "operations strategy",
    "management trainee", "pmo analyst", "chief of staff", "founder's office",
    "consultant", "analyst",
]

# Jobs with these in the title are almost never a fit — filter them out.
NEGATIVE_TITLE = [
    "sales executive", "telecaller", "telesales", "field sales", "delivery",
    "driver", "nurse", "security guard", "electrician", "plumber",
    "software engineer", "software developer", "devops", "qa engineer", "sdet",
    "civil engineer", "mechanical engineer", "data entry", "bpo", "customer support",
    "frontend", "backend", "full stack", "firmware",
]

# Seniority you're targeting (MBA 2026 grad / early career).
PREFERRED_SENIORITY = ["associate", "analyst", "manager", "specialist", "lead",
                       "executive", "senior", "consultant", "trainee", "graduate"]
