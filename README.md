# Workday Automation Tool

A comprehensive automation solution for Workday job applications, featuring both a Chrome extension for quick login auto-fill and a Python script for complete application automation.

## Features

### Chrome Extension
- Automatic login credential filling on Workday sites
- Secure credential storage using Chrome's sync storage
- One-click auto-fill functionality
- Support for multiple Workday domains
- Clean, user-friendly interface

### Python Automation Script
- Complete job application automation
- Resume upload automation
- Multi-page form handling
- Intelligent form field detection and filling
- Application status tracking
- Comprehensive logging system
- Error handling and recovery
- Batch job processing

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (automatically managed by the script)

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Chrome Extension Installation
1. Download or clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the `chrome-extension` folder
5. The extension will be installed and ready to use

## Configuration

### Chrome Extension Setup
1. Click the extension icon in your browser toolbar
2. Enter your Workday login credentials
3. Click "Save Credentials"
4. Navigate to any Workday login page and click "Auto Fill"

### Python Script Configuration
1. Copy `config/config_template.json` to `config.json`
2. Fill in your personal information:
   - Email and password for Workday login
   - Resume file path
   - Job URLs to apply to
   - Form field values

Example configuration:
```json
{
  "credentials": {
    "email": "your.email@company.com",
    "password": "your_password"
  },
  "resume_path": "resume.pdf",
  "job_urls": [
    "https://company.workday.com/careers/job/12345"
  ],
  "form_fields": {
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
  }
}
```

## Usage

### Chrome Extension
1. Navigate to a Workday login page
2. Click the extension icon
3. Click "Auto Fill" to automatically fill login credentials
4. Optionally enable auto-submit in extension settings

### Python Automation Script
```bash
python workday_automation.py
```

The script will:
1. Load configuration from `config.json`
2. Process each job URL in the list
3. Automatically fill application forms
4. Upload resume files
5. Submit applications
6. Generate a results report

## Configuration Options

### Chrome Extension Settings
- **Auto Submit**: Automatically submit forms after filling
- **Fill Delay**: Delay before auto-filling (in milliseconds)
- **Domain Matching**: Specify which domains to activate on

### Python Script Settings
- **Wait Time**: Delay between applications (seconds)
- **Max Retries**: Number of retry attempts for failed applications
- **Headless Mode**: Run browser in background
- **Auto Submit**: Automatically submit applications

## Form Field Mapping

The script automatically maps common form fields:

| Field Type | Common Names | Auto-Fill Value |
|------------|--------------|------------------|
| Personal Info | first_name, last_name | From config |
| Contact | email, phone, address | From config |
| Work Authorization | work_authorization | "Yes" |
| Sponsorship | sponsorship_required | "No" |
| Diversity | disability_status, veteran_status | Configurable |

## Logging and Monitoring

### Log Files
- `workday_automation.log`: Detailed application logs
- `application_results.json`: Results summary for each job

### Log Levels
- INFO: General process information
- WARNING: Non-critical issues
- ERROR: Application failures
- DEBUG: Detailed debugging information

## Error Handling

The tool includes comprehensive error handling:

### Common Issues
- **Job No Longer Available**: Automatically detected and skipped
- **Login Failures**: Retry with manual intervention option
- **Form Field Not Found**: Fallback to manual completion
- **Network Issues**: Automatic retry with exponential backoff

### Recovery Options
- Manual intervention prompts for complex forms
- Automatic retry for transient failures
- Graceful degradation for unsupported fields

## Security Considerations

### Credential Storage
- Chrome extension uses Chrome's secure storage
- Python script stores credentials in local config file
- Never commit credentials to version control

### Best Practices
- Use strong, unique passwords
- Regularly update credentials
- Monitor application logs for security issues
- Use environment variables for production deployments

## Troubleshooting

### Chrome Extension Issues
- **Extension not working**: Check if domain is in permissions
- **Credentials not saving**: Verify Chrome sync is enabled
- **Auto-fill not triggering**: Check page load timing

### Python Script Issues
- **ChromeDriver errors**: Update Chrome and ChromeDriver
- **Form field not found**: Check field selectors in code
- **Application submission failed**: Verify form completion

### Common Solutions
1. Update Chrome browser to latest version
2. Clear browser cache and cookies
3. Check network connectivity
4. Verify job URLs are accessible
5. Review log files for specific error messages

## Development

### Project Structure
```
workday-automation/
├── chrome-extension/          # Chrome extension files
│   ├── manifest.json         # Extension manifest
│   ├── content.js            # Content script
│   ├── popup.html            # Extension popup
│   ├── popup.js              # Popup functionality
│   └── background.js         # Background script
├── config/                   # Configuration files
│   └── config_template.json  # Configuration template
├── workday_automation.py     # Main Python script
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── LICENSE                   # MIT License
└── README.md                 # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Testing
```bash
# Run Python script tests
python -m pytest tests/

# Test Chrome extension
# Load extension in developer mode and test on Workday sites
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Create an issue on GitHub
4. Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Chrome extension for login auto-fill
- Python automation script
- Comprehensive configuration system
- MIT license
- Complete documentation

## Roadmap

### Planned Features
- Firefox extension support
- Advanced form field detection
- Machine learning for form mapping
- Integration with job boards
- Mobile app companion
- Cloud deployment options

### Known Limitations
- Limited to Workday platform
- Requires manual intervention for complex forms
- Chrome extension only works on supported domains
- Python script requires local Chrome installation
