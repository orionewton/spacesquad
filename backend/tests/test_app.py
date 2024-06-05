# tests/test_app.py
import pytest
from backend.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test que la page d'accueil se charge correctement."""
    rv = client.get('/')
    assert rv.status_code == 200
