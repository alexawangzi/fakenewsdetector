chrome.runtime.onMessage.addListener(
  	function(request, sender, sendResponse) {
    	if( request.message === "receiving response" ) {
            var response = JSON.parse(request.query);
            chrome.storage.sync.set({'newsData': response}, function() {
    		    console.log('Save response data to local storage');
    		    console.log(response);
    		    chrome.runtime.sendMessage({"message": "open popup"});
    		            	 chrome.storage.sync.get('newsData', function(res) {
    		    console.log(res);
    		    console.log("test");
        	});
        	});

    	}
    	if( request.message === "sending request" ) {
    		var urls = request.urls;
    		console.log(urls);
            console.log("Sending request to backend server");
    	} 
  	}
);

