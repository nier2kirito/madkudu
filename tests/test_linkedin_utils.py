# tests/test_linkedin_utils.py

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from linkedin_utils import linkedin_auth, scrape_linkedin_profile

class TestLinkedInUtils(unittest.TestCase):
    @patch('linkedin_utils.os.getenv')
    @patch('linkedin_utils.Linkedin')
    def test_linkedin_auth_success(self, mock_linkedin, mock_getenv):
        mock_getenv.side_effect = lambda key: {
            "LINKEDIN_USERNAME": "test_user",
            "LINKEDIN_PASSWORD": "test_pass"
        }.get(key, None)
        
        linkedin_instance = linkedin_auth()
        mock_linkedin.assert_called_with("test_user", "test_pass")
        self.assertEqual(linkedin_instance, mock_linkedin.return_value)
    
    @patch('linkedin_utils.os.getenv')
    def test_linkedin_auth_missing_credentials(self, mock_getenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            linkedin_auth()
    
    @patch('linkedin_utils.linkedin_auth')
    def test_scrape_linkedin_profile_success(self, mock_auth):
        linkedin = MagicMock()
        profile_url = "https://www.linkedin.com/in/test-user/"
        # Ensure get_profile raises an error
        linkedin.get_profile.side_effect = RuntimeError("Profile not found")
    
        profile_data = {
            "firstName": "Test",
            "lastName": "User",
            "headline": "Software Engineer",
            "summary": "Experienced developer.",
            "experience": [{"title": "Developer"}],
            "education": [{"schoolName": "Test University"}],
            "skills": [{"name": "Python"}, {"name": "Java"}]
        }
        linkedin.get_profile.return_value = profile_data
        
        from linkedin_utils import scrape_linkedin_profile
        with self.assertRaises(RuntimeError):
            result = scrape_linkedin_profile(linkedin, profile_url)
        expected = {
            "name": "Test User",
            "headline": "Software Engineer",
            "summary": "Experienced developer.",
            "experience": ["Developer"],
            "education": ["Test University"],
            "skills": ["Python", "Java"]
        }
        self.assertEqual(result, expected)
    
    @patch('linkedin_utils.Linkedin.get_profile')
    def test_scrape_linkedin_profile_failure(self, mock_get_profile):
        mock_get_profile.side_effect = Exception("Profile not found.")
        from linkedin_utils import scrape_linkedin_profile
        with self.assertRaises(RuntimeError):
            scrape_linkedin_profile(MagicMock(), "invalid_url")

if __name__ == '__main__':
    unittest.main()