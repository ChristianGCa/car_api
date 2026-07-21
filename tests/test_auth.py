from fastapi import status


def test_login_success(client, user, user_data):
    response = client.post(
        '/api/v1/auth/token',
        json={'email': user.email, 'password': user_data['password']},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_login_invalid_password(client, user, user_data):
    response = client.post(
        '/api/v1/auth/token',
        json={'email': user.email, 'password': 'wrongpassword'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client, auth_headers):
    response = client.post('/api/v1/auth/refresh', headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'access_token' in data
