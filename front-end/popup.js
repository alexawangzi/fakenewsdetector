function populateData() {
	chrome.storage.sync.get('newsData', function(result) {
		var news = result.newsData.news;
		var bias = result.newsData.bias;
		var sentiment = result.newsData.sentiment;

		var marker2pc = (sentiment.score+1)*100/2;
		var sentiment = "";
		if (-0.1 <= sentiment.score && 0.1 >= sentiment.score && sentiment.magnitude <= 1.5) {
			sentiment = "neutral";
		} else if (sentiment.score > 0.1) {
			sentiment = "positive";
		} else if (sentiment.score < -0.1) {
			sentiment = "negative";
		} else {
			sentiment = "mixed";
		}
		document.getElementById("sentiment").innerHTML = "Sentiment: " + sentiment;
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
        } else {
        	var sourceTextBody = "";
        	bias.forEach(source => {
        		sourceTextBody += "<div class='source'>";
        		sourceTextBody += "<div><b>" + source.name + "</b></div>";
        		sourceTextBody += "<div>Category: " + source.category + "</b></div>";
        		sourceTextBody += "<div>Factual level: " + source.factual + "</b></div>";
        		sourceTextBody += "</div>";
        	})
        	document.getElementById("source-trustworthyness").innerHTML = sourceTextBody;
        }
    });
}

populateData();
