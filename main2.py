import os
import json
from linkedin_api import Linkedin
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize LinkedIn API
def linkedin_auth():
    # Get credentials from environment variables
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not username or not password:
        raise ValueError("Please set LINKEDIN_USERNAME and LINKEDIN_PASSWORD environment variables")
    
    # Authenticate using username and password
    return Linkedin(username, password)

def scrape_linkedin_profile(linkedin, profile_url):
    """Scrape LinkedIn profile data"""
    try:
        profile_id = profile_url.split("/in/")[-1].strip("/")
        profile = linkedin.get_profile(public_id=profile_id)
        
        # Extract relevant information
        return {
            "name": profile.get("firstName", "") + " " + profile.get("lastName", ""),
            "headline": profile.get("headline", ""),
            "summary": profile.get("summary", ""),
            "experience": [exp.get("title", "") for exp in profile.get("experience", [])],
            "education": [edu.get("schoolName", "") for edu in profile.get("education", [])],
            "skills": [skill.get("name", "") for skill in profile.get("skills", [])]
        }
    except Exception as e:
        raise RuntimeError(f"Failed to scrape profile: {str(e)}")

def generate_connection_note(profile_info, openai_api_key):
    """Generate personalized connection note using LangChain"""
    template = """You are a professional networking assistant. Write a personalized LinkedIn connection request message to explore opportunities of an internship for:
    
    Name: {name}
    Headline: {headline}
    Summary: {summary}
    Experience: {experience}
    Education: {education}
    Skills: {skills}

    Requirements:
    - Keep it under 300 characters
    - Mention 1-2 specific details from their profile
    - Focus on common ground or mutual value
    - Professional but friendly tone
    - No emojis or hashtags"""

    prompt = PromptTemplate(
        input_variables=["name", "headline", "summary", "experience", "education", "skills"],
        template=template
    )

    llm = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-4o",
        openai_api_key=openai_api_key
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(profile_info)

def process_profiles(profiles_file, output_file, linkedin, openai_api_key):
    """Process LinkedIn profiles from a JSON file and generate connection notes"""
    try:
        with open(profiles_file, "r") as infile:
            profiles = json.load(infile)
        
        results = []

        for profile_url in profiles:
            try:
                profile_info = scrape_linkedin_profile(linkedin, profile_url)
                connection_note = generate_connection_note(profile_info, openai_api_key)
                results.append({
                    "profile_url": profile_url,
                    "name": profile_info.get("name", ""),
                    "connection_note": connection_note
                })
            except Exception as e:
                print(f"Error processing profile {profile_url}: {e}")

        with open(output_file, "w") as outfile:
            json.dump(results, outfile, indent=4)

        print(f"Processed {len(results)} profiles. Results saved to {output_file}")
    except Exception as e:
        raise RuntimeError(f"Failed to process profiles: {str(e)}")

if __name__ == "__main__":
    # Authenticate LinkedIn
    linkedin = linkedin_auth()

    # Get OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Input and output file paths
    profiles_file = "linkedin_profiles.json"  # JSON file containing LinkedIn profile URLs
    output_file = "connection_notes.json"  # JSON file to save the connection notes

    # Process profiles
    process_profiles(profiles_file, output_file, linkedin, openai_api_key)
