#!/usr/bin/env python3
"""
Basic usage example for Workday Automation Tool
"""

import json
import os
from workday_automation import WorkdayAutomation

def create_sample_config():
    """Create a sample configuration file"""
    config = {
        "credentials": {
            "email": "your.email@company.com",
            "password": "your_password_here"
        },
        "resume_path": "resume.pdf",
        "job_urls": [
            "https://company.workday.com/careers/job/12345",
            "https://company.workday.com/careers/job/67890"
        ],
        "form_fields": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "country": "United States",
            "work_authorization": "Yes",
            "sponsorship_required": "No",
            "disability_status": "I don't wish to answer",
            "veteran_status": "I am not a veteran",
            "gender": "Male",
            "ethnicity": "White",
            "how_did_you_hear": "LinkedIn"
        },
        "settings": {
            "wait_time_between_applications": 30,
            "max_retries": 3,
            "headless_mode": False,
            "auto_submit": True
        }
    }
    
    with open('sample_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Sample configuration created: sample_config.json")
    return config

def single_job_example():
    """Example of applying to a single job"""
    print("=== Single Job Application Example ===")
    
    # Create sample config
    config = create_sample_config()
    
    # Initialize automation
    automation = WorkdayAutomation('sample_config.json')
    
    try:
        # Apply to first job in the list
        job_url = config['job_urls'][0]
        print(f"Applying to job: {job_url}")
        
        success = automation.apply_to_job(job_url)
        
        if success:
            print("Application completed successfully!")
        else:
            print("Application failed. Check logs for details.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()

def multiple_jobs_example():
    """Example of applying to multiple jobs"""
    print("=== Multiple Jobs Application Example ===")
    
    # Create sample config
    config = create_sample_config()
    
    # Initialize automation
    automation = WorkdayAutomation('sample_config.json')
    
    try:
        # Process all jobs
        results = automation.process_job_list(config['job_urls'])
        
        # Analyze results
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\nResults Summary:")
        print(f"Total jobs: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        
        # Print detailed results
        for i, result in enumerate(results, 1):
            status = "SUCCESS" if result['success'] else "FAILED"
            print(f"Job {i}: {status} - {result['url']}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()

def custom_configuration_example():
    """Example with custom configuration"""
    print("=== Custom Configuration Example ===")
    
    # Custom configuration
    custom_config = {
        "credentials": {
            "email": "custom@example.com",
            "password": "custom_password"
        },
        "resume_path": "custom_resume.pdf",
        "job_urls": [
            "https://tech-company.workday.com/careers/job/software-engineer"
        ],
        "form_fields": {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+1987654321",
            "address": "456 Tech Ave",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94105",
            "country": "United States",
            "work_authorization": "Yes",
            "sponsorship_required": "No",
            "disability_status": "I don't wish to answer",
            "veteran_status": "I am not a veteran",
            "gender": "Female",
            "ethnicity": "Asian",
            "how_did_you_hear": "Company Website"
        },
        "settings": {
            "wait_time_between_applications": 60,
            "max_retries": 5,
            "headless_mode": True,
            "auto_submit": False
        }
    }
    
    # Save custom configuration
    with open('custom_config.json', 'w') as f:
        json.dump(custom_config, f, indent=2)
    
    print("Custom configuration created: custom_config.json")
    
    # Initialize with custom config
    automation = WorkdayAutomation('custom_config.json')
    
    try:
        # Process jobs with custom settings
        results = automation.process_job_list(custom_config['job_urls'])
        
        print(f"Processed {len(results)} jobs with custom configuration")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()

def error_handling_example():
    """Example of proper error handling"""
    print("=== Error Handling Example ===")
    
    # Create sample config
    config = create_sample_config()
    
    automation = None
    try:
        # Initialize automation
        automation = WorkdayAutomation('sample_config.json')
        
        # Process jobs with error handling
        for job_url in config['job_urls']:
            try:
                print(f"Processing: {job_url}")
                success = automation.apply_to_job(job_url)
                
                if success:
                    print(f"✓ Successfully applied to {job_url}")
                else:
                    print(f"✗ Failed to apply to {job_url}")
                    
            except Exception as job_error:
                print(f"✗ Error applying to {job_url}: {job_error}")
                # Continue with next job
                continue
                
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if automation:
            automation.close()
            print("Automation closed")

def main():
    """Run all examples"""
    print("Workday Automation Tool - Usage Examples")
    print("=" * 50)
    
    # Check if required files exist
    if not os.path.exists('workday_automation.py'):
        print("Error: workday_automation.py not found")
        print("Please run this script from the project root directory")
        return
    
    # Run examples
    try:
        single_job_example()
        print("\n" + "=" * 50)
        
        multiple_jobs_example()
        print("\n" + "=" * 50)
        
        custom_configuration_example()
        print("\n" + "=" * 50)
        
        error_handling_example()
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"Error running examples: {e}")
    
    # Cleanup
    for file in ['sample_config.json', 'custom_config.json']:
        if os.path.exists(file):
            os.remove(file)
            print(f"Cleaned up: {file}")

if __name__ == "__main__":
    main()
