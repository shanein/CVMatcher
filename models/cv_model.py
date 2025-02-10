from pydantic import BaseModel
from typing import Optional, List, Dict

class Duration(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_duration: Optional[str] = None

class PersonalInformation(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    social_media: Optional[Dict[str, Optional[str]]] = None

class Experience(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[Duration] = None
    responsibilities: Optional[List[str]] = None

class Education(BaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[Duration] = None
    courses: Optional[List[str]] = None

class Skills(BaseModel):
    hard_skills: Optional[List[str]] = None
    soft_skills: Optional[List[str]] = None

class CVExtraction(BaseModel):
    personal_information: Optional[PersonalInformation] = None
    professional_experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    skills: Optional[Skills] = None
    hobbies: Optional[List[str]] = None