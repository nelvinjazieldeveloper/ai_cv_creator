from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests

app = FastAPI()

# Configuración de Gemini AI (reemplaza con tu API key real)
API_KEY = "AIzaSyAjVwQIUl3LLGkOA_j8hY8k7S-EQN1FCRg"
MODEL = "gemini-1.5-pro-latest"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str
    description: str

class Education(BaseModel):
    degree: str
    institution: str
    year: int

class CVRequest(BaseModel):
    full_name: str
    profession: str
    email: str
    phone: Optional[str] = None
    location: str
    linkedin: Optional[str] = None
    experiences: List[Experience]
    education: List[Education]
    skills: str
    languages: str
    job_target: Optional[str] = None

@app.post("/generate-cv")
async def generate_cv(cv_data: CVRequest):
    try:
        prompt = f"""
        Generate a professional Europass-style CV in Markdown format using this data:
        
        **Personal Information:**
        - Name: {cv_data.full_name}
        - Profession: {cv_data.profession}
        - Location: {cv_data.location}
        - Email: {cv_data.email}
        - Phone: {cv_data.phone or 'Not specified'}
        - LinkedIn: {cv_data.linkedin or 'Not specified'}
        
        **Work Experience:**
        {"".join(
            f"\n- **{exp.title}** at {exp.company} ({exp.start_date} - {exp.end_date})\n"
            f"  {exp.description}\n"
            for exp in cv_data.experiences
        )}
        
        **Education:**
        {"".join(
            f"\n- {edu.degree} - {edu.institution} ({edu.year})"
            for edu in cv_data.education
        )}
        
        **Skills:**
        {cv_data.skills}
        
        **Languages:**
        {cv_data.languages}
        
        Format requirements:
        - Use Markdown syntax
        - Section headers with ##
        - Bullet points for lists
        - Empty line between sections
        - Professional tone
        - Focus on achievements
        """
        
        headers = {"Content-Type": "application/json"}
        params = {"key": API_KEY}
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)
        
        if response.status_code == 200:
            return {
                "cv_markdown": response.json()["candidates"][0]["content"]["parts"][0]["text"],
                "status": "success"
            }
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))