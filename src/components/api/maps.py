import os

import googlemaps


class Gmaps:
    """Use Google Maps API to get address and coordinates upon search.
    Requiere a string query. Return a dictionary address and coordinates."""

    GMAPS_KEY = os.environ.get("GMAPS_KEY")

    def __init__(self):

        self.gmaps_service = googlemaps.Client(key=self.GMAPS_KEY)
        self.about_query = []

    def get(self, query):

        try:
            self.about_query = self.gmaps_service.geocode(query)

        except Exception as e:
            raise Exception('Cette erreur de connexion est survenue => {}'.format(e))

        else:
            result = {'address': self.about_query[0].get('formatted_address'),
                      'coord': self.about_query[0]['geometry'].get('location')}

            return result


def main():
    location = Gmaps()
    result = location.get('Openclassrooms')
    print(result)


if __name__ == '__main__':
    main()
