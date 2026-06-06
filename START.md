# AI Resume Analyser — Setup Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)
- Anthropic API key (get from console.anthropic.com)

---

## 1. Backend Setup

```bash
cd backend

# Copy env file and fill in your values
copy .env.example .env
# Edit .env: add ANTHROPIC_API_KEY and JWT_SECRET

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the API server
python run.py
# Runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
# Runs at http://localhost:3000
```

---

## 3. Environment Variables

### backend/.env
```
ANTHROPIC_API_KEY=sk-ant-...
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=career_guidance
JWT_SECRET=any-long-random-string-here
FRONTEND_URL=http://localhost:3000
```

### frontend/.env.local (already created)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Project Structure

```
AI resume analyser/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (auth, resume, analysis)
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Claude AI + auth logic
│   │   ├── utils/        # Resume parser + job role data
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── app/
    │   ├── page.tsx        # Landing page
    │   ├── login/          # Login page
    │   ├── register/       # Register page
    │   ├── dashboard/      # Upload + role select
    │   └── analysis/       # Full results page
    ├── lib/
    │   ├── api.ts          # All API calls
    │   └── types.ts        # TypeScript types
    └── .env.local
```

---

## User Flow

1. Register / Login
2. Upload resume (PDF, DOCX, TXT)
3. Select target role
4. Click "Analyse Resume"
5. View: ATS score, strength score, role match %, skill gaps, roadmap, interview questions
