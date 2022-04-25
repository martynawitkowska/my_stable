import pytest
from django.urls import reverse

from horses.models import Horse, Stable


def test_add_horse_view_user_not_logged_in(client):
    url = reverse('horses:add_horse')
    response = client.get(url, follow=True)
    assert response.status_code == 200


def test_add_horse_view_user_can_add_horse(user, client):
    url = reverse('horses:add_horse')
    client.force_login(user)
    response = client.post(url, data={
        'name': 'Kalahari',
        'mother': 'Korina',
        'father': 'Landos II',
        'birth_date': '2010-03-09',
        'age': 12,
        'stall': 2,
        'horse_owner': 'Mi Wi',
        'stable_owner': 1,
        'farrier': 1,
        'vet': 1,
    })
    assert response.status_code == 302
    assert len(Horse.objects.all()) == 1


@pytest.mark.django_db
def test_add_stable_view_user_can_add_stable(client, user):
    url = reverse('horses:add_stable')
    client.force_login(user)
    client.post(url, data={
        'name': 'Happy Horses',
        'description': 'Horses are happy here at our stable',
        'stalls_quantity': 12
    })

    assert len(Stable.objects.all()) == 1
