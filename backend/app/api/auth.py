from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId
from app.models.schemas import UserCreate, UserLogin, Token, UserOut
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate):
    db = get_db()
    if await db.users.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "created_at": datetime.utcnow(),
    }
    result = await db.users.insert_one(user_doc)
    return UserOut(
        id=str(result.inserted_id),
        name=user_doc["name"],
        email=user_doc["email"],
        created_at=user_doc["created_at"],
    )


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    db = get_db()
    user = await db.users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user["_id"])})
    return Token(access_token=token)
