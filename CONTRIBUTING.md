# Contributing to Workday Automation Tool

Thank you for your interest in contributing to the Workday Automation Tool! This document provides guidelines and information for contributors.

## Code of Conduct

This project follows a code of conduct that ensures a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Chrome browser
- Basic understanding of Selenium and web automation

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/workday-automation.git
   cd workday-automation
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. **Install Chrome Extension**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `chrome-extension` folder

4. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

## Contribution Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Report issues and bugs
- **Feature Requests**: Suggest new features
- **Code Contributions**: Submit code improvements
- **Documentation**: Improve documentation
- **Testing**: Add or improve tests
- **Examples**: Add usage examples

### Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the problem
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, browser version
6. **Logs**: Relevant log files or error messages
7. **Screenshots**: If applicable

### Feature Requests

When requesting features, please include:

1. **Use Case**: Why this feature would be useful
2. **Proposed Solution**: How you envision it working
3. **Alternatives**: Other solutions you've considered
4. **Additional Context**: Any other relevant information

### Code Contributions

#### Development Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description
   ```

2. **Make Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   python -m pytest tests/
   python workday_automation.py --test-mode
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Code Style Guidelines

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Use consistent formatting
- **Comments**: Write clear, helpful comments
- **Naming**: Use descriptive variable and function names
- **Functions**: Keep functions focused and small
- **Error Handling**: Include proper error handling

#### Testing Requirements

- **Unit Tests**: Add tests for new functionality
- **Integration Tests**: Test component interactions
- **Manual Testing**: Test with real Workday sites
- **Edge Cases**: Test error conditions and edge cases

### Documentation Contributions

#### Types of Documentation

- **README Updates**: Improve main documentation
- **API Documentation**: Document functions and classes
- **Code Comments**: Add inline documentation
- **Examples**: Create usage examples
- **Troubleshooting**: Add common issues and solutions

#### Documentation Standards

- **Clarity**: Write clear, concise documentation
- **Examples**: Include practical examples
- **Accuracy**: Ensure information is current and correct
- **Formatting**: Use proper markdown formatting
- **Links**: Include relevant links and references

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Test improvements
- `refactor/description` - Code refactoring

### Commit Messages

Use clear, descriptive commit messages:

```
Add feature: Chrome extension auto-fill functionality
Fix bug: Handle missing form fields gracefully
Update docs: Add installation instructions
Refactor: Improve error handling in automation script
```

### Pull Request Process

1. **Create Pull Request**
   - Use descriptive title and description
   - Reference related issues
   - Include screenshots if applicable

2. **Review Process**
   - Code will be reviewed by maintainers
   - Address feedback and suggestions
   - Update documentation if needed

3. **Testing**
   - Ensure all tests pass
   - Test on different platforms if possible
   - Verify Chrome extension functionality

4. **Merge**
   - PR will be merged after approval
   - Feature will be included in next release

## Testing Guidelines

### Unit Testing

```python
import unittest
from workday_automation import WorkdayAutomation

class TestWorkdayAutomation(unittest.TestCase):
    def test_config_loading(self):
        # Test configuration loading
        pass
    
    def test_form_filling(self):
        # Test form filling functionality
        pass
```

### Integration Testing

```python
def test_full_application_process():
    # Test complete application workflow
    pass
```

### Manual Testing

1. **Chrome Extension**
   - Test on different Workday sites
   - Verify credential storage
   - Test auto-fill functionality

2. **Python Script**
   - Test with sample job URLs
   - Verify form field detection
   - Test error handling

## Code Review Guidelines

### For Contributors

- **Self-Review**: Review your own code before submitting
- **Test Thoroughly**: Ensure all functionality works
- **Document Changes**: Update relevant documentation
- **Respond to Feedback**: Address review comments promptly

### For Reviewers

- **Be Constructive**: Provide helpful feedback
- **Test Changes**: Verify functionality works
- **Check Documentation**: Ensure docs are updated
- **Consider Impact**: Think about broader implications

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number updated
- [ ] Release notes prepared
- [ ] Tag created

## Community Guidelines

### Communication

- **Be Respectful**: Treat everyone with respect
- **Be Constructive**: Provide helpful feedback
- **Be Patient**: Allow time for responses
- **Be Clear**: Communicate clearly and concisely

### Getting Help

- **Documentation**: Check existing documentation first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub discussions for questions
- **Code Review**: Ask questions during code review

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- **README**: Listed in contributors section
- **Changelog**: Mentioned in release notes
- **GitHub**: Listed in contributors on GitHub

## Contact

For questions about contributing:
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub discussions
- **Email**: Contact maintainers directly

Thank you for contributing to the Workday Automation Tool!
