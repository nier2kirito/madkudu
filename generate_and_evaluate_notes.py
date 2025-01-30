import json 
from note_generator import generate_connection_note
from linkedin_utils import linkedin_auth, scrape_linkedin_profile
from evaluation import evaluate_note
import logging 
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_evaluation(config_file, results_file):

    # Get OpenAI API Key
    openai_api_key = os.getenv("OPENAI_API_KEY")

    with open(config_file, 'r') as file:
        config = json.load(file)
    
    linkedin = linkedin_auth()
    results = []

    total_profiles = len(config['profile_urls'])
    successful_matches = {'length_ok': 0, 'specific_details_ok': 0, 'tone': 0, 'professional text': 0}

    for profile_url in config['profile_urls']:
        profile_info = scrape_linkedin_profile(linkedin, profile_url)
        note = generate_connection_note(profile_info, openai_api_key)
        result= evaluate_note(note, profile_info)
        
        if result['length_ok'][0]:
            successful_matches['length_ok'] += 1
        if result['specific_details_ok'][0]:
            successful_matches['specific_details_ok'] += 1
        if result['tone'][0]:
            successful_matches['tone'] += 1
        if result['professional text'][0]:
            successful_matches['professional text'] += 1

        results.append({
            "profile_url": profile_url,
            "profile_info": profile_info,
            "generated_note": note,
            "evaluation": {
                "success": result,
            }
        })
    
    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)

    # Print summary of results
    logger.info(f"Processed {total_profiles} profiles")
    logger.info(f"Successful Evaluations: length_ok: {successful_matches['length_ok']}, specific_details_ok: {successful_matches['specific_details_ok']}, tone: {successful_matches['tone']}, professional text: {successful_matches['professional text']}")
    logger.info(f"Failed Evaluations: length_ok: {total_profiles - successful_matches['length_ok']}, specific_details_ok: {total_profiles - successful_matches['specific_details_ok']}, tone: {total_profiles - successful_matches['tone']}, professional text: {total_profiles - successful_matches['professional text']}")

# Execute the evaluation
run_evaluation('linkedin_profiles.json', 'connection_notes.json')