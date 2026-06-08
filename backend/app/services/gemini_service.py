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

    prompt = f"""You are analyzing a resume for the role: "{target_role}".

ROLE REQUIREMENTS (use ONLY these to judge skills):
{role_req}

RESUME TEXT (read carefully — every skill mentioned counts):
{resume_text}

Follow these steps IN ORDER to build your JSON response:

STEP 1 — Extract skills: Read the entire resume and list every technical skill, tool, language, framework, or technology mentioned. Be thorough — include everything explicitly stated.

STEP 2 — Match skills: Compare your extracted skills against the role requirements above. A skill is "matched" if it appears (or a close synonym appears) in BOTH the resume AND the role requirements list.

STEP 3 — Find missing skills: List only the required skills (core + important) that are genuinely absent from the resume.

STEP 4 — Calculate scores using these EXACT formulas:
- match_percentage = round((number of matched_skills / total core+important skills) * 100)
- ats_score = start at 50, add 5 for each ATS keyword found in resume, cap at 95. If matched_skills has 5+ items, minimum ats_score is 65.
- strength_score = based on impact statements, numbers/metrics in resume, and action verbs (0-100)

STEP 5 — Build skill_gaps: ONLY include skills that are in missing_skills. If missing_skills is empty, skill_gaps MUST be [].

Now return ONLY a valid JSON object with this exact structure (no markdown, no extra text):
{{
  "ats_score": <integer 0-100, derived from Step 4>,
  "strength_score": <integer 0-100, derived from Step 4>,
  "match_percentage": <integer 0-100, derived from Step 4 formula>,
  "extracted_skills": [<all skills found in resume from Step 1>],
  "matched_skills": [<skills present in BOTH resume and role requirements from Step 2>],
  "missing_skills": [<required skills NOT found in resume from Step 3>],
  "skill_gaps": [
    {{
      "skill": "<must be from missing_skills only>",
      "importance": "<critical|important|nice-to-have>",
      "resources": ["<specific course name + platform>", "<specific resource>"]
    }}
  ],
  "ats_feedback": [<3-5 specific, actionable ATS improvement tips>],
  "strengths": [<3-5 specific strengths visible in this resume>],
  "weaknesses": [<3-5 specific weaknesses or gaps in this resume>],
  "summary": "<2-3 sentence honest overall assessment>"
}}"""

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
