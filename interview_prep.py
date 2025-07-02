import openai
import asyncio
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_interview_questions(job_text):
    prompt = f"""
    Generate a list of 5 technical and 5 behavioral interview questions based on this job description:
    {job_text}
    """
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"questions": [q for q in response.choices[0].message.content.strip().split("\n") if q.strip()]}