# evaluation.py

import re
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_length(note, max_length=300):
    """Check if the note is under the specified maximum length."""
    length = len(note)
    return (length <= max_length, length)

def evaluate_specific_details(note, profile_info):
    """Check if 1-2 specific details from the profile are mentioned in the note."""
    details = []
    if profile_info.get("experience"):
        details.extend(profile_info["experience"][0].split())
    if profile_info.get("education"):
        details.extend(profile_info["education"][0].split())
    if profile_info.get("skills"):
        details.extend(profile_info["skills"][0].split())

    matches = [detail for detail in details if re.search(rf'\b{re.escape(detail)}\b', note, re.IGNORECASE)]
    return (1 <= len(matches) <= 2, matches)

def evaluate_tone_with_vader(note):
    """Evaluate the tone of a note using VADER sentiment analysis."""
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(note)
    
    # Determine tone based on compound score
    compound_score = sentiment['compound']
    if compound_score >= 0.05:
        tone = 'positive'
    elif compound_score <= -0.05:
        tone = 'negative'
    else:
        tone = 'neutral'
    
    return (tone != "negative", tone)

def evaluate_text(note):
    """Evaluate text for the presence of emojis and hashtags."""
    # Use the emoji library to find all emojis in the text
    emojis = [char for char in note if char in emoji.EMOJI_DATA]
    
    # Check for the presence of hashtags
    hashtags = '#' in note
    
    # Return a tuple indicating if the text is free of emojis and hashtags, and the list of found emojis
    return (len(emojis) == 0 and not hashtags, emojis)

def evaluate_note(note, profile_info):
    """Evaluate the generated connection note based on defined metrics."""
    evaluations = {
        "length_ok": evaluate_length(note),
        "specific_details_ok": evaluate_specific_details(note, profile_info),
        "tone" : evaluate_tone_with_vader(note),
        "professional text": evaluate_text(note)
    }
    return evaluations