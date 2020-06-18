import requests


class Wikipedia:
    """Access wikipedia API for search on name"""
    URL = "https://fr.wikipedia.org/w/api.php"

    def __init__(self, query):
        self.global_search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "srsearch": "",
            "srenablerewrites": 1,
            "srsort": "relevance"
        }

        self.page_search_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "pageids": "",
            "utf8": 1,
            "exsentences": "3",
            "exintro": 1,
            "explaintext": 1,
            "inprop": "url"
        }

        self.query = query
        self.session = requests.Session()
        result_page_id = self.find_page_id()
        self.infos = self.get_infos(result_page_id)

    def call_api(self, params):
        """Call wikipedia api with specific parameters"""
        response = self.session.get(url=self.URL, params=params)
        data = response.json()

        return data

    def find_page_id(self):
        """Get id of the first page corresponding to the query. Return an
        integer corresponding to the page id"""

        # add query to parameters for the api call
        self.global_search_params.update({"srsearch": self.query})

        # call to wikipedia API
        data = self.call_api(self.global_search_params)

        page_id = data['query']['search'][0].get('pageid')

        return page_id

    def get_infos(self, page_id):
        """Get extract of a specific page. Require a page id. Return a dict
        containing page extract and url
        ."""

        # add page id to parameters for the api call
        self.page_search_params.update({"pageids": page_id})

        # call to wikipedia API
        data = self.call_api(self.page_search_params)

        extract = data['query']['pages'][str(page_id)].get('extract')
        page_url = data['query']['pages'][str(page_id)].get('fullurl')

        return {"extract": extract, "url": page_url}


def main():
    test_search = Wikipedia("Paris")
    print("Extrait: \n {a} \n Lien: {b}".format(a=test_search.infos.get(
        "extract"), b=test_search.infos.get("url")))


if __name__ == '__main__':
    main()







