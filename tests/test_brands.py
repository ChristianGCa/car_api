from fastapi import status


def test_create_brand(client, auth_headers):
    response = client.post(
        '/api/v1/brands/',
        json={'name': 'Honda', 'description': 'Honda cars', 'is_active': True},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == 'Honda'


def test_create_brand_duplicate(client, brand, auth_headers):
    response = client.post(
        '/api/v1/brands/',
        json={'name': brand.name, 'description': 'Duplicate'},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_brands(client, brand, auth_headers):
    response = client.get('/api/v1/brands/', headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data['brands']) > 0


def test_get_brand(client, brand, auth_headers):
    response = client.get(f'/api/v1/brands/{brand.id}', headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == brand.name


def test_update_brand(client, brand, auth_headers):
    response = client.put(
        f'/api/v1/brands/{brand.id}',
        json={'name': 'Toyota Updated'},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Toyota Updated'


def test_delete_brand(client, brand, auth_headers):
    response = client.delete(
        f'/api/v1/brands/{brand.id}', headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(f'/api/v1/brands/{brand.id}', headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
