import pytest
import requests

from ...src.components.api.wikipedia import Wikipedia


# ---- Defining fixtures and mocks used for testing ---- #

sample_data = {'searchinfo': {'totalhits': 397460}, 'search': [{'ns': 0, 'title': 'Paris', 'pageid': 681159, 'size': 404111, 'wordcount': 44331, 'snippet': 'significations, voir <span class="searchmatch">Paris</span> (homonymie). «\xa0Ville Lumière\xa0» redirige ici. Ne pas confondre avec Ville de lumière ni la villa Lumière. <span class="searchmatch">Paris</span> [pa.ʁi] Écouter est', 'timestamp': '2020-07-12T09:15:03Z'}, {'ns': 0, 'title': 'Pâris', 'pageid': 47880, 'size': 16380, 'wordcount': 1885, 'snippet': 'les articles homonymes, voir <span class="searchmatch">Paris</span> (homonymie). Dans la mythologie grecque, <span class="searchmatch">Pâris</span> [<span class="searchmatch">paʁis</span>] (en grec ancien Πάρις\xa0/ <span class="searchmatch">Páris</span>) ou Alexandre (en grec ancien', 'timestamp': '2020-07-07T18:37:03Z'}, {'ns': 0, 'title': 'Paris-Brest-Paris', 'pageid': 677105, 'size': 14168, 'wordcount': 1472, 'snippet': 'voir <span class="searchmatch">Paris</span>-Brest. <span class="searchmatch">Paris</span>-Brest-<span class="searchmatch">Paris</span> Affiche de 1901 représentant le vainqueur Maurice Garin de l\'équipe La Française <span class="searchmatch">Paris</span>-Brest-<span class="searchmatch">Paris</span>, ou <span class="searchmatch">Paris</span>-Brest', 'timestamp': '2020-07-04T12:46:52Z'}, {'ns': 0, 'title': 'Arrondissements de Paris', 'pageid': 15830, 'size': 46470, 'wordcount': 3131, 'snippet': 'avec l\'Arrondissement de <span class="searchmatch">Paris</span>. Les arrondissements de <span class="searchmatch">Paris</span> sont des divisions administratives intracommunales qui partagent <span class="searchmatch">Paris</span>, la capitale de la France', 'timestamp': '2020-07-11T06:31:38Z'}, {'ns': 0, 'title': 'Paris sera toujours Paris', 'pageid': 11362060, 'size': 3629, 'wordcount': 168, 'snippet': 'avec <span class="searchmatch">Paris</span> est toujours <span class="searchmatch">Paris</span>. <span class="searchmatch">Paris</span> sera toujours <span class="searchmatch">Paris</span> <span class="searchmatch">Paris</span> sera toujours <span class="searchmatch">Paris</span> Clip vidéo [vidéo] <span class="searchmatch">Paris</span> sera toujours <span class="searchmatch">Paris</span> sur YouTube <span class="searchmatch">Paris</span> sera', 'timestamp': '2020-05-04T23:16:17Z'}, {'ns': 0, 'title': 'Paris est toujours Paris', 'pageid': 6844326, 'size': 7349, 'wordcount': 768, 'snippet': 'confondu avec <span class="searchmatch">Paris</span> sera toujours <span class="searchmatch">Paris</span>. <span class="searchmatch">Paris</span> est toujours <span class="searchmatch">Paris</span> Pour plus de détails, voir Fiche technique et Distribution <span class="searchmatch">Paris</span> est toujours <span class="searchmatch">Paris</span> (titre', 'timestamp': '2020-05-24T14:40:26Z'}, {'ns': 0, 'title': 'Paris-Marseille-Paris', 'pageid': 9513876, 'size': 105980, 'wordcount': 5025, 'snippet': '<span class="searchmatch">Paris</span>-Marseille-<span class="searchmatch">Paris</span> no\xa06 Panhard-Levassor piloté par Émile Mayade, vainqueur de la course. <span class="searchmatch">Paris</span>-Marseille-<span class="searchmatch">Paris</span> est la première course automobile organisée', 'timestamp': '2020-03-21T17:07:55Z'}, {'ns': 0, 'title': 'Métro de Paris', 'pageid': 66173, 'size': 259941, 'wordcount': 25253, 'snippet': 'partie d\'un «\xa0bon thème\xa0». Le métro de <span class="searchmatch">Paris</span> est l\'un des systèmes de transport en commun desservant la ville de <span class="searchmatch">Paris</span> et son agglomération. Exploité par', 'timestamp': '2020-07-02T09:30:26Z'}, {'ns': 0, 'title': 'Paris-Bordeaux-Paris', 'pageid': 6714041, 'size': 56705, 'wordcount': 3490, 'snippet': 'homonymes, voir <span class="searchmatch">Paris</span>-Bordeaux. <span class="searchmatch">Paris</span>-Bordeaux-<span class="searchmatch">Paris</span> Monument commémoratif de l\'arrivée d\'Émile Levassor La course <span class="searchmatch">Paris</span>-Bordeaux-<span class="searchmatch">Paris</span> du 11 juin 1895', 'timestamp': '2020-04-13T12:17:50Z'}, {'ns': 0, 'title': 'Conseil de Paris', 'pageid': 609268, 'size': 24450, 'wordcount': 1863, 'snippet': 'municipal (France) et <span class="searchmatch">Paris</span>. Ne doit pas être confondu avec le Conseil municipal de <span class="searchmatch">Paris</span> qui l\'a précédé jusqu\'en 1967. Conseil de <span class="searchmatch">Paris</span> Composition actuelle', 'timestamp': '2020-06-30T13:02:11Z'}]}


@pytest.fixture
def mock_response():
    """Create fake response object"""
    class FakeResponse:
        @staticmethod
        def json():
            return sample_data

    return FakeResponse()


@pytest.fixture
def wikipedia_test_instance():
    return Wikipedia('test', auto=False)


# ----- Tests ------ #

def test_api_call_return_response_object(wikipedia_test_instance):
    custom_test_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": "Paris",
        "srenablerewrites": 1,
        "srsort": "relevance"
    }
    expected_url = 'https://fr.wikipedia.org/w/api.php?action=query&format=json&list=search&utf8=1&srsearch=Paris&srenablerewrites=1&srsort=relevance'

    result = wikipedia_test_instance._call_api(custom_test_params)

    assert isinstance(result, requests.models.Response)
    assert result.url == expected_url


def test_get_data_from_response(wikipedia_test_instance, mock_response):
    """Should return a dict similar to our sample_data"""
    result = wikipedia_test_instance._get_data_from_response(mock_response)
    expected_data = sample_data
    assert result == expected_data


def test_find_page_id(wikipedia_test_instance):
    """Should return the 'pageid' integer from the response received from
     Wikipedia"""

    wikipedia_test_instance.query = 'Paris'
    result = wikipedia_test_instance._find_page_id()

    expected_id = 681159
    assert result == expected_id


def test_get_infos(wikipedia_test_instance, test_id = 681159):
    """Given a page_id should return a dict containing the page url and an
    extract of it."""

    result = wikipedia_test_instance._get_infos(test_id)

    expected_extract = "Paris [pa.ʁi]  est la ville la plus peuplée et la capitale de la France.\nElle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016."

    assert isinstance(result, dict)
    assert result.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert result.get('extract') == expected_extract
