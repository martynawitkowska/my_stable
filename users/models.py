from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.db import models

from address.models import AddressField

from . import enums


class CustomAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, company_name, email, address, password=None):
        if not email:
            raise ValueError('You must provide an email')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            address=address
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        if user.user_type == 1:
            vet_group = Group.objects.get(name='veterinarians')
            user.groups.add(vet_group)


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    company_name = models.CharField(max_length=120, verbose_name='company name')
    email = models.EmailField(max_length=70, unique=True, verbose_name='email')
    address = AddressField()
    user_type = models.SmallIntegerField(choices=enums.UserType, default=0)
    date_join = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'company name'

    objects = CustomAccountManager()

    def __str__(self):
        return self.company_name
