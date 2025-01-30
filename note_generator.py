# note_generator.py

import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_connection_note(profile_info, openai_api_key):
    """Generate a personalized LinkedIn connection note."""
    template = """You are a professional networking assistant. Write a personalized LinkedIn connection request message for:
    
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

    try:
        llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4",
            openai_api_key=openai_api_key
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        connection_note = chain.run(profile_info)
        logger.info("Successfully generated connection note.")
        return connection_note.strip()
    except Exception as e:
        logger.exception("Failed to generate connection note.")
        raise RuntimeError(f"Failed to generate connection note: {str(e)}")