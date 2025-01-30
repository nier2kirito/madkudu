# linkedin_utils.py

import os
from linkedin_api import Linkedin
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def linkedin_auth():
    """Authenticate to LinkedIn using credentials from environment variables."""
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not username or not password:
        logger.error("LINKEDIN_USERNAME and LINKEDIN_PASSWORD must be set in the environment.")
        raise ValueError("Please set LINKEDIN_USERNAME and LINKEDIN_PASSWORD environment variables")
    
    try:
        linkedin = Linkedin(username, password)
        logger.info("Successfully authenticated to LinkedIn.")
        return linkedin
    except Exception as e:
        logger.exception("LinkedIn authentication failed.")
        raise RuntimeError(f"LinkedIn authentication failed: {str(e)}")

def scrape_linkedin_profile(linkedin, profile_url):
    """Scrape LinkedIn profile data."""
    try:
        profile_id = profile_url.split("/in/")[-1].strip("/")
        profile = linkedin.get_profile(public_id=profile_id)
        logger.info(f"Successfully scraped profile: {profile_id}")
        
        return {
            "name": f"{profile.get('firstName', '').strip()} {profile.get('lastName', '').strip()}",
            "headline": profile.get("headline", "").strip(),
            "summary": profile.get("summary", '').strip(),
            "experience": [exp.get("title", "").strip() for exp in profile.get("experience", [])],
            "education": [edu.get("schoolName", "").strip() for edu in profile.get("education", [])],
            "skills": [skill.get("name", "").strip() for skill in profile.get("skills", [])]
        }
    except Exception as e:
        logger.exception("Failed to scrape LinkedIn profile.")
        raise RuntimeError(f"Failed to scrape profile: {str(e)}")