from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from app.api.deps import get_current_user
from app.database import get_db
from app.models.schemas import AnalysisRequest, AnalysisResult, InterviewQuestionRequest
from app.services.gemini_service import analyze_resume, generate_roadmap, generate_interview_questions

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResult)
async def run_analysis(payload: AnalysisRequest, current_user: dict = Depends(get_current_user)):
    db = get_db()

    resume = await db.resumes.find_one({
        "_id": ObjectId(payload.resume_id),
        "user_id": str(current_user["_id"]),
    })
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    raw_text = resume["raw_text"]
    role = payload.target_role

    analysis_data = await analyze_resume(raw_text, role)

    # ── Server-side consistency correction ──────────────────────────────────
    matched = analysis_data.get("matched_skills", [])
    missing = analysis_data.get("missing_skills", [])
    total_required = len(matched) + len(missing)

    # Recalculate match_percentage from actual skill lists
    if total_required > 0:
        analysis_data["match_percentage"] = round(len(matched) / total_required * 100)
    else:
        analysis_data["match_percentage"] = 0

    # ATS score must be proportional: can't be high if no matched skills
    if len(matched) == 0 and analysis_data.get("ats_score", 0) > 50:
        analysis_data["ats_score"] = min(analysis_data["ats_score"], 45)

    # skill_gaps must only contain skills from missing_skills
    missing_set = set(s.lower() for s in missing)
    analysis_data["skill_gaps"] = [
        gap for gap in analysis_data.get("skill_gaps", [])
        if gap.get("skill", "").lower() in missing_set
    ]
    # If no missing skills, clear skill_gaps entirely
    if not missing:
        analysis_data["skill_gaps"] = []
    # ────────────────────────────────────────────────────────────────────────

    roadmap = await generate_roadmap(raw_text, role, missing)
    questions = await generate_interview_questions(raw_text, role)

    result_doc = {
        "resume_id": payload.resume_id,
        "user_id": str(current_user["_id"]),
        "target_role": role,
        "created_at": datetime.utcnow(),
        **analysis_data,
        "roadmap": roadmap,
        "interview_questions": questions,
    }

    await db.analyses.insert_one(result_doc)

    return AnalysisResult(
        resume_id=payload.resume_id,
        target_role=payload.target_role,
        ats_score=analysis_data["ats_score"],
        strength_score=analysis_data["strength_score"],
        match_percentage=analysis_data["match_percentage"],
        extracted_skills=analysis_data["extracted_skills"],
        matched_skills=analysis_data["matched_skills"],
        missing_skills=analysis_data["missing_skills"],
        skill_gaps=analysis_data["skill_gaps"],
        ats_feedback=analysis_data["ats_feedback"],
        strengths=analysis_data["strengths"],
        weaknesses=analysis_data["weaknesses"],
        roadmap=roadmap,
        interview_questions=questions,
        summary=analysis_data["summary"],
        created_at=result_doc["created_at"],
    )


@router.get("/history")
async def get_analysis_history(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.analyses.find(
        {"user_id": str(current_user["_id"])},
        {"raw_text": 0}
    ).sort("created_at", -1).limit(20)

    history = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        history.append(doc)
    return history


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    doc = await db.analyses.find_one({
        "_id": ObjectId(analysis_id),
        "user_id": str(current_user["_id"]),
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Analysis not found")
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/interview-questions")
async def get_interview_questions(
    payload: InterviewQuestionRequest,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    resume = await db.resumes.find_one({
        "_id": ObjectId(payload.resume_id),
        "user_id": str(current_user["_id"]),
    })
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    questions = await generate_interview_questions(
        resume["raw_text"], payload.target_role.value, payload.difficulty
    )
    return {"questions": questions}
