chrome.runtime.onMessage.addListener(
  	function(request, sender, sendResponse) {
    	if( request.message === "receiving response" ) {
            var response = JSON.parse(request.query);
            console.log(response);
    	}
    	if( request.message === "sending request" ) {
            console.log("sending request");
    	} 
  	}
);

