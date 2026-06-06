from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from app.api.deps import get_current_user
from app.database import get_db
from app.utils.resume_parser import extract_text_from_upload
from app.models.schemas import ResumeOut

router = APIRouter(prefix="/api/resume", tags=["resume"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/upload", response_model=ResumeOut)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 5MB.")

    raw_text = await extract_text_from_upload(file)

    db = get_db()
    resume_doc = {
        "user_id": str(current_user["_id"]),
        "filename": file.filename,
        "raw_text": raw_text,
        "uploaded_at": datetime.utcnow(),
    }
    result = await db.resumes.insert_one(resume_doc)

    return ResumeOut(
        id=str(result.inserted_id),
        user_id=resume_doc["user_id"],
        filename=resume_doc["filename"],
        uploaded_at=resume_doc["uploaded_at"],
        raw_text_length=len(raw_text),
    )


@router.get("/list", response_model=list[ResumeOut])
async def list_resumes(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.resumes.find({"user_id": str(current_user["_id"])}).sort("uploaded_at", -1)
    resumes = []
    async for doc in cursor:
        resumes.append(ResumeOut(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            filename=doc["filename"],
            uploaded_at=doc["uploaded_at"],
            raw_text_length=len(doc.get("raw_text", "")),
        ))
    return resumes


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    result = await db.resumes.delete_one({
        "_id": ObjectId(resume_id),
        "user_id": str(current_user["_id"]),
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted"}
