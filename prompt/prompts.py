import json

def prompt_for_cv_extraction(cv_text: str) -> str:
    return f"""
    Voici un CV : {cv_text}.
    Veuillez extraire les informations suivantes et renvoyer un JSON avec la structure exacte suivante :

    Si une information est absente dans la fiche de poste, utilisez `null` pour ce champ, sans remplir avec des valeurs génériques ou de texte par défaut.

    {{
      "personal_information": {{
        "name": "Nom complet",
        "email": "Email",
        "phone": "Téléphone",
        "age": "Âge" (récupérer en format int),
        "social_media": {{
          "linkedin": "URL LinkedIn",
          "twitter": "URL Twitter"
        }}
      }},
      "professional_experience": [
        {{
          "role": "Titre du poste",
          "company": "Nom de l'entreprise",
          "location": "Lieu",
          "duration": {{
            "start_date": "Date de début",
            "end_date": "Date de fin ou 'Présent'"
          }},
          "responsibilities": [
            "Responsabilité 1",
            "Responsabilité 2"
          ]
        }}
      ],
      "education": [
        {{
          "degree": "Diplôme",
          "field_of_study": "Domaine d'étude",
          "institution": "Nom de l'institution",
          "location": "Lieu de l'institution",
          "duration": {{
            "start_date": "Date de début",
            "end_date": "Date de fin"
          }},
          "courses": ["Cours principal 1", "Cours principal 2"]
        }}
      ],
      "skills": {{
        "hard_skills": ["Compétence technique 1", "Compétence technique 2"],
        "soft_skills": ["Compétence personnelle 1", "Compétence personnelle 2"]
      }},
      "hobbies": ["Hobby 1", "Hobby 2"]
    }}

    Respectez cette structure JSON exactement et remplissez les informations en fonction du contenu du CV fourni.
    """

def prompt_for_job_description_extraction(job_text: str) -> str:
    return f"""
    Voici une fiche de poste : {job_text}.
    Veuillez extraire les informations suivantes et renvoyer un JSON avec la structure exacte suivante. Assurez-vous que les valeurs correspondent aux options prédéfinies lorsque cela est spécifié :

    Si une information est absente dans la fiche de poste, utilisez `null` pour ce champ, sans remplir avec des valeurs génériques ou de texte par défaut.

    {{
      "job_information": {{
        "title": "Titre du poste",
        "company": "Nom de l'entreprise",
        "location": {{
          "country": "Pays",
          "city": "Ville",
          "region": "Région",
          "postal_code": "Code postal",
          "address": "Adresse complète"
        }},
        "employment_type": "Type de contrat (choisir parmi : 'CDI', 'CDD', 'Alternance', 'Stage', 'Freelance')",
        "remote_policy": "Travail à distance (choisir parmi : 'Occasionnel', 'Non 100% sur site', 'Télétravail complet')",
        "duration": {{
          "start_date": "Date de début",
          "end_date": "Date de fin ou 'Présent'"
        }},
        "experience_level": "Niveau d'expérience (choisir parmi : 'Débutant/Étudiant', 'Junior', 'Medior', 'Senior', 'Senior+')",
        "compensation": {{
          "salary_range": "Gamme de salaire",
          "currency": "Devise (e.g. 'EUR', 'USD')",
          "bonuses": ["Bonus 1", "Bonus 2"]
        }}
      }},
      "responsibilities": {{
        "responsibilities": [
          "Responsabilité 1",
          "Responsabilité 2"
        ]
      }},
      "skills_required": {{
        "hard_skills": ["Compétence technique 1", "Compétence technique 2"],
        "soft_skills": ["Compétence personnelle 1", "Compétence personnelle 2"],
        "languages": ["Langue 1 (choisir parmi : 'Français', 'Anglais', 'Espagnol', 'Allemand')", "Langue 2"]
      }},
      "work_culture": {{
        "diversity_inclusion": true,
        "flexible_hours": true
      }},
      "benefits": {{
        "benefits": ["Avantage 1 (choisir parmi : 'Tickets Restaurants', 'Remboursement partie de frais de transport')", "Avantage 2"]
      }},
      "additional_information": "Informations supplémentaires"
    }}

    Respectez cette structure JSON exactement et remplissez les informations en fonction du contenu de la fiche de poste fournie. Assurez-vous que les valeurs pour 'employment_type', 'remote_policy', 'experience_level', et 'languages' correspondent aux options prédéfinies.
    """