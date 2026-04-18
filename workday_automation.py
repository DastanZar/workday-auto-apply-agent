#!/usr/bin/env python3
"""
Workday Job Application Automation Tool

This script automates the process of applying to jobs on Workday platforms.
It handles form filling, resume uploads, and multi-page applications.
"""

import time
import os
import sys
import json
import logging
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workday_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkdayAutomation:
    """Main class for Workday job application automation"""
    
    def __init__(self, config_file='config.json'):
        """Initialize the automation with configuration"""
        self.config = self.load_config(config_file)
        self.driver = None
        self.wait = None
        self.setup_driver()
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {config_file} not found")
            sys.exit(1)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {config_file}")
            sys.exit(1)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            sys.exit(1)
    
    def navigate_to_job(self, job_url):
        """Navigate to a specific job URL"""
        try:
            logger.info(f"Navigating to job: {job_url}")
            self.driver.get(job_url)
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {job_url}: {e}")
            return False
    
    def check_job_availability(self):
        """Check if the job is still available"""
        try:
            # Check for common "job closed" indicators
            closed_indicators = [
                "no longer accepting applications",
                "position has been filled",
                "job posting has closed",
                "position is no longer available"
            ]
            
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            for indicator in closed_indicators:
                if indicator in page_text:
                    logger.warning(f"Job appears to be closed: {indicator}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error checking job availability: {e}")
            return True  # Assume available if we can't check
    
    def click_apply_button(self):
        """Click the apply button on the job page"""
        try:
            apply_selectors = [
                "a[role='button'][data-uxi-element-id='Apply_adventureButton']",
                "button[data-automation-id='apply']",
                "a[href*='apply']",
                "button:contains('Apply')",
                "a:contains('Apply')"
            ]
            
            for selector in apply_selectors:
                try:
                    apply_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if apply_button.is_displayed() and apply_button.is_enabled():
                        apply_button.click()
                        logger.info("Apply button clicked successfully")
                        time.sleep(3)
                        return True
                except NoSuchElementException:
                    continue
            
            logger.warning("Apply button not found")
            return False
        except Exception as e:
            logger.error(f"Error clicking apply button: {e}")
            return False
    
    def handle_authentication(self):
        """Handle login/signup process"""
        try:
            # Check if already logged in
            if self.is_logged_in():
                logger.info("Already logged in")
                return True
            
            # Try to find login form
            if self.find_login_form():
                self.fill_login_form()
            else:
                logger.info("No login form found, proceeding with application")
            
            return True
        except Exception as e:
            logger.error(f"Error handling authentication: {e}")
            return False
    
    def is_logged_in(self):
        """Check if user is already logged in"""
        try:
            # Look for indicators that user is logged in
            logged_in_indicators = [
                "logout",
                "sign out",
                "profile",
                "dashboard"
            ]
            
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            return any(indicator in page_text for indicator in logged_in_indicators)
        except:
            return False
    
    def find_login_form(self):
        """Find and identify login form"""
        try:
            # Look for email/password fields
            email_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[id*='email']")
            password_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
            
            return len(email_fields) > 0 and len(password_fields) > 0
        except:
            return False
    
    def fill_login_form(self):
        """Fill in login credentials"""
        try:
            # Find email field
            email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[id*='email']")
            email_field.clear()
            email_field.send_keys(self.config['credentials']['email'])
            
            # Find password field
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.clear()
            password_field.send_keys(self.config['credentials']['password'])
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            submit_button.click()
            
            logger.info("Login form submitted")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"Error filling login form: {e}")
            return False
    
    def upload_resume(self):
        """Upload resume file"""
        try:
            resume_path = self.config['resume_path']
            if not os.path.exists(resume_path):
                logger.error(f"Resume file not found: {resume_path}")
                return False
            
            # Find file upload input
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(os.path.abspath(resume_path))
            
            logger.info("Resume uploaded successfully")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Error uploading resume: {e}")
            return False
    
    def fill_application_form(self):
        """Fill out the job application form"""
        try:
            # Get form fields configuration
            form_fields = self.config.get('form_fields', {})
            
            # Fill each field
            for field_name, field_value in form_fields.items():
                if self.fill_form_field(field_name, field_value):
                    logger.info(f"Filled field: {field_name}")
                else:
                    logger.warning(f"Failed to fill field: {field_name}")
            
            return True
        except Exception as e:
            logger.error(f"Error filling application form: {e}")
            return False
    
    def fill_form_field(self, field_name, field_value):
        """Fill a specific form field"""
        try:
            # Common selectors for different field types
            selectors = [
                f"input[name='{field_name}']",
                f"input[id='{field_name}']",
                f"input[data-automation-id='{field_name}']",
                f"select[name='{field_name}']",
                f"textarea[name='{field_name}']"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        if element.tag_name == 'select':
                            self.handle_dropdown(element, field_value)
                        else:
                            element.clear()
                            element.send_keys(str(field_value))
                        return True
                except NoSuchElementException:
                    continue
            
            return False
        except Exception as e:
            logger.error(f"Error filling field {field_name}: {e}")
            return False
    
    def handle_dropdown(self, element, value):
        """Handle dropdown/select elements"""
        try:
            from selenium.webdriver.support.ui import Select
            select = Select(element)
            select.select_by_visible_text(str(value))
            return True
        except:
            # Fallback: try clicking and selecting
            element.click()
            time.sleep(1)
            option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{value}')]")
            option.click()
            return True
    
    def submit_application(self):
        """Submit the job application"""
        try:
            # Look for submit button
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Submit')",
                "button:contains('Apply')",
                "button[data-automation-id='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        submit_button.click()
                        logger.info("Application submitted successfully")
                        time.sleep(3)
                        return True
                except NoSuchElementException:
                    continue
            
            logger.warning("Submit button not found")
            return False
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return False
    
    def apply_to_job(self, job_url):
        """Complete the entire job application process"""
        try:
            logger.info(f"Starting application process for: {job_url}")
            
            # Navigate to job
            if not self.navigate_to_job(job_url):
                return False
            
            # Check if job is available
            if not self.check_job_availability():
                logger.warning("Job is no longer available")
                return False
            
            # Click apply button
            if not self.click_apply_button():
                logger.error("Failed to click apply button")
                return False
            
            # Handle authentication
            if not self.handle_authentication():
                logger.error("Authentication failed")
                return False
            
            # Upload resume
            if not self.upload_resume():
                logger.warning("Resume upload failed")
            
            # Fill application form
            if not self.fill_application_form():
                logger.warning("Form filling failed")
            
            # Submit application
            if not self.submit_application():
                logger.error("Application submission failed")
                return False
            
            logger.info("Job application completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error in job application process: {e}")
            return False
    
    def process_job_list(self, job_urls):
        """Process a list of job URLs"""
        results = []
        
        for i, job_url in enumerate(job_urls, 1):
            logger.info(f"Processing job {i}/{len(job_urls)}: {job_url}")
            
            try:
                success = self.apply_to_job(job_url)
                results.append({
                    'url': job_url,
                    'success': success,
                    'timestamp': datetime.now().isoformat()
                })
                
                if success:
                    logger.info(f"Successfully applied to job {i}")
                else:
                    logger.warning(f"Failed to apply to job {i}")
                
                # Wait between applications
                if i < len(job_urls):
                    logger.info("Waiting 30 seconds before next application...")
                    time.sleep(30)
                    
            except Exception as e:
                logger.error(f"Error processing job {i}: {e}")
                results.append({
                    'url': job_url,
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return results
    
    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the automation"""
    try:
        # Initialize automation
        automation = WorkdayAutomation()
        
        # Load job URLs
        job_urls = automation.config.get('job_urls', [])
        if not job_urls:
            logger.error("No job URLs found in configuration")
            return
        
        logger.info(f"Found {len(job_urls)} jobs to process")
        
        # Process all jobs
        results = automation.process_job_list(job_urls)
        
        # Save results
        with open('application_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        # Print summary
        successful = sum(1 for r in results if r['success'])
        logger.info(f"Application process completed: {successful}/{len(results)} successful")
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if 'automation' in locals():
            automation.close()

if __name__ == "__main__":
    main()
