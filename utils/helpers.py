#!/usr/bin/env python3
"""
Helper utilities for Workday Automation Tool
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('workday_automation')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler('workday_automation.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary
    
    Args:
        config: Configuration dictionary to validate
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['credentials', 'job_urls']
    
    for field in required_fields:
        if field not in config:
            logging.error(f"Missing required field: {field}")
            return False
    
    # Validate credentials
    if 'email' not in config['credentials'] or 'password' not in config['credentials']:
        logging.error("Missing email or password in credentials")
        return False
    
    # Validate job URLs
    if not isinstance(config['job_urls'], list) or len(config['job_urls']) == 0:
        logging.error("job_urls must be a non-empty list")
        return False
    
    # Validate resume path
    if 'resume_path' in config:
        if not os.path.exists(config['resume_path']):
            logging.warning(f"Resume file not found: {config['resume_path']}")
    
    return True

def load_config_file(config_path: str) -> Optional[Dict[str, Any]]:
    """
    Load and validate configuration file
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Configuration dictionary or None if invalid
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if validate_config(config):
            return config
        else:
            logging.error("Configuration validation failed")
            return None
            
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in configuration file: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return None

def save_results(results: List[Dict[str, Any]], filename: str = "application_results.json") -> bool:
    """
    Save application results to file
    
    Args:
        results: List of result dictionaries
        filename: Output filename
    
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        logging.info(f"Results saved to {filename}")
        return True
        
    except Exception as e:
        logging.error(f"Error saving results: {e}")
        return False

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"

def calculate_success_rate(results: List[Dict[str, Any]]) -> float:
    """
    Calculate success rate from results
    
    Args:
        results: List of result dictionaries
    
    Returns:
        Success rate as percentage (0.0 to 1.0)
    """
    if not results:
        return 0.0
    
    successful = sum(1 for r in results if r.get('success', False))
    return successful / len(results)

def generate_summary_report(results: List[Dict[str, Any]]) -> str:
    """
    Generate a summary report from results
    
    Args:
        results: List of result dictionaries
    
    Returns:
        Formatted summary report string
    """
    if not results:
        return "No results to summarize"
    
    total = len(results)
    successful = sum(1 for r in results if r.get('success', False))
    failed = total - successful
    success_rate = calculate_success_rate(results) * 100
    
    report = f"""
Application Summary Report
========================
Total Applications: {total}
Successful: {successful}
Failed: {failed}
Success Rate: {success_rate:.1f}%

Detailed Results:
"""
    
    for i, result in enumerate(results, 1):
        status = "✓ SUCCESS" if result.get('success', False) else "✗ FAILED"
        url = result.get('url', 'Unknown URL')
        timestamp = result.get('timestamp', 'Unknown time')
        
        report += f"{i:2d}. {status} - {url} ({timestamp})\n"
        
        if not result.get('success', False) and 'error' in result:
            report += f"    Error: {result['error']}\n"
    
    return report

def sanitize_url(url: str) -> str:
    """
    Sanitize URL for logging and display
    
    Args:
        url: URL to sanitize
    
    Returns:
        Sanitized URL
    """
    # Remove sensitive parameters
    sensitive_params = ['password', 'token', 'key', 'secret']
    
    # Basic URL sanitization
    if '?' in url:
        base_url, params = url.split('?', 1)
        # Remove sensitive parameters
        param_pairs = params.split('&')
        safe_params = []
        
        for pair in param_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                if key.lower() not in sensitive_params:
                    safe_params.append(f"{key}={value}")
        
        if safe_params:
            return f"{base_url}?{'&'.join(safe_params)}"
        else:
            return base_url
    
    return url

def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """
    Retry function with exponential backoff
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        base_delay: Base delay in seconds
    
    Returns:
        Function result or raises last exception
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise e
            
            delay = base_delay * (2 ** attempt)
            logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)

def create_backup_config(config_path: str) -> bool:
    """
    Create backup of configuration file
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        True if backup created successfully
    """
    try:
        if os.path.exists(config_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{config_path}.backup_{timestamp}"
            
            with open(config_path, 'r') as src:
                with open(backup_path, 'w') as dst:
                    dst.write(src.read())
            
            logging.info(f"Configuration backup created: {backup_path}")
            return True
        
        return False
        
    except Exception as e:
        logging.error(f"Error creating backup: {e}")
        return False

def check_dependencies() -> bool:
    """
    Check if all required dependencies are available
    
    Returns:
        True if all dependencies available, False otherwise
    """
    required_modules = [
        'selenium',
        'requests',
        'json',
        'logging',
        'time',
        'os'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        logging.error(f"Missing dependencies: {', '.join(missing_modules)}")
        return False
    
    return True

def get_system_info() -> Dict[str, str]:
    """
    Get system information for debugging
    
    Returns:
        Dictionary with system information
    """
    import platform
    import sys
    
    return {
        'platform': platform.platform(),
        'python_version': sys.version,
        'architecture': platform.architecture()[0],
        'machine': platform.machine(),
        'processor': platform.processor()
    }
