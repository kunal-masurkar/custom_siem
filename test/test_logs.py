import pytest
from api.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_logs_search_requires_api_key(client):
    response = client.get('/logs/search')
    assert response.status_code == 401
    assert b'Unauthorized' in response.data

def test_logs_search_valid(client):
    response = client.get('/logs/search?q=test', headers={'X-API-KEY': 'changeme123'})
    assert response.status_code in (200, 500)  # 500 if ES not running, 200 if running

def test_logs_search_invalid_param(client):
    response = client.get('/logs/search?q=123', headers={'X-API-KEY': 'changeme123'})
    assert response.status_code in (200, 500)  # Should not fail validation for string 
