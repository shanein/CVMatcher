from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

class ContractType(str, Enum):
    CDI = "CDI"
    CDD = "CDD"
    Alternance = "Alternance"
    Stage = "Stage"
    Freelance = "Freelance"

class EducationLevel(str, Enum):
    Bac = "Bac"
    Bac_1 = "Bac+1"
    Bac_2 = "Bac+2"
    Bac_3 = "Bac+3"
    Bac_4 = "Bac+4"
    Bac_5 = "Bac+5"
    No_Degree = "Pas d'études"
    Bac_Pro = "Bac Pro"

class Language(str, Enum):
    French = "Français"
    English = "Anglais"
    Spanish = "Espagnol"
    German = "Allemand"

class ExperienceLevel(str, Enum):
    Beginner = "Débutant/Étudiant"
    Junior = "Junior"
    Medior = "Medior"
    Senior = "Senior"
    SeniorPlus = "Senior+"

class RemotePolicy(str, Enum):
    Occasional = "Occasionnel"
    OnSite = "Non 100% sur site"
    FullRemote = "Télétravail complet"

class Benefit(str, Enum):
    MealVouchers = "Tickets Restaurants"
    TransportReimbursement = "Remboursement partie de frais de transport"

class Duration(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Compensation(BaseModel):
    salary_range: Optional[str] = None
    currency: Optional[str] = None
    bonuses: Optional[List[str]] = None

class Location(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    address: Optional[str] = None

class JobInformation(BaseModel):
    title: Optional[str] = None  # Rend le titre optionnel
    company: Optional[str] = None
    location: Optional[Location] = None
    employment_type: Optional[ContractType] = None
    remote_policy: Optional[RemotePolicy] = None
    duration: Optional[Duration] = None
    experience_level: Optional[ExperienceLevel] = None
    compensation: Optional[Compensation] = None

class Responsibilities(BaseModel):
    responsibilities: Optional[List[str]] = None  # Rend les responsabilités optionnelles

class SkillsRequired(BaseModel):
    hard_skills: Optional[List[str]] = None  # Rend les compétences techniques optionnelles
    soft_skills: Optional[List[str]] = None  # Rend les compétences personnelles optionnelles
    languages: Optional[List[Language]] = None

class WorkCulture(BaseModel):
    diversity_inclusion: Optional[bool] = None
    flexible_hours: Optional[bool] = None

class Benefits(BaseModel):
    benefits: Optional[List[Benefit]] = None  # Rend les avantages optionnels

class JobDescriptionExtraction(BaseModel):
    job_information: Optional[JobInformation] = None
    responsibilities: Optional[Responsibilities] = None
    skills_required: Optional[SkillsRequired] = None
    work_culture: Optional[WorkCulture] = None
    benefits: Optional[Benefits] = None
    additional_information: Optional[str] = None