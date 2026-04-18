#!/usr/bin/env python3
"""
Unit tests for Workday Automation Tool
"""

import unittest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Mock selenium imports
sys.modules['selenium'] = Mock()
sys.modules['selenium.webdriver'] = Mock()
sys.modules['selenium.webdriver.chrome'] = Mock()
sys.modules['selenium.webdriver.common.by'] = Mock()
sys.modules['selenium.webdriver.support.ui'] = Mock()
sys.modules['selenium.webdriver.support.expected_conditions'] = Mock()

class TestWorkdayAutomation(unittest.TestCase):
    """Test cases for WorkdayAutomation class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            "credentials": {
                "email": "test@example.com",
                "password": "testpassword"
            },
            "resume_path": "test_resume.pdf",
            "job_urls": ["https://test.workday.com/job/123"],
            "form_fields": {
                "first_name": "Test",
                "last_name": "User"
            }
        }
    
    def test_load_config(self):
        """Test configuration loading"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_config, f)
            config_file = f.name
        
        try:
            from workday_automation import WorkdayAutomation
            # Mock the WebDriver initialization
            with patch('workday_automation.webdriver.Chrome'):
                automation = WorkdayAutomation(config_file)
                self.assertEqual(automation.config, self.test_config)
        finally:
            os.unlink(config_file)
    
    def test_config_validation(self):
        """Test configuration validation"""
        required_fields = ['credentials', 'job_urls']
        
        for field in required_fields:
            invalid_config = self.test_config.copy()
            del invalid_config[field]
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(invalid_config, f)
                config_file = f.name
            
            try:
                with patch('workday_automation.webdriver.Chrome'):
                    from workday_automation import WorkdayAutomation
                    # Should handle missing fields gracefully
                    automation = WorkdayAutomation(config_file)
                    self.assertIsNotNone(automation.config)
            finally:
                os.unlink(config_file)
    
    def test_job_url_validation(self):
        """Test job URL validation"""
        test_urls = [
            "https://company.workday.com/job/123",
            "https://myworkday.com/careers/456",
            "invalid-url",
            ""
        ]
        
        valid_urls = [url for url in test_urls if url.startswith('http') and 'workday' in url]
        self.assertEqual(len(valid_urls), 2)
    
    def test_form_field_mapping(self):
        """Test form field mapping functionality"""
        form_fields = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }
        
        # Test field name normalization
        normalized_fields = {}
        for key, value in form_fields.items():
            normalized_key = key.replace('_', ' ').title()
            normalized_fields[normalized_key] = value
        
        self.assertIn("First Name", normalized_fields)
        self.assertIn("Last Name", normalized_fields)
    
    def test_error_handling(self):
        """Test error handling mechanisms"""
        # Test with invalid configuration file
        with self.assertRaises(SystemExit):
            from workday_automation import WorkdayAutomation
            WorkdayAutomation('nonexistent.json')
    
    def test_logging_setup(self):
        """Test logging configuration"""
        import logging
        
        # Test that logging is properly configured
        logger = logging.getLogger('workday_automation')
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.INFO)

class TestChromeExtension(unittest.TestCase):
    """Test cases for Chrome extension functionality"""
    
    def test_manifest_validation(self):
        """Test Chrome extension manifest"""
        manifest_path = 'chrome-extension/manifest.json'
        
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Check required manifest fields
            required_fields = ['manifest_version', 'name', 'version', 'permissions']
            for field in required_fields:
                self.assertIn(field, manifest)
    
    def test_content_script_structure(self):
        """Test content script structure"""
        content_script_path = 'chrome-extension/content.js'
        
        if os.path.exists(content_script_path):
            with open(content_script_path, 'r') as f:
                content = f.read()
            
            # Check for essential functions
            essential_functions = ['autoFillCredentials', 'isWorkdayLoginPage']
            for func in essential_functions:
                self.assertIn(func, content)

class TestConfiguration(unittest.TestCase):
    """Test configuration management"""
    
    def test_config_template_exists(self):
        """Test that configuration template exists"""
        template_path = 'config/config_template.json'
        self.assertTrue(os.path.exists(template_path))
        
        with open(template_path, 'r') as f:
            template = json.load(f)
        
        # Check template structure
        required_sections = ['credentials', 'form_fields', 'settings']
        for section in required_sections:
            self.assertIn(section, template)
    
    def test_requirements_file(self):
        """Test requirements.txt file"""
        requirements_path = 'requirements.txt'
        self.assertTrue(os.path.exists(requirements_path))
        
        with open(requirements_path, 'r') as f:
            requirements = f.read()
        
        # Check for essential packages
        essential_packages = ['selenium', 'requests']
        for package in essential_packages:
            self.assertIn(package, requirements)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestWorkdayAutomation))
    suite.addTest(unittest.makeSuite(TestChromeExtension))
    suite.addTest(unittest.makeSuite(TestConfiguration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
