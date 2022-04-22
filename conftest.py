import pytest
from users.models import Address


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