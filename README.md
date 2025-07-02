
# 🧠 Intelligent Job Application Optimizer

An AI-powered web application to analyze job descriptions, optimize resumes, generate cover letters, and prepare interview questions.

---

## 📦 Project Structure

```
project/
│
├── backend/
│   ├── main.py
│   ├── cover_letter_gen.py
│   ├── interview_prep.py
│   ├── job_analyzer.py
│
├── frontend/
│   ├── index.html
│   ├── JobOptimizerApp.jsx
│   ├── package.json
│
└── # Intelligent Job Application Optimizer.py
```

---

## 🚀 Local Setup Instructions

### 1. Backend (FastAPI)

```bash
cd backend
pip install fastapi uvicorn python-multipart spacy beautifulsoup4 requests openai
python -m spacy download en_core_web_sm
```

Set your OpenAI API key:

```bash
# Windows
set OPENAI_API_KEY=your_key_here

# Linux/macOS
export OPENAI_API_KEY=your_key_here
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend will run on: `http://localhost:8000`

---

### 2. Frontend (React + Parcel)

```bash
cd frontend
npm install
npm run start
```

Frontend will run on: `http://localhost:1234`

---

## 🌐 Deployment Guide

### ✅ Deploy Backend on [Render](https://render.com)

- Create new Web Service
- Use Python 3.10+ environment
- Set start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
- Add environment variable: `OPENAI_API_KEY=your_key_here`
- Copy the live URL (e.g., `https://job-api.onrender.com`)

### ✅ Deploy Frontend on [Netlify](https://netlify.com)

```bash
cd frontend
npm run build
```

- Upload `dist/` folder to Netlify
- In `JobOptimizerApp.jsx`, update:
  ```js
  const backendURL = "https://your-backend.onrender.com";
  ```

---

## ✨ Features

- Analyze Job Description from URL
- Detect keywords/skills
- Upload and Optimize Resume
- Generate Custom Cover Letters
- Prepare with AI-generated Interview Questions

---

## 📬 Contact

Built by Chaitanya Joshi – B.Tech CSE Student  
Feel free to reach out for collaboration or improvements!
