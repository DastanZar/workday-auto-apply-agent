#!/usr/bin/env python3
"""
Installation script for Workday Automation Tool
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"Python version: {sys.version}")

def install_dependencies():
    """Install required Python packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_chrome_driver():
    """Setup ChromeDriver for Selenium"""
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        
        # Download and setup ChromeDriver
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver installed at: {driver_path}")
        
        # Test ChromeDriver
        service = Service(driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.quit()
        print("ChromeDriver test successful")
        
    except Exception as e:
        print(f"Error setting up ChromeDriver: {e}")
        sys.exit(1)

def create_config_file():
    """Create default configuration file if it doesn't exist"""
    if not os.path.exists('config.json'):
        import shutil
        shutil.copy('config/config_template.json', 'config.json')
        print("Default configuration file created")
    else:
        print("Configuration file already exists")

def main():
    """Main installation process"""
    print("Installing Workday Automation Tool...")
    
    check_python_version()
    install_dependencies()
    setup_chrome_driver()
    create_config_file()
    
    print("Installation completed successfully!")
    print("Next steps:")
    print("1. Edit config.json with your credentials")
    print("2. Add job URLs to the configuration")
    print("3. Run: python workday_automation.py")

if __name__ == "__main__":
    main()
