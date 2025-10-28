import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add(client):
    response = client.get('/add?a=2&b=3')
    data = response.get_json()
    assert data['result'] == 5
