"""
Tests pour l'application dashboard.
Verifie que le tableau de bord se charge correctement.
"""

from dashboard.appli import creer_application


def test_page_dashboard():
    """Le dashboard renvoie un code 200."""
    appli = creer_application()
    client = appli.test_client()
    reponse = client.get('/')
    assert reponse.status_code == 200


def test_contenu_dashboard():
    """Le dashboard contient le titre attendu."""
    appli = creer_application()
    client = appli.test_client()
    reponse = client.get('/')
    html = reponse.data.decode('utf-8')
    assert 'Tableau de bord' in html
    assert 'graphique-visibilite' in html


def test_url_api_injectee():
    """L'URL de l'API du serveur est injectee dans le template."""
    appli = creer_application()
    client = appli.test_client()
    reponse = client.get('/')
    html = reponse.data.decode('utf-8')
    assert 'http://localhost:5000' in html
