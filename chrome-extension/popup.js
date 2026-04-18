// Workday Auto Login Popup Script
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('credentialsForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const autoFillBtn = document.getElementById('autoFillBtn');
    const statusDiv = document.getElementById('status');

    // Load saved credentials
    chrome.storage.sync.get(['workdayEmail', 'workdayPassword'], function(result) {
        if (result.workdayEmail) {
            emailInput.value = result.workdayEmail;
        }
        if (result.workdayPassword) {
            passwordInput.value = result.workdayPassword;
        }
    });

    // Save credentials
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        
        if (!email || !password) {
            showStatus('Please fill in both email and password', 'error');
            return;
        }
        
        chrome.storage.sync.set({
            workdayEmail: email,
            workdayPassword: password
        }, function() {
            showStatus('Credentials saved successfully!', 'success');
        });
    });

    // Auto fill button
    autoFillBtn.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: 'autoFill'}, function(response) {
                if (chrome.runtime.lastError) {
                    showStatus('Please navigate to a Workday login page first', 'error');
                } else if (response && response.success) {
                    showStatus('Credentials filled successfully!', 'success');
                } else {
                    showStatus('Auto-fill failed. Make sure you are on a Workday login page', 'error');
                }
            });
        });
    });

    // Show status message
    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `status ${type}`;
        statusDiv.style.display = 'block';
        
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 3000);
    }
});
