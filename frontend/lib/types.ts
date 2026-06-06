export type JobRole = string; // free text — any job role

export interface SkillGap {
  skill: string;
  importance: "critical" | "important" | "nice-to-have";
  resources: string[];
}

export interface RoadmapPhase {
  phase: number;
  title: string;
  duration_weeks: number;
  goals: string[];
  skills_to_learn: string[];
  projects: string[];
  courses: string[];
}

export interface AnalysisResult {
  resume_id: string;
  target_role: JobRole;
  ats_score: number;
  strength_score: number;
  match_percentage: number;
  extracted_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  skill_gaps: SkillGap[];
  ats_feedback: string[];
  strengths: string[];
  weaknesses: string[];
  roadmap: RoadmapPhase[];
  interview_questions: string[];
  summary: string;
  created_at: string;
}

export interface Resume {
  id: string;
  filename: string;
  uploaded_at: string;
  raw_text_length: number;
}
