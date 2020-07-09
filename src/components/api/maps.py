import googlemaps

import os
import logging

# create maps logger as ml for short
ml = logging.getLogger('components.maps')


class GmapsModuleError(Exception):
    """Define specific """
    pass


class Gmaps:
    """Use Google Maps API to get address and coordinates upon search.
    Return a dictionary address and coordinates."""

    GMAPS_KEY = os.environ.get("GMAPS_KEY")

    def __init__(self):

        try:
            self.gmaps_service = googlemaps.Client(key=self.GMAPS_KEY)

        except ValueError as e:
            ml.exception("Clé d'API invalide => {}".format(e))
            raise GmapsModuleError

        except googlemaps.exceptions.TransportError as e:
            ml.exception("Un problème de réseau est survenue => {}".format(e))
            raise GmapsModuleError

        else:
            self.about_query = []

    def get(self, query):
        ml.info('La géolocalisation de {} est lancée.'.format(query))

        try:
            self.about_query = self.gmaps_service.geocode(query)

        except googlemaps.exceptions.HTTPError as e:
            message = 'Cette erreur de connexion est survenue => {}'.format(e)
            ml.exception(message)
            raise GmapsModuleError

        except googlemaps.exceptions.ApiError as e:
            message = "Cette erreur de l'API est survenue => {}".format(e)
            ml.exception(message)
            raise GmapsModuleError

        except googlemaps.exceptions.TransportError as e:
            message = 'Cette erreur de connexion est survenue => {}'.format(e)
            ml.exception(message)
            raise GmapsModuleError

        except googlemaps.exceptions.Timeout as e:
            message = 'Cette erreur de connexion est survenue => {}'.format(e)
            ml.exception(message)
            raise GmapsModuleError

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
