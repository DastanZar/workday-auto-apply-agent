// Workday Auto Login Background Script
chrome.runtime.onInstalled.addListener(function(details) {
    if (details.reason === 'install') {
        console.log('Workday Auto Login extension installed');
        
        // Set default settings
        chrome.storage.sync.set({
            autoSubmit: false,
            autoFillDelay: 1000
        });
    }
});

// Handle extension icon click
chrome.action.onClicked.addListener(function(tab) {
    // This will open the popup automatically due to manifest configuration
});

// Listen for tab updates to auto-fill on Workday pages
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.status === 'complete' && tab.url) {
        if (tab.url.includes('workday.com') || tab.url.includes('myworkday.com')) {
            console.log('Workday page detected:', tab.url);
            
            // Optional: Auto-fill credentials when Workday page loads
            chrome.storage.sync.get(['autoSubmit'], function(result) {
                if (result.autoSubmit) {
                    setTimeout(() => {
                        chrome.tabs.sendMessage(tabId, {action: 'autoFill'});
                    }, 2000);
                }
            });
        }
    }
});
