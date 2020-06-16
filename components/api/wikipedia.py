"""
racine: https://fr.wikipedia.org/
Pour recherche en général

/w/api.php?action=query&format=json&list=search&utf8=1&srsearch=cite%20paradis&srenablerewrites=1&srsort=relevance
{
	"action": "query",
	"format": "json",
	"list": "search",
	"utf8": 1,
	"srsearch": "cite paradis",
	"srenablerewrites": 1,
	"srsort": "relevance"
}


Pour recherche sur un id de page spécifique
/w/api.php?action=query&format=json&prop=extracts%7Cinfo&pageids=7856&utf8=1&exintro=1&explaintext=1&inprop=url
{
	"action": "query",
	"format": "json",
	"prop": "extracts|info",
	"pageids": ""7856|133038"",
	"utf8": 1,
    "exsentences": "3",
	"exintro": 1,
	"explaintext": 1,
	"inprop": "url"
}


"""
