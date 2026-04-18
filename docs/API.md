# Workday Automation API Documentation

## Overview

The Workday Automation Tool provides a comprehensive API for automating job applications on Workday platforms. This document outlines the available classes, methods, and configuration options.

## Core Classes

### WorkdayAutomation

The main automation class that handles the complete job application process.

#### Constructor
```python
WorkdayAutomation(config_file='config.json')
```

**Parameters:**
- `config_file` (str): Path to the configuration JSON file

#### Methods

##### `load_config(config_file)`
Loads configuration from a JSON file.

**Parameters:**
- `config_file` (str): Path to configuration file

**Returns:** dict - Configuration dictionary

**Raises:**
- `FileNotFoundError`: If configuration file doesn't exist
- `json.JSONDecodeError`: If configuration file contains invalid JSON

##### `navigate_to_job(job_url)`
Navigates to a specific job URL.

**Parameters:**
- `job_url` (str): URL of the job posting

**Returns:** bool - True if navigation successful, False otherwise

##### `check_job_availability()`
Checks if the job is still available for applications.

**Returns:** bool - True if job is available, False if closed

##### `click_apply_button()`
Clicks the apply button on the job page.

**Returns:** bool - True if button clicked successfully

##### `handle_authentication()`
Handles the login/signup process.

**Returns:** bool - True if authentication successful

##### `upload_resume()`
Uploads the resume file to the application form.

**Returns:** bool - True if upload successful

##### `fill_application_form()`
Fills out the job application form with configured data.

**Returns:** bool - True if form filled successfully

##### `submit_application()`
Submits the completed job application.

**Returns:** bool - True if submission successful

##### `apply_to_job(job_url)`
Completes the entire job application process for a single job.

**Parameters:**
- `job_url` (str): URL of the job to apply to

**Returns:** bool - True if application completed successfully

##### `process_job_list(job_urls)`
Processes a list of job URLs.

**Parameters:**
- `job_urls` (list): List of job URLs to process

**Returns:** list - List of result dictionaries with application status

##### `close()`
Closes the browser and cleans up resources.

## Configuration Schema

### Main Configuration
```json
{
  "credentials": {
    "email": "string",
    "password": "string"
  },
  "resume_path": "string",
  "job_urls": ["string"],
  "form_fields": {
    "field_name": "value"
  },
  "settings": {
    "wait_time_between_applications": "number",
    "max_retries": "number",
    "headless_mode": "boolean",
    "auto_submit": "boolean"
  }
}
```

### Form Fields Configuration

The `form_fields` section supports the following standard fields:

| Field Name | Type | Description |
|------------|------|-------------|
| `first_name` | string | Applicant's first name |
| `last_name` | string | Applicant's last name |
| `phone` | string | Phone number |
| `address` | string | Street address |
| `city` | string | City |
| `state` | string | State/Province |
| `zip_code` | string | Postal/ZIP code |
| `country` | string | Country |
| `work_authorization` | string | Work authorization status |
| `sponsorship_required` | string | Visa sponsorship requirement |
| `disability_status` | string | Disability status declaration |
| `veteran_status` | string | Veteran status |
| `gender` | string | Gender identity |
| `ethnicity` | string | Ethnic background |
| `how_did_you_hear` | string | How applicant heard about the job |

### Settings Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `wait_time_between_applications` | number | 30 | Seconds to wait between applications |
| `max_retries` | number | 3 | Maximum retry attempts for failed applications |
| `headless_mode` | boolean | false | Run browser in headless mode |
| `auto_submit` | boolean | true | Automatically submit applications |

## Chrome Extension API

### Content Script Functions

#### `autoFillCredentials()`
Automatically fills login credentials on Workday pages.

**Returns:** Promise<boolean> - True if credentials filled successfully

#### `isWorkdayLoginPage()`
Checks if the current page is a Workday login page.

**Returns:** boolean - True if page is a Workday login page

### Popup Functions

#### `saveCredentials(email, password)`
Saves login credentials to Chrome storage.

**Parameters:**
- `email` (string): User's email address
- `password` (string): User's password

#### `autoFill()`
Triggers auto-fill functionality on the current page.

**Returns:** boolean - True if auto-fill successful

## Error Handling

### Common Exceptions

#### `TimeoutException`
Raised when WebDriver operations timeout.

**Handling:**
```python
try:
    automation.apply_to_job(job_url)
except TimeoutException:
    logger.error("Operation timed out")
```

#### `NoSuchElementException`
Raised when required page elements are not found.

**Handling:**
```python
try:
    automation.click_apply_button()
except NoSuchElementException:
    logger.warning("Apply button not found")
```

#### `WebDriverException`
Raised for general WebDriver errors.

**Handling:**
```python
try:
    automation.setup_driver()
except WebDriverException as e:
    logger.error(f"WebDriver error: {e}")
```

### Error Recovery

The automation tool includes several error recovery mechanisms:

1. **Automatic Retry**: Failed operations are retried up to `max_retries` times
2. **Graceful Degradation**: Non-critical failures don't stop the entire process
3. **Manual Intervention**: User is prompted for manual completion when needed
4. **Logging**: All errors are logged with detailed information

## Logging

### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General process information
- **WARNING**: Non-critical issues
- **ERROR**: Application failures

### Log Files

- `workday_automation.log`: Main application log
- `application_results.json`: Application results summary

### Log Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workday_automation.log'),
        logging.StreamHandler()
    ]
)
```

## Usage Examples

### Basic Usage
```python
from workday_automation import WorkdayAutomation

# Initialize automation
automation = WorkdayAutomation('config.json')

# Apply to a single job
success = automation.apply_to_job('https://company.workday.com/job/123')

# Process multiple jobs
results = automation.process_job_list([
    'https://company.workday.com/job/123',
    'https://company.workday.com/job/456'
])

# Clean up
automation.close()
```

### Advanced Configuration
```python
# Custom configuration
config = {
    "credentials": {
        "email": "user@example.com",
        "password": "password123"
    },
    "resume_path": "/path/to/resume.pdf",
    "job_urls": ["https://company.workday.com/job/123"],
    "form_fields": {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890"
    },
    "settings": {
        "wait_time_between_applications": 60,
        "max_retries": 5,
        "headless_mode": True,
        "auto_submit": False
    }
}

# Save configuration
import json
with open('custom_config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

### Error Handling Example
```python
try:
    automation = WorkdayAutomation('config.json')
    results = automation.process_job_list(job_urls)
    
    # Process results
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"Successful applications: {len(successful)}")
    print(f"Failed applications: {len(failed)}")
    
except Exception as e:
    logger.error(f"Fatal error: {e}")
finally:
    if 'automation' in locals():
        automation.close()
```

## Best Practices

1. **Configuration Management**: Use environment variables for sensitive data
2. **Error Handling**: Always wrap automation calls in try-catch blocks
3. **Resource Cleanup**: Always call `close()` method when done
4. **Logging**: Enable appropriate log levels for debugging
5. **Testing**: Test with a small set of jobs before running large batches
6. **Rate Limiting**: Use appropriate delays between applications
7. **Monitoring**: Monitor logs for errors and performance issues
