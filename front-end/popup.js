function populateData() {
	chrome.storage.sync.get('newsData', function(result) {
		var news = result.newsData.news;
		var bias = result.newsData.bias;
		var sentiment = result.newsData.sentiment;

		var marker1pc = sentiment.magnitude*100/2;
		var marker2pc = (sentiment.score+1)*100/2;
		document.getElementById("marker1").style.width = marker1pc + "%";
		document.getElementById("marker2").style.width = marker2pc + "%";
        document.getElementById("article-count").innerHTML = "<b>Article found: " + news.articleCount + "</b>";

        var articleBodyText = "";
        if (news.articleCount == 0) {
        	articleBodyText = "No relevant article found."
        } else {
        	news.articles.forEach(article => {
        		articleBodyText += "<div class='article'>";
        		articleBodyText += "<div><b>" + article.title + "</b></div>";
        		articleBodyText += "<a href='" + article.url +"'>" + article.source.name + "</a>";
        		articleBodyText += "</div>";
        	})
        }
        document.getElementById("suggested-articles").innerHTML = articleBodyText;
        if (bias.length == 0) {
        	document.getElementById("source-trustworthyness").innerHTML = "No information about source found/provided";
        }
    });
}

populateData();
