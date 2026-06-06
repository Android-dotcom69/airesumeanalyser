import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;

// --- Auth ---
export const register = (data: { name: string; email: string; password: string }) =>
  api.post("/api/auth/register", data);

export const login = (data: { email: string; password: string }) =>
  api.post("/api/auth/login", data);

// --- Resume ---
export const uploadResume = (file: File) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/api/resume/upload", form);
};

export const listResumes = () => api.get("/api/resume/list");
export const deleteResume = (id: string) => api.delete(`/api/resume/${id}`);

// --- Analysis ---
export const runAnalysis = (resume_id: string, target_role: string) =>
  api.post("/api/analysis/analyze", { resume_id, target_role });

export const getAnalysisHistory = () => api.get("/api/analysis/history");
export const getAnalysis = (id: string) => api.get(`/api/analysis/${id}`);

export const getInterviewQuestions = (
  resume_id: string,
  target_role: string,
  difficulty = "mixed"
) => api.post("/api/analysis/interview-questions", { resume_id, target_role, difficulty });
