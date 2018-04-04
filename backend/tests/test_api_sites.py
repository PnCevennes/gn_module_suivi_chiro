import requests

from .bootstrap_test import geonature_app


class TestApiModulePrConcact:
    """
        Test de l'api du module pr_contact
    """

    def get_token(self, base_url, login="admin", password="admin"):
        response = requests.post(
            '{}/auth/login'.format(base_url),
            json={
                'login': login,
                'password': password,
                'id_application': 14,
                'with_cruved': True
            }
        )
        if response.ok:
            return response.cookies['token']
        else:
            raise Exception('Invalid login {}, {}'.format(login, password))

    def test_get_sites(self, geonature_app):
        token = self.get_token(geonature_app.config['API_ENDPOINT'])
        # Test récupérer la liste des sites
        response = requests.get(
            '{}/suivi_chiro/sites'.format(
                geonature_app.config['API_ENDPOINT']
            ),
            cookies={'token': token}
        )
        assert response.status_code == 200

        data = (response.json())
        id_site = data[0]['properties']['id_base_site']

        # Test récupérer le détail d'un site
        response = requests.get(
            '{}/suivi_chiro/site/{}'.format(
                geonature_app.config['API_ENDPOINT'],
                id_site
            ),
            cookies={'token': token}
        )
        assert response.status_code == 200