"""Pick which of Ajinkya's tailored resumes best fits a given job.

Each entry maps a resume file (inside the local "resumes/" folder, gitignored
— it never gets pushed to the public repo) to the kind of role it was
tailored for. For every job we score all resumes by how well the job's
title/description/company matches their keywords, and recommend the best.
The general resume wins when no specialist resume clearly fits.
"""
from __future__ import annotations

# weight 1 = broad/general resume, weight 2 = specialist (wins when relevant)
CATALOG = [
    {"label": "Business Analyst — general (IIM Visakhapatnam)", "weight": 1,
     "path": "resumes/Ajinkya_Kolhe_IIM_Visakhapatnam_Resume.pdf",
     "kw": ["business analyst", "transformation analyst", "program coordination",
            "process transformation", "stakeholder management",
            "management reporting", "pmo", "decision analytics"]},

    {"label": "Business Analyst — Change & Transformation (IBM style)", "weight": 2,
     "path": "resumes/IBM_changetrans_Ajinkya_Kolhe_IIM_Visakhapatnam_Resume.pdf",
     "kw": ["technology business analyst", "business systems analyst",
            "change management", "digital solution design", "business analysis",
            "ibm", "accenture", "capgemini", "publicis sapient", "thoughtworks",
            "infosys consulting", "cognizant consulting", "requirements gathering"]},

    {"label": "Business Transformation Manager (EY style)", "weight": 2,
     "path": "resumes/Ajinkya_Kolhe_EY_Business_Transformation_Manager.pdf",
     "kw": ["business transformation manager", "transformation manager",
            "associate consultant", "consulting analyst", "business case",
            "feasibility", "process diagnostics", "deloitte", "pwc", "kpmg",
            "ey", "ernst", "parthenon", "strategy&", "big 4", "member firm"]},

    {"label": "Digital Transformation Officer (SCG style)", "weight": 2,
     "path": "resumes/Ajinkya_Kolhe_SCG_Digital_Transformation_Officer.pdf",
     "kw": ["digital transformation analyst", "digital transformation officer",
            "process transformation analyst", "erp", "sap", "digitalization",
            "process digitalization", "siemens", "schneider", "honeywell",
            "johnson controls", "software ag", "aris", "process mining"]},

    {"label": "Founder's Office / CEO Office (Glide Brands style)", "weight": 2,
     "path": "resumes/Ajinkya_Kolhe_Glide_Brands_Founders_Office.pdf",
     "kw": ["founder's office", "founders office", "ceo office", "chief of staff",
            "product analyst", "internal tools", "llm", "automation anywhere",
            "uipath", "celonis", "workflow automation", "startup"]},

    {"label": "Solutions / Data Analyst (McKinsey AI Solutions style)", "weight": 2,
     "path": "resumes/Ajinkya_Kolhe_McKinsey_AI_Solutions_Analyst.pdf",
     "kw": ["solutions consultant", "business systems analyst", "product analyst",
            "ai solutions", "analytics automation", "dashboards", "benchmarking",
            "zs associates", "gartner", "data analyst", "financial services"]},

    {"label": "Strategy / Associate Consultant (McKinsey Associate style)", "weight": 2,
     "path": "resumes/Ajinkya_Kolhe_McKinsey_Associate_Intern.pdf",
     "kw": ["strategy analyst", "business strategy analyst", "operations strategy",
            "associate consultant", "consulting analyst", "market assessment",
            "market sizing", "case study", "mckinsey", "bain", "boston consulting",
            "bcg", "kearney", "oliver wyman", "roland berger", "primary research"]},
]

_FALLBACK = CATALOG[0]  # Business Analyst — general


def recommend(title: str, description: str, company: str = "") -> tuple[str, str]:
    """Return (resume_label, resume_path) best suited to this job."""
    text = f"{title} {description} {company}".lower()
    best = _FALLBACK
    best_score = 0
    for entry in CATALOG:
        score = sum(entry["weight"] for kw in entry["kw"] if kw in text)
        if score > best_score:
            best_score, best = score, entry
    return best["label"], best["path"]
