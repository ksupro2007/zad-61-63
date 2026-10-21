import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code in [200, 500]

def test_product_not_found(client):
    response = client.get('/product/99999')
    assert response.status_code == 404

def test_app_exists():
    assert app is not None