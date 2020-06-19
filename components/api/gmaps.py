import requests


class Gmaps:
    """Class allowing to call Google Maps API. Require a query string. Response is saved in the 'response' attribute of
    the class"""
    
    URL = "https://www.google.com/maps/search/?api=1"

    def __init__(self, query):
        self.query = query

        self.params = {"query": self.query}
        self.response = self.call_api()

    def call_api(self):
        """Call Google Maps API with specified query. Return the response object"""
        session = requests.Session()
        response = session.get(url=self.URL, params=self.params)
        return response

    def convert_query(self, query):
        """Convert query string to a valid URL encoding."""
        pass


def main():
    test = Gmaps("Openclassrooms")
    print(test.response.headers)


if __name__ == '__main__':
    main()
