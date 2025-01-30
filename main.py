# main.py

import os
import logging
from linkedin_utils import linkedin_auth, scrape_linkedin_profile
from note_generator import generate_connection_note
from evaluation import evaluate_note

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Authenticate to LinkedIn
        linkedin = linkedin_auth()
        
        # Get OpenAI API Key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("OPENAI_API_KEY must be set in the environment.")
            raise ValueError("Please set the OPENAI_API_KEY environment variable.")
        
        # Input LinkedIn Profile URL
        profile_url = input("Enter LinkedIn profile URL: ").strip()
        if not profile_url:
            logger.error("No LinkedIn profile URL provided.")
            raise ValueError("LinkedIn profile URL cannot be empty.")
        
        # Scrape LinkedIn Profile
        profile_info = scrape_linkedin_profile(linkedin, profile_url)
        logger.debug(f"Profile Info: {profile_info}")
        
        # Generate Connection Note
        connection_note = generate_connection_note(profile_info, openai_api_key)
        print("\nGenerated Connection Note:")
        print(connection_note)
        
        # Evaluate Connection Note
        evaluation_results = evaluate_note(connection_note, profile_info)
        print("\nEvaluation Results:")
        for metric, result in evaluation_results.items():
            print(f"{metric}: {'Pass' if result[0] else 'Fail'} (Details: {result[1]})")
    
    except Exception as e:
        logger.exception("An error occurred during execution.")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()