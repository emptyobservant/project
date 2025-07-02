import openai
import asyncio
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_cover_letter(resume_text, job_text):
    prompt = f"""
    Write a personalized cover letter tailored to the job description below using the resume provided.
    Resume:
    {resume_text}

    Job Description:
    {job_text}
    """
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"cover_letter": response.choices[0].message.content.strip()}