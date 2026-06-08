"use client";
import Link from "next/link";
import { Brain, FileText, Target, Map, MessageSquare, TrendingUp } from "lucide-react";

const features = [
  { icon: FileText, title: "Resume Parsing", desc: "Upload PDF, DOCX or TXT — we extract everything automatically" },
  { icon: Target, title: "ATS Score", desc: "See how well your resume passes Applicant Tracking Systems" },
  { icon: TrendingUp, title: "Skill Gap Detection", desc: "Know exactly which skills you're missing for your target role" },
  { icon: Map, title: "Career Roadmap", desc: "Get a personalized week-by-week learning plan with real courses" },
  { icon: MessageSquare, title: "Interview Prep", desc: "AI-generated questions tailored to your resume and role" },
  { icon: Brain, title: "Powered by Groq AI", desc: "Built on Groq's Llama 3.3 for fast, accurate career feedback" },
];


export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-950">
      <nav className="border-b border-gray-800 px-6 py-4 flex justify-between items-center">
        <span className="text-xl font-bold text-indigo-400">AI Resume Analyser</span>
        <div className="flex gap-3">
          <Link href="/login" className="px-4 py-2 text-sm text-gray-300 hover:text-white transition">Login</Link>
          <Link href="/register" className="px-4 py-2 text-sm bg-indigo-600 hover:bg-indigo-500 rounded-lg transition">Get Started</Link>
        </div>
      </nav>

      <section className="max-w-4xl mx-auto px-6 py-24 text-center">
        <div className="inline-block px-3 py-1 mb-6 text-xs font-medium bg-indigo-900/50 text-indigo-300 rounded-full border border-indigo-800">
          Powered by Groq AI — Free & Fast
        </div>
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
          AI-Powered Career Intelligence
        </h1>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
          Upload your resume, pick a target role, and get instant ATS scores, skill gap analysis,
          a personalized learning roadmap, and interview questions — all in one place.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link href="/login" className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-medium transition text-lg">
            Analyse My Resume
          </Link>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-6 pb-16 text-center">
        <p className="text-2xl font-semibold text-gray-200 leading-snug">
          Stop guessing. Start growing.{" "}
          <span className="text-indigo-400">Know exactly where you stand</span> — and the fastest path to where you want to be.
        </p>
      </section>

      <section className="max-w-5xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Everything you need to land the role</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-indigo-800 transition">
              <Icon className="w-8 h-8 text-indigo-400 mb-3" />
              <h3 className="font-semibold mb-2">{title}</h3>
              <p className="text-sm text-gray-400">{desc}</p>
            </div>
          ))}
        </div>
      </section>

    </main>
  );
}
