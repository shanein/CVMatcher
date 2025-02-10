import json
from services.mistral_client import MistralLanguageModel

def create_prompt_for_compatibility(cv_data: dict, job_data: dict) -> str:
    """Crée un prompt structuré pour Mistral afin d'évaluer la compatibilité entre le CV et l'offre d'emploi."""
    return f"""
    Évaluez le CV du candidat par rapport aux exigences de l'offre d'emploi ci-dessous et générez un score de compatibilité.

    **Données du CV du candidat :**
    {json.dumps(cv_data, indent=2, ensure_ascii=False)}
    **Fin de données du CV du candidat**

    **Données de l'offre d'emploi :**
    {json.dumps(job_data, indent=2, ensure_ascii=False)}
    **Fin de données de l'offre du candidat**
    
    
    Critères de compatibilité et pondération du score :
    1. **Compétences** : Attribuez 40% du score total, basé uniquement sur les compétences demandées par l'offre. Les compétences supplémentaires dans le CV mais non demandées doivent être ignorées dans l'évaluation.
    2. **Expérience** : Attribuez 30% du score total, en vérifiant les rôles et l'expérience pertinente pour l'offre, même si les intitulés diffèrent.
    3. **Langues** : Attribuez 15% du score pour la correspondance des langues si une ou plusieurs langues sont spécifiées dans l'offre. Si aucune langue n'est exigée, redistribuez ce pourcentage de manière proportionnelle entre les autres catégories (compétences, expérience, éducation).
    4. **Éducation** : Attribuez 15% du score total pour les diplômes, en fonction de la correspondance exacte avec les diplômes ou domaines d'études demandés dans l'offre.

    Si des intitulés de poste sont différents mais que des compétences ou expériences pertinentes sont présentes, ajustez le score de compatibilité en conséquence.

    Format de réponse attendu (en JSON uniquement) :
    {{
      "match_details": {{
        "skills": {{
          "matched": ["Compétences explicitement demandées dans l'offre d'emploi et trouvées dans le CV ; seules les compétences présentes dans les deux documents doivent être listées ici"],
          "missing": ["Compétences requises dans l'offre et manquantes dans le CV"]
        }},
        "experience": {{
          "years_matched": "Nombre total d'années d'expérience pertinente trouvées",
          "years_missed": "Nombre total d'années d'expérience pertinente manquantes",
          "roles_matched": ["Rôles similaires aux exigences du poste"],
        }},
        "languages": {{
          "matched": ["Langues correspondant aux exigences"],
          "missing": ["Langues manquantes aux exigences"]
        }},
        "education": {{
          "matched": "Diplôme correspondant dans le CV",
          "missing": "Diplôme requis non trouvé dans le CV"
        }}
      }},
      "detailed_score": {{
        "skills": "XX/40% basé sur la correspondance des compétences demandées (ou XX/45% si les langues ne sont pas exigées)",
        "experience": "XX/30% basé sur la correspondance des années et rôles (ou XX/35% si les langues ne sont pas exigées)",
        "languages": "XX/15% du score total (ou exclu du calcul si aucune langue n'est exigée dans l'offre dans ce cas ne pas prendre en compte le score "languages")",
        "education": "XX/15% basé sur les diplômes demandés (ou XX/20% si les langues ne sont pas exigées)"
      }},
      "compatibility_score": "Score XX%",
      "extra_details": "Explications supplémentaires sur le calcul du score de compatibilité, les correspondances et la gestion des langues si non spécifiées."
    }}
    """


def calculate_compatibility(cv_data: dict, job_data: dict, mistral_client: MistralLanguageModel) -> dict:
    """Utilise Mistral pour calculer le score de compatibilité entre un CV et une offre d'emploi."""
    prompt = create_prompt_for_compatibility(cv_data, job_data)
    # print(cv_data)
    # print(job_data)
    compatibility_response = mistral_client.generate(prompt)

    # Vérification que la réponse est bien un JSON structuré, puis on renvoie le résultat
    try:
        compatibility_data = json.loads(compatibility_response)
        return compatibility_data
    except json.JSONDecodeError:
        raise ValueError("La réponse de Mistral n'est pas dans un format JSON valide.", compatibility_response)
