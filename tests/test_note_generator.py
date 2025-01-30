# tests/test_note_generator.py

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from note_generator import generate_connection_note

class TestNoteGenerator(unittest.TestCase):
    @patch('note_generator.ChatOpenAI')
    def test_generate_connection_note_success(self, mock_chat_openai):
        mock_llm_instance = MagicMock()
        mock_llm_instance.run.return_value = "Hello Test, I'd love to connect!"
        mock_chat_openai.return_value = mock_llm_instance
        
        profile_info = {
            "name": "Test User",
            "headline": "Software Engineer",
            "summary": "Experienced developer.",
            "experience": ["Developer"],
            "education": ["Test University"],
            "skills": ["Python", "Java"]
        }
        openai_api_key = "test_key"
        
        note = generate_connection_note(profile_info, openai_api_key)
        self.assertEqual(note, "Hello Test, I'd love to connect!")
        mock_llm_instance.run.assert_called_with(profile_info)
    
    @patch('note_generator.ChatOpenAI')
    def test_generate_connection_note_failure(self, mock_chat_openai):
        mock_chat_openai.side_effect = Exception("API Error")
        profile_info = {}
        openai_api_key = "test_key"
        with self.assertRaises(RuntimeError):
            generate_connection_note(profile_info, openai_api_key)

if __name__ == '__main__':
    unittest.main()