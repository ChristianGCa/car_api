from fastapi import status


def test_create_user(client):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@example.com'
    assert 'id' in data


def test_create_user_existing_username(client, user, user_data):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': user.username,
            'email': 'other@example.com',
            'password': 'password123',
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_existing_email(client, user, user_data):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': 'otheruser',
            'email': user.email,
            'password': 'password123',
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_users(client, user):
    response = client.get('/api/v1/users/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data['users']) > 0
    assert data['users'][0]['username'] == user.username


def test_get_user(client, user):
    response = client.get(f'/api/v1/users/{user.id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['username'] == user.username


def test_update_user(client, user, auth_headers):
    response = client.put(
        f'/api/v1/users/{user.id}',
        json={'username': 'updateduser'},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['username'] == 'updateduser'


def test_delete_user(client, user, auth_headers):
    response = client.delete(f'/api/v1/users/{user.id}', headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(f'/api/v1/users/{user.id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
