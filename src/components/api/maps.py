import googlemaps
import requests

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


class MyGmaps:
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
        """Call Google Maps API. Require"""

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
                ml.exception("Le serveur renvoie un message d'erreur => {"
                             "}".format(e))
                raise

            else:
                return response

    def find(self, query):
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
        """Get the address and coordinates of the place located from the
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
    location = MyGmaps()
    result = location.find('Openclassrooms')
    print(result)


if __name__ == '__main__':
    main()
"""
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "Pont de Brotonne",
               "short_name" : "Pont de Brotonne",
               "types" : [ "establishment", "point_of_interest", "tourist_attraction" ]
            },
            {
               "long_name" : "Rives-en-Seine",
               "short_name" : "Rives-en-Seine",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Seine-Maritime",
               "short_name" : "Seine-Maritime",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Normandie",
               "short_name" : "Normandie",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "France",
               "short_name" : "FR",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "76490",
               "short_name" : "76490",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "Pont de Brotonne, 76490 Rives-en-Seine, France",
         "geometry" : {
            "location" : {
               "lat" : 49.5205268,
               "lng" : 0.7472835
            },
            "location_type" : "GEOMETRIC_CENTER",
            "viewport" : {
               "northeast" : {
                  "lat" : 49.5218757802915,
                  "lng" : 0.7486324802915021
               },
               "southwest" : {
                  "lat" : 49.5191778197085,
                  "lng" : 0.745934519708498
               }
            }
         },
         "place_id" : "ChIJecnrgiz44EcRI-9N10HL8Ec",
         "plus_code" : {
            "compound_code" : "GPCW+6W Rives-en-Seine, France",
            "global_code" : "8FX2GPCW+6W"
         },
         "types" : [ "establishment", "point_of_interest", "tourist_attraction" ]
      }
   ],
   "status" : "OK"
}
"""