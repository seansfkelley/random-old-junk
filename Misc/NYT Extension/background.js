function checkForValidUrl(tabId, changeInfo, tab) {
    if (tab.url.indexOf('&gwh=') > -1) {
        chrome.pageAction.show(tabId);
    }
};
chrome.tabs.onUpdated.addListener(checkForValidUrl);
chrome.pageAction.onClicked.addListener(function(tab) {
    var new_url = tab.url.substring(0, tab.url.indexOf("&gwh="));
    chrome.tabs.update(tab.id, {"url": new_url});
});