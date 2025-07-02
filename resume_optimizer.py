import openai
import asyncio
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def optimize_resume(resume_text, job_text):
    prompt = f"""
    Optimize this resume for the following job description.
    Resume:
    {resume_text}

    Job Description:
    {job_text}
    """
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"optimized_resume": response.choices[0].message.content.strip()}