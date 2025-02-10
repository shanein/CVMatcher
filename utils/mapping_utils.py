import json
import os
from typing import Dict, Any, List

from colorama import Fore, Style

from models.job_post_model import Language, Benefit
import re

def parse_duration(duration_str: str) -> Dict[str, str]:
    match = re.match(r"(\d{4}) - (\d{4}|\bPrésent\b)", duration_str)
    if match:
        return {"start_date": match.group(1), "end_date": match.group(2)}
    return {"start_date": duration_str, "end_date": None}

def flatten_hobbies(hobbies_data: Any) -> List[str]:
    if isinstance(hobbies_data, list):
        return hobbies_data  # Déjà sous forme de liste
    elif isinstance(hobbies_data, dict):
        # Concatène les valeurs de chaque clé de `hobbies_data` dans une seule liste
        return [hobby for category in hobbies_data.values() for hobby in category]
    return []

def map_to_cv_extraction(data: Dict[str, Any]) -> Dict[str, Any]:
    personal_info = data.get("personal_information", {})
    # age_str = personal_info.get("age", "0").split()[0]
    # age = int(age_str) if age_str.isdigit() else 0

    mapped_data = {
        "personal_information": {
            "name": personal_info.get("name", ""),
            "email": personal_info.get("email", ""),
            "phone": personal_info.get("phone", ""),
            "age": personal_info.get("age", ""),
            "social_media": personal_info.get("social_media", {})
        },
        "professional_experience": [
            {
                "role": exp.get("role", ""),
                "company": exp.get("company", ""),
                "location": exp.get("location", ""),
                "duration": (
                    parse_duration(exp["duration"]) if isinstance(exp.get("duration"), str)
                    else {
                        "start_date": exp.get("duration", {}).get("start_date", ""),
                        "end_date": exp.get("duration", {}).get("end_date", "")
                    }
                ),
                "responsibilities": exp.get("responsibilities", [])
            } for exp in data.get("professional_experience", [])
        ],
        "education": [
            {
                "degree": edu.get("degree", ""),
                "field_of_study": edu.get("field_of_study", ""),
                "institution": edu.get("institution", ""),
                "location": edu.get("location", ""),
                "duration": (
                    parse_duration(edu["duration"]) if isinstance(edu.get("duration"), str)
                    else {
                        "start_date": edu.get("duration", {}).get("start_date", ""),
                        "end_date": edu.get("duration", {}).get("end_date", "")
                    }
                ),
                "courses": edu.get("courses", [])
            } for edu in data.get("education", [])
        ],
        "skills": {
            "hard_skills": data.get("skills", {}).get("hard_skills", []),
            "soft_skills": data.get("skills", {}).get("soft_skills", [])
        },
        # Conversion des hobbies en une liste plate
        "hobbies": flatten_hobbies(data.get("hobbies", []))
    }
    return mapped_data

def map_to_job_description_extraction(data: Dict[str, Any]) -> Dict[str, Any]:
    job_info = data.get("job_information", {})
    location = job_info.get("location", {})
    duration = job_info.get("duration", {})
    compensation = job_info.get("compensation", {})

    def empty_to_none(value):
        return value if value != "" else None

    mapped_data = {
        "job_information": {
            "title": job_info.get("title", ""),
            "company": job_info.get("company", ""),
            "location": {
                "country": location.get("country", ""),
                "city": location.get("city", ""),
                "region": location.get("region", ""),
                "postal_code": location.get("postal_code", ""),
                "address": location.get("address", "")
            },
            "employment_type": empty_to_none(job_info.get("employment_type", "")),
            "remote_policy": empty_to_none(job_info.get("remote_policy", "")),
            "duration": {
                "start_date": duration.get("start_date", ""),
                "end_date": duration.get("end_date", "")
            },
            "experience_level": empty_to_none(job_info.get("experience_level", "")),
            "compensation": {
                "salary_range": compensation.get("salary_range", ""),
                "currency": compensation.get("currency", ""),
                "bonuses": compensation.get("bonuses", [])
            }
        },
        "responsibilities": {
            "responsibilities": data.get("responsibilities", {}).get("responsibilities", [])
            if isinstance(data.get("responsibilities", {}).get("responsibilities", []), list) 
            else [data.get("responsibilities", {}).get("responsibilities", "")]
        },
        "skills_required": {
            "hard_skills": data.get("skills_required", {}).get("hard_skills", []),
            "soft_skills": data.get("skills_required", {}).get("soft_skills", []),
            "languages": [
                lang for lang in data.get("skills_required", {}).get("languages", [])
                if lang in Language.__members__
            ]
        },
        "work_culture": {
            "diversity_inclusion": data.get("work_culture", {}).get("diversity_inclusion", None),
            "flexible_hours": data.get("work_culture", {}).get("flexible_hours", None)
        },
        "benefits": {
            "benefits": [
                benefit for benefit in data.get("benefits", [])
                if benefit in Benefit.__members__
            ]
        },
        "additional_information": data.get("additional_information", "")
    }
    return mapped_data


def save_to_file(data, filename, destination):
    # Création du dossier de destination s'il n'existe pas
    os.makedirs(destination, exist_ok=True)

    # Chemin complet du fichier
    filepath = os.path.join(destination, filename)

    # Gestion de l'écriture en fonction du type de `data`
    with open(filepath, "w", encoding="utf-8") as file:
        if isinstance(data, dict):
            # Si `data` est un dictionnaire, on le convertit en JSON
            json.dump(data, file, ensure_ascii=False, indent=4)
        elif isinstance(data, str):
            # Si `data` est une chaîne, on l'écrit directement
            file.write(data)
        else:
            raise TypeError("Le type de `data` n'est pas pris en charge. Utilisez `str` ou `dict`.")

    print(f"{Fore.GREEN}Data successfully saved to {filepath}{Style.RESET_ALL}")
