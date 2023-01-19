from src.main import tc

client = tc
bearerToken = 'Bearer token-jabar-juara'

def test_public_route():
    response = client.get('/')
    assert response.status_code == 200

def test_private_route_without_token():
    response = client.get('/protected')
    assert response.status_code == 401

def test_private_route_with_token():
    response = client.get('/protected', headers={"Authorization": bearerToken})
    assert response.status_code == 200