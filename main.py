from colorama import Fore, Style
from config.settings import API_KEY
from models.cv_model import CVExtraction
from models.job_post_model import JobDescriptionExtraction
from services.compatibility_scoring import calculate_compatibility
from services.mistral_client import MistralLanguageModel
from utils.json_utils import print_json
from utils.mapping_utils import save_to_file
from utils.pdf_to_text import extract_text_from_pdf
from prompt.prompts import prompt_for_cv_extraction, prompt_for_job_description_extraction


def main():
    # Demande des chemins pour le CV en PDF et la description de poste
    pdf_file_path = input("Enter the path to the CV PDF file: ")
    job_post_text_path = input("Enter the path to the job description text file: ")

    # pdf_file_path = ' /Users/samuelhanein/Desktop/ProjetHT/CV Samuel Hanein - Recherche Alternance 2023.pdf'
    # job_post_text_path = '/Users/samuelhanein/Downloads/Job Desc.txt'

    # Lecture du texte de description de poste depuis le fichier
    with open(job_post_text_path, 'r', encoding='utf-8') as file:
        job_post_text = file.read()

    # Chargement de la clé API depuis les variables d'environnement
    api_key = API_KEY
    model_choice = 'mistral-large-latest'
    model_choice_analysis = 'mistral-large-latest'
    mistral_client = MistralLanguageModel(api_key=api_key, model_choice=model_choice)
    mistral_client_analysis = MistralLanguageModel(api_key=api_key, model_choice=model_choice_analysis)

    # Étape 1 : Extraction des informations du CV à partir du PDF
    print(f"\n{Fore.CYAN}--- Step 1: CV Information Extraction ---{Style.RESET_ALL}")
    print("\nExtracting data from the PDF file...")
    extracted_text = extract_text_from_pdf(pdf_file_path)
    ## stockage des données brutes du CV
    save_to_file(extracted_text, "extracted_cv_text.txt", "data/raw_data")
    print("Processing extracted data with AI model using prompt for CV data...")
    prompt_cv = prompt_for_cv_extraction(extracted_text)
    cv_data = mistral_client.generate(prompt_cv, output_format=CVExtraction).dict()
    print("\nExtracted CV Data:")
    # print_json(cv_data)
    save_to_file(cv_data, "cv_data.json", "data/prompts_data")

    # Étape 2 : Extraction des informations de la description de poste
    print(f"\n{Fore.CYAN}--- Step 2: Job Description Information Extraction ---{Style.RESET_ALL}")
    print("\nExtracting data from job post file...")
    ## stockage des données brutes de l'offre
    save_to_file(job_post_text, "job_post_text.txt", "data/raw_data")

    print("Processing job post data with AI model using prompt for job description data...")
    prompt_job = prompt_for_job_description_extraction(job_post_text)
    job_description = mistral_client.generate(prompt_job, output_format=JobDescriptionExtraction).dict()
    print("\nExtracted Job Description Data:")
    # print_json(job_description)
    save_to_file(job_description, "job_data.json", "data/prompts_data")

    # Étape 3 : Calcul de compatibilité en utilisant Mistral via `calculate_compatibility`
    print(f"\n{Fore.CYAN}--- Step 3: Compatibility Scoring ---{Style.RESET_ALL}")
    print("\nCalculating compatibility score...")
    compatibility_score = calculate_compatibility(cv_data, job_description, mistral_client_analysis)

    # Affichage des informations extraites et de la compatibilité
    save_to_file(compatibility_score, "compatibility_score.json", "data/prompts_data")
    print("\nCompatibility:")
    print_json(compatibility_score)

if __name__ == "__main__":
    main()
