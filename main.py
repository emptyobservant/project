from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from job_analyzer import analyze_job_description
from resume_optimizer import optimize_resume
from cover_letter_gen import generate_cover_letter
from interview_prep import generate_interview_questions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-job")
async def analyze_job(job_url: str = Form(...)):
    return await analyze_job_description(job_url)

@app.post("/optimize-resume")
async def optimize(user_resume: UploadFile, job_text: str = Form(...)):
    resume_content = await user_resume.read()
    return await optimize_resume(resume_content.decode(), job_text)

@app.post("/generate-cover-letter")
async def generate_letter(user_resume: UploadFile, job_text: str = Form(...)):
    resume_content = await user_resume.read()
    return await generate_cover_letter(resume_content.decode(), job_text)

@app.post("/interview-prep")
async def prep(job_text: str = Form(...)):
    return await generate_interview_questions(job_text)