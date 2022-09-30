from users.models import Address


def test_create_user_and_address(user, django_user_model):
    users = django_user_model.objects.all()
    address = Address.objects.all()
    assert len(users) == 1
    assert len(address) == 1
