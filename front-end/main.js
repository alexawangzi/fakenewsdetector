evaluateNews = function(word){
	var query = word.selectionText;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	var activeTab = tabs[0];

        chrome.tabs.sendMessage(activeTab.id, {"message": "sending request"});

    	var req = new XMLHttpRequest();
      	const baseURL = "https://fakenewscrosscheck.appspot.com";
		req.open("POST", baseURL, true);
        req.setRequestHeader("Content-Type", "application/json");
        req.send(JSON.stringify({"newsContent": query}));
    	req.onreadystatechange = function() { // Call a function when the state changes.
        	if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            	chrome.tabs.sendMessage(activeTab.id, {"message": "receiving response", "query": this.responseText});
        	}
    	}

  	});
};

sendRequest = function(query) {
	console.log(query);
}

chrome.contextMenus.create({
 	title: "Evaluate news",
 	contexts:["selection"],  // ContextType
 	onclick: evaluateNews    // A callback function
});