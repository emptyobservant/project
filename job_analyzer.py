from bs4 import BeautifulSoup
import requests
import spacy
import asyncio

nlp = spacy.load("en_core_web_sm")

async def analyze_job_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except requests.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(html, 'html.parser')
    job_text = soup.get_text()

    doc = nlp(job_text)
    skills = [ent.text for ent in doc.ents if ent.label_.lower() in ["skill", "work_of_art"]]

    return {
        "raw_text": job_text[:1000],
        "skills": skills[:15],
    }