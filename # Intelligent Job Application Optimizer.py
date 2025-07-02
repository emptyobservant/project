# --- main.py ---
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from job_analyzer import analyze_job_description
from resume_optimizer import optimize_resume
from cover_letter_gen import generate_cover_letter
from interview_prep import generate_interview_questions
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Intelligent Job Application Optimizer",
              description="AI-powered tools for job application enhancement",
              version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-job")
async def analyze_job(job_url: str = Form(...)):
    try:
        return await analyze_job_description(job_url)
    except Exception as e:
        logger.error(f"Job analysis failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/optimize-resume")
async def optimize(user_resume: UploadFile, job_text: str = Form(...)):
    try:
        resume_content = await user_resume.read()
        return await optimize_resume(resume_content.decode(), job_text)
    except Exception as e:
        logger.error(f"Resume optimization failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-cover-letter")
async def generate_letter(user_resume: UploadFile, job_text: str = Form(...)):
    try:
        resume_content = await user_resume.read()
        return await generate_cover_letter(resume_content.decode(), job_text)
    except Exception as e:
        logger.error(f"Cover letter generation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/interview-prep")
async def prep(job_text: str = Form(...)):
    try:
        return await generate_interview_questions(job_text)
    except Exception as e:
        logger.error(f"Interview prep failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# --- job_analyzer.py ---
from bs4 import BeautifulSoup
import requests
import spacy
from typing import Dict, Any
import re

nlp = spacy.load("en_core_web_sm")

async def analyze_job_description(url: str) -> Dict[str, Any]:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        job_text = soup.get_text()
        # Clean up text
        job_text = re.sub(r'\s+', ' ', job_text).strip()
        
        doc = nlp(job_text)
        
        # Extract skills (for production, consider training a custom NER model)
        skills = []
        for token in doc:
            if token.pos_ == "PROPN" or token.pos_ == "NOUN":
                skills.append(token.text)
        
        return {
            "raw_text": job_text[:1000] + "..." if len(job_text) > 1000 else job_text,
            "skills": list(set(skills))[:15],  # Remove duplicates
            "word_count": len(job_text.split())
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch job description: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- resume_optimizer.py ---
import openai
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

async def optimize_resume(resume_text: str, job_text: str) -> Dict[str, Any]:
    try:
        prompt = f"""
        Optimize this resume for the following job description.
        Focus on:
        - Matching keywords from the job description
        - Highlighting relevant experience
        - Maintaining original structure
        - Keeping it concise
        
        Resume:
        {resume_text}

        Job Description:
        {job_text}
        
        Return only the optimized resume text.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        optimized_text = response.choices[0].message.content
        return {"optimized_resume": optimized_text}
        
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=503, detail="AI service unavailable")
    except Exception as e:
        logger.error(f"Resume optimization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- cover_letter_gen.py ---
import openai
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

async def generate_cover_letter(resume_text: str, job_text: str) -> Dict[str, Any]:
    try:
        prompt = f"""
        Write a professional, concise cover letter (3-4 paragraphs) that:
        1. Matches the candidate's skills from the resume with the job requirements
        2. Highlights 2-3 most relevant experiences
        3. Shows enthusiasm for the specific role
        4. Uses formal but modern business language
        
        Resume:
        {resume_text}

        Job Description:
        {job_text}
        
        Return only the cover letter text.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        cover_letter = response.choices[0].message.content
        return {"cover_letter": cover_letter}
        
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=503, detail="AI service unavailable")
    except Exception as e:
        logger.error(f"Cover letter generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- interview_prep.py ---
import openai
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

async def generate_interview_questions(job_text: str) -> Dict[str, List[str]]:
    try:
        prompt = f"""
        Generate interview questions based on this job description.
        Format:
        1. 5 technical questions specific to the role's requirements
        2. 5 behavioral questions assessing soft skills
        3. 2 situational questions about work scenarios
        
        Job Description:
        {job_text}
        
        Return as a numbered list with clear separation between categories.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000
        )
        
        questions = response.choices[0].message.content.split("\n")
        # Filter out empty lines
        questions = [q.strip() for q in questions if q.strip()]
        return {"questions": questions}
        
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=503, detail="AI service unavailable")
    except Exception as e:
        logger.error(f"Question generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))