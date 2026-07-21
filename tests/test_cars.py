from fastapi import status


def test_create_car(client, brand, user, auth_headers):
    response = client.post(
        '/api/v1/cars/',
        json={
            'model': 'Civic',
            'factory_year': 2022,
            'model_year': 2022,
            'color': 'Black',
            'plate': 'XYZ9876',
            'price': 120000.0,
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'description': 'Nice car',
            'is_available': True,
            'brand_id': brand.id,
            'owner_id': user.id,
        },
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['model'] == 'Civic'


def test_list_cars(client, car, auth_headers):
    response = client.get('/api/v1/cars/', headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data['cars']) > 0
    assert data['cars'][0]['model'] == car.model


def test_get_car(client, car, auth_headers):
    response = client.get(f'/api/v1/cars/{car.id}', headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['model'] == car.model


def test_update_car(client, car, auth_headers):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        json={'color': 'Red'},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['color'] == 'Red'


def test_delete_car(client, car, auth_headers):
    response = client.delete(f'/api/v1/cars/{car.id}', headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(f'/api/v1/cars/{car.id}', headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
