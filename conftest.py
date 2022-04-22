import pytest
from users.models import Address
from horses.models import Horse, Stable


@pytest.fixture(scope='function')
def user(db, django_user_model):
    """
    User instance from default user model and Address instance from 'users.models'
    that is necessary to create a User object.
    """
    address = Address.objects.create(
        street='Al. Wolności',
        house_number=25,
        apartment_number=23,
        city='Warsaw',
        country='Poland',
        postal_code='00-000',
    )
    user = django_user_model.objects.create_user(
        password='12345',
        first_name='Zdzisław',
        last_name='Iksiński',
        company_name='Happy Horses',
        email='office@happyhorses.pl',
        user_type=3,
        address=address,
    )
    yield user


@pytest.fixture(scope='function')
def horse(db):
    horse = Horse.objects.create(
        name='Hima',
        mother='Hestia',
        father='Davos',
        birth_date='2010-03-07',
        age=6,
        stall=3,
        horse_owner='Olga Makowska',
    )
    yield horse


@pytest.fixture(scope='function')
def stable(db):
    stable = Stable.objects.create(
        name='My Stable',
        description='Horses are happy here.',
        stalls_quantity=20,
    )
    yield stable