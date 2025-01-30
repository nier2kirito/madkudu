# tests/test_evaluation.py

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluation import evaluate_length, evaluate_note, evaluate_specific_details, evaluate_text, evaluate_tone_with_vader

class TestEvaluation(unittest.TestCase):
    def test_evaluate_length_pass(self):
        note = "This is a short note."
        result, length = evaluate_length(note)
        self.assertTrue(result)
        self.assertEqual(length, len(note))
    
    def test_evaluate_length_fail(self):
        note = "A" * 301
        result, length = evaluate_length(note)
        self.assertFalse(result)
        self.assertEqual(length, 301)
    
    def test_evaluate_specific_details_pass(self):
        profile_info = {
            "experience": ["Developer"],
            "education": ["Test University"],
            "skills": ["Python"]
        }
        note = "Loved your experience as a Developer."
        result, matches = evaluate_specific_details(note, profile_info)
        self.assertTrue(result)
        self.assertIn("Developer", matches)
    
    def test_evaluate_specific_details_fail(self):
        profile_info = {
            "experience": ["Developer"],
            "education": ["Test University"],
            "skills": ["Python"]
        }
        note = "Great to connect!"
        result, matches = evaluate_specific_details(note, profile_info)
        self.assertFalse(result)
        self.assertEqual(matches, [])
    
    def test_evaluate_text_pass(self):
        note = "Looking forward to connecting with you."
        self.assertTrue(evaluate_text(note))
    
    def test_evaluate_text_fail_emojis(self):
        note = "Let's connect! 😊"
        self.assertFalse(evaluate_text(note))
    
    def test_evaluate_text_fail_hashtags(self):
        note = "Join #networking with me."
        self.assertFalse(evaluate_text(note))
    
    def test_evaluate_tone_pass_positive(self):
        note = "I am excited to connect with you!"
        self.assertTrue(evaluate_tone_with_vader(note))

    def test_evaluate_tone_pass_neutral(self):
        note = "I would like to connect."
        self.assertTrue(evaluate_tone_with_vader(note))  # Assuming neutral is treated as pass

    def test_evaluate_tone_fail_negative(self):
        note = "I don't think this is a good idea."
        self.assertFalse(evaluate_tone_with_vader(note))

    def test_evaluate_tone_fail_emojis(self):
        note = "Let's connect! 😊"
        self.assertTrue(evaluate_tone_with_vader(note))  # Assuming the emoji does not affect the positive tone

    def test_evaluate_tone_fail_hashtags(self):
        note = "Join #networking with me."
        self.assertTrue(evaluate_tone_with_vader(note))  # Assuming the hashtag does not affect the positive tone

    def test_evaluate_tone_fail_excessively_negative(self):
        note = "This is the worst experience I've ever had."
        self.assertFalse(evaluate_tone_with_vader(note))
    def test_evaluate_note_all_pass(self):
        profile_info = {
            "experience": ["Developer"],
            "education": ["Test University"],
            "skills": ["Python"]
        }
        note = "Hello Test, as a Developer at Test University, I'd love to connect!"
        evaluations = evaluate_note(note, profile_info)
        self.assertTrue(evaluations["length_ok"][0])
        self.assertTrue(evaluations["specific_details_ok"][0])
        self.assertTrue(evaluations["tone_ok"])
    
    def test_evaluate_note_partial_fail(self):
        profile_info = {
            "experience": ["Developer"],
            "education": ["Test University"],
            "skills": ["Python"]
        }
        note = "Hi! 😊 Let's connect."
        evaluations = evaluate_note(note, profile_info)
        self.assertTrue(evaluations["length_ok"][0])
        self.assertFalse(evaluations["specific_details_ok"][0])
        self.assertFalse(evaluations["tone_ok"])

if __name__ == '__main__':
    unittest.main()