from groq import Groq
import json
from app.config import settings
from app.utils.job_roles import JOB_ROLE_REQUIREMENTS

client = Groq(api_key=settings.groq_api_key)
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are an expert career counselor and technical recruiter with 15 years of experience
reviewing resumes for top tech companies. You provide precise, actionable, and honest feedback.
Always respond with valid JSON matching the exact schema requested. Never include markdown fences or extra text.
Return ONLY the raw JSON object, nothing else."""


def _role_context(role: str) -> str:
    req = JOB_ROLE_REQUIREMENTS.get(role, {})
    return json.dumps(req, indent=2)


def _clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def _chat(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    return response.choices[0].message.content


async def analyze_resume(resume_text: str, target_role: str) -> dict:
    role_req = _role_context(target_role)

    prompt = f"""Analyze this resume for the target role of "{target_role}".

ROLE REQUIREMENTS:
{role_req}

RESUME TEXT:
{resume_text}

Return a JSON object with EXACTLY this structure:
{{
  "ats_score": <integer 0-100>,
  "strength_score": <integer 0-100>,
  "match_percentage": <integer 0-100>,
  "extracted_skills": [<list of skills found in resume>],
  "matched_skills": [<skills from resume that match role requirements>],
  "missing_skills": [<required skills not found in resume>],
  "skill_gaps": [
    {{
      "skill": "<skill name>",
      "importance": "<critical|important|nice-to-have>",
      "resources": ["<resource 1>", "<resource 2>"]
    }}
  ],
  "ats_feedback": [<3-5 specific ATS improvement tips as strings>],
  "strengths": [<3-5 specific strengths from this resume>],
  "weaknesses": [<3-5 specific weaknesses or gaps>],
  "summary": "<2-3 sentence overall assessment>"
}}

Scoring guidance:
- ats_score: Based on keyword density, formatting clarity, section headers, no tables/graphics in text
- strength_score: Based on impact statements, quantified achievements, relevance to role
- match_percentage: Percentage of core+important skills present"""

    return json.loads(_clean_json(_chat(prompt)))


async def generate_roadmap(resume_text: str, target_role: str, missing_skills: list[str]) -> list[dict]:
    prompt = f"""Create a personalized learning roadmap for someone targeting "{target_role}".

Their resume shows they need to learn: {', '.join(missing_skills[:10])}

Return a JSON array of roadmap phases with EXACTLY this structure:
[
  {{
    "phase": 1,
    "title": "<phase title>",
    "duration_weeks": <integer>,
    "goals": ["<goal 1>", "<goal 2>"],
    "skills_to_learn": ["<skill 1>", "<skill 2>"],
    "projects": ["<concrete project idea 1>", "<concrete project idea 2>"],
    "courses": ["<course/resource name + platform>", "<course name + platform>"]
  }}
]

Create 3-4 phases totaling 12-20 weeks. Be specific — name actual courses (e.g., "CS50 on edX"),
real project ideas, and concrete skills. Prioritize the most impactful gaps first."""

    return json.loads(_clean_json(_chat(prompt)))


async def generate_interview_questions(resume_text: str, target_role: str, difficulty: str = "mixed") -> list[str]:
    prompt = f"""Generate 10 interview questions for a "{target_role}" candidate based on their resume.

RESUME:
{resume_text[:3000]}

Difficulty: {difficulty}
Mix of: technical questions (role-specific), behavioral questions (STAR format),
and resume-specific questions (based on what they listed).

Return a JSON array of exactly 10 strings, each being a complete interview question.
Example format: ["Tell me about a time you...", "How would you design...", ...]"""

    return json.loads(_clean_json(_chat(prompt)))
