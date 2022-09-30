from django.contrib.auth import get_user_model
from django.urls import reverse


def test_login_page(client):
    url = reverse('users:login')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Login</h1>' in response.content.decode('UTF-8')


def test_logging_in_status_code(client):
    url = reverse('users:login')
    response = client.post(url)
    assert response.status_code == 200


def test_logging_in_redirect_works(client):
    url = reverse('users:login')
    client.post(url)
    response = client.get(reverse('home:home'))
    assert '<h1>MY STABLE&trade;</h1>' in response.content.decode('UTF-8')


def test_user_can_register(client, user):
    url = reverse('users:register')
    client.post(url, data={
        'first_name': 'DeeDee',
        'last_name': 'Lockhart',
        'company_name': 'My Little Pony',
        'email': 'deedee@mylittlepony.com',
        'user_type': 3,
        'password': 'imsocrazy6',
        'password2': 'imsocrazy6',
        'street': 'Pink Munchkin Alley',
        'house_number': 3,
        'apartment_number': 1,
        'city': 'Rainbow City Kansas',
        'country': 'USA',
        'postal_code': '12345',
    })

    assert len(get_user_model().objects.all()) == 1


