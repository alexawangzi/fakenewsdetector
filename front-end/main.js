evaluateNews = function(word){
	var query = word.selectionText;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		var activeTab = tabs[0];

		var urls = extractUrls(query);

		chrome.tabs.sendMessage(activeTab.id, {"message": "sending request", "urls": urls});

		var req = new XMLHttpRequest();
		const baseURL = "https://fakenewscrosscheck.appspot.com";
		
		req.open("POST", baseURL, true);
		req.setRequestHeader("Content-Type", "application/json");
		req.send(JSON.stringify({"newsContent": query, "urls": urls}));

		req.onreadystatechange = function() {
			if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
				chrome.storage.sync.set({'newsData':  this.responseText}, function() {
        		});
				chrome.tabs.sendMessage(activeTab.id, {"message": "receiving response", "query": this.responseText});
			}
		}
	});
};


extractUrls = function(query) {
	var uri_pattern = /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi;
	let uris = query.match(uri_pattern);
	let strippedUris = [];
	if (uris != null && uris.length > 0) {
		uris.forEach(uri => {
			uri = uri.replace("https://", "");
			uri = uri.replace("http://", "");
			uri = uri.split("/")[0];
			strippedUris.push(uri);
		});
	}
	return strippedUris;
}

sendRequest = function(query) {
	console.log(query);
}

chrome.runtime.onMessage.addListener(
  	function(request, sender, sendResponse) {
    	if( request.message === "open popup" ) {
			window.open("popup.html", "extension_popup", "width=300,height=500, status=no, scrollbars=yes, resizable=no");
    	}
  	}
);

chrome.contextMenus.create({
	title: "Evaluate news",
	contexts:["selection"],  // ContextType
	onclick: evaluateNews    // A callback function
});