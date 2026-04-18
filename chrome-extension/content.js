// Workday Auto Login Content Script
(function() {
    'use strict';

    // Configuration for different Workday login forms
    const LOGIN_SELECTORS = {
        email: [
            'input[type="email"]',
            'input[name="email"]',
            'input[id*="email"]',
            'input[data-automation-id="email"]',
            'input[placeholder*="email" i]',
            'input[placeholder*="Email" i]'
        ],
        password: [
            'input[type="password"]',
            'input[name="password"]',
            'input[id*="password"]',
            'input[data-automation-id="password"]'
        ],
        submit: [
            'button[type="submit"]',
            'input[type="submit"]',
            'button[data-automation-id="click_filter"]',
            'button:contains("Sign In")',
            'button:contains("Login")',
            'button:contains("Log In")'
        ]
    };

    // Auto-fill function
    function autoFillCredentials() {
        return new Promise((resolve) => {
            chrome.storage.sync.get(['workdayEmail', 'workdayPassword'], function(result) {
                if (!result.workdayEmail || !result.workdayPassword) {
                    console.log('Workday Auto Login: No credentials found');
                    resolve(false);
                    return;
                }

                let emailFilled = false;
                let passwordFilled = false;

                // Try to fill email
                for (const selector of LOGIN_SELECTORS.email) {
                    const emailField = document.querySelector(selector);
                    if (emailField && emailField.offsetParent !== null) {
                        emailField.focus();
                        emailField.value = result.workdayEmail;
                        emailField.dispatchEvent(new Event('input', { bubbles: true }));
                        emailField.dispatchEvent(new Event('change', { bubbles: true }));
                        emailFilled = true;
                        console.log('Workday Auto Login: Email filled');
                        break;
                    }
                }

                // Try to fill password
                for (const selector of LOGIN_SELECTORS.password) {
                    const passwordField = document.querySelector(selector);
                    if (passwordField && passwordField.offsetParent !== null) {
                        passwordField.focus();
                        passwordField.value = result.workdayPassword;
                        passwordField.dispatchEvent(new Event('input', { bubbles: true }));
                        passwordField.dispatchEvent(new Event('change', { bubbles: true }));
                        passwordFilled = true;
                        console.log('Workday Auto Login: Password filled');
                        break;
                    }
                }

                if (emailFilled && passwordFilled) {
                    console.log('Workday Auto Login: Credentials filled successfully');
                    
                    // Optional: Auto-submit after a short delay
                    setTimeout(() => {
                        for (const selector of LOGIN_SELECTORS.submit) {
                            const submitButton = document.querySelector(selector);
                            if (submitButton && submitButton.offsetParent !== null) {
                                submitButton.click();
                                console.log('Workday Auto Login: Form submitted');
                                break;
                            }
                        }
                    }, 500);
                }

                resolve(emailFilled && passwordFilled);
            });
        });
    }

    // Check if current page is a Workday login page
    function isWorkdayLoginPage() {
        const url = window.location.href.toLowerCase();
        const bodyText = document.body.textContent.toLowerCase();
        
        return (
            url.includes('workday.com') ||
            url.includes('myworkday.com') ||
            bodyText.includes('workday') ||
            bodyText.includes('sign in') ||
            bodyText.includes('login')
        );
    }

    // Main execution
    function init() {
        if (isWorkdayLoginPage()) {
            console.log('Workday Auto Login: Login page detected');
            
            // Wait for page to be fully loaded
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    setTimeout(autoFillCredentials, 1000);
                });
            } else {
                setTimeout(autoFillCredentials, 1000);
            }
        }
    }

    // Initialize
    init();

    // Listen for messages from popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'autoFill') {
            autoFillCredentials().then(success => {
                sendResponse({ success: success });
            });
            return true;
        }
    });

})();
