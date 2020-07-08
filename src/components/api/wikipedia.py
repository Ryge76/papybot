import requests

import logging

wl = logging.getLogger('components.wikipedia')


class WikipediaModuleError(Exception):
    """Defining module specific errors"""
    pass


class Wikipedia:
    """Access wikipedia API for search on name. Requiere a string for instanciation.
    'infos' property keep a dict containing an extract and the url of found page.
    Only the first page found on wikipedia (sorted by relevance) is queried"""

    URL = "https://fr.wikipedia.org/w/api.php"

    def __init__(self, query):
        self.global_search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "srsearch": None,
            "srenablerewrites": 1,
            "srsort": "relevance"
        }

        self.page_search_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "pageids": None,
            "utf8": 1,
            "exsentences": "3",
            "exintro": 1,
            "explaintext": 1,
            "inprop": "url"
        }

        self.query = query

        if len(self.query) == 0:
            wl.error('Mauvaise initiation de la recherche: au moins un '
                     'mot-clé est nécessaire pour lancer la recherche.')
            raise WikipediaModuleError

        self.session = requests.Session()
        self.result_page_id = self._find_page_id()
        self.infos = self._get_infos(self.result_page_id)

    def _call_api(self, params):
        """Call wikipedia api with specific parameters
        Return a dict containing the API response."""

        # Check connection to Wikipedia API
        try:
            response = self.session.get(url=self.URL, params=params,
                                        timeout=5)

        except requests.exceptions.RequestException as e:
            message = 'Une erreur de connexion est survenue => {}'.format(e)
            wl.exception(message)
            raise WikipediaModuleError

        else:
            # Check answer'status from API
            if response.status_code == requests.codes.OK:
                try:
                    # Check if Requests can decode the json
                    data = response.json()

                except requests.exceptions.ContentDecodingError as e:
                    message = 'Problème avec le JSON reçu => {}'.format(e)
                    wl.exception(message)
                    raise WikipediaModuleError

                else:
                    # Wikipedia send back a json with a error section in
                    # case of bad request. But the http code is still 200...
                    if "error" in data.keys():
                        wl.error("Le serveur Wikipedia indique une erreur"
                                 " => {}.".format(data.get('error')))
                        raise WikipediaModuleError

                    else:
                        return data

            else:
                # Check if response'status is 400 or 500 and raise an error
                # accordingly
                try:
                    response.raise_for_status()

                except requests.exceptions.HTTPError as e:
                    message = "Le serveur wikipedia a répondu avec le code" \
                              " {} => {}".format(response.status_code, e)
                    wl.exception(message)
                    raise WikipediaModuleError

    def _find_page_id(self):
        """Get id of the first page corresponding to the query. 
        Return an integer corresponding to the page id"""

        # add query to parameters for the api call
        self.global_search_params.update({"srsearch": self.query})

        # call to wikipedia API
        try:
            data = self._call_api(self.global_search_params)

        except requests.exceptions.RequestException:
            raise WikipediaModuleError

        else:
            page_id = data['query']['search'][0].get('pageid')
            return page_id

    def _get_infos(self, page_id):
        """Get extract of a specific page. 
        Require a page id. 
        Return a dict containing page extract and url.
        ."""

        # add page id to parameters for the api call
        self.page_search_params.update({"pageids": page_id})

        # call to wikipedia API
        try:
            data = self._call_api(self.page_search_params)

        except requests.exceptions.RequestException as e:
            wl.exception(e)
            raise WikipediaModuleError

        else:
            extract = data['query']['pages'][str(page_id)].get('extract')
            page_url = data['query']['pages'][str(page_id)].get('fullurl')

            return {"extract": extract, "url": page_url}


def main():
    test_search = Wikipedia("Paris")
    print(test_search.result_page_id)
    print("Extrait: \n {a} \n Lien: {b}".format(a=test_search.infos.get(
        "extract"), b=test_search.infos.get("url")))


if __name__ == '__main__':
    main()
