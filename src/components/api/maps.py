import os
import logging

import requests

# create maps logger as ml for short
ml = logging.getLogger('components.maps')


class GmapsModuleError(Exception):
    """Define specific module error"""
    pass


class Gmaps:
    """Use Google Maps API to get address and coordinates upon search.
    Return a dictionary address and coordinates."""

    GMAPS_KEY = os.environ.get("GMAPS_KEY")
    URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(self):
        self.session = requests.Session()
        self.parameters = {'address': None,
                           'key': self.GMAPS_KEY
                           }

    def _call_api(self, parameters):
        """Call Google Maps API. Require a dict containing the API key and
        at least an 'address' parameter.
        Return a Response object."""

        try:
            response = self.session.get(url=self.URL, params=parameters,
                                        timeout=5)

        except requests.exceptions.RequestException as e:
            message = 'Une erreur de connexion est survenue => {}'.format(e)
            ml.exception(message)
            raise GmapsModuleError

        else:
            try:
                response.raise_for_status()

            except requests.exceptions.HTTPError as e:
                ml.exception("Le serveur renvoie un message "
                             "d'erreur => {}".format(e))
                raise

            else:
                return response

    def find(self, query):
        """Get coordinates and address of the place in query.
        Require string. Return a dict."""


        self.parameters.update({'address': query})

        try:
            api_response = self._call_api(self.parameters)

        except requests.exceptions.RequestException:
            ml.exception("Echec de la requête")
            raise GmapsModuleError

        try:
            results = self._extract_result(api_response)

        except requests.exceptions.ContentDecodingError:
            raise GmapsModuleError

        except KeyError:
            raise GmapsModuleError

        except Exception:
            raise GmapsModuleError

        else:
            return results

    @staticmethod
    def _extract_result(api_response):
        """Extract the address and coordinates of the place located from the
        response object.
        Require a response object. Return a dict."""

        try:
            source = api_response.json()

        except requests.exceptions.ContentDecodingError as e:
            message = 'Problème avec le JSON reçu => {}'.format(e)
            ml.exception(message)
            raise

        else:
            try:
                extract = {'address': source['results'][0].get('formatted_address'),
                           'coord': source['results'][0]['geometry'].get('location')}

            except KeyError as e:
                ml.exception(e)
                raise

            else:
                return extract


def main():
    location = Gmaps()
    result = location.find('Openclassrooms')
    print("L'adresse d'Openclassrooms est {address} et ses coordonnées: {"
          "coord}".format(**result))


if __name__ == '__main__':
    main()