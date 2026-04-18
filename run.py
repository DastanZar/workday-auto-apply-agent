#!/usr/bin/env python3
"""
Quick start script for Workday Automation Tool
"""

import os
import sys
import json
import shutil

def check_config():
    """Check if configuration file exists"""
    if not os.path.exists('config.json'):
        if os.path.exists('config/config_template.json'):
            print("Creating configuration file from template...")
            shutil.copy('config/config_template.json', 'config.json')
            print("✓ Configuration file created: config.json")
            print("Please edit config.json with your credentials and job URLs")
            return False
        else:
            print("Error: Configuration template not found")
            return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import selenium
        import requests
        print("✓ Dependencies are installed")
        return True
    except ImportError as e:
        print(f"Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main entry point"""
    print("Workday Automation Tool - Quick Start")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check configuration
    if not check_config():
        return
    
    # Import and run automation
    try:
        from workday_automation import WorkdayAutomation
        
        print("Starting Workday automation...")
        automation = WorkdayAutomation('config.json')
        
        # Load job URLs
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        job_urls = config.get('job_urls', [])
        if not job_urls:
            print("No job URLs found in configuration")
            return
        
        print(f"Found {len(job_urls)} jobs to process")
        
        # Process jobs
        results = automation.process_job_list(job_urls)
        
        # Show results
        successful = sum(1 for r in results if r.get('success', False))
        print(f"\nResults: {successful}/{len(results)} applications successful")
        
        automation.close()
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
