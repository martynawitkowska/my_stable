import os

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin
from django.db import models
import pytz

from . import enums


class CustomAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, company_name, email, address, user_type, password=None):
        if not email:
            raise ValueError('You must provide an email')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            address=address,
            user_type=user_type,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        if user.user_type == 1:
            vet_group = Group.objects.get(name=os.environ.get('DJ_GROUP_VETERINARIANS'))
            user.groups.add(vet_group)
            return user
        elif user.user_type == 2:
            farrier_group = Group.objects.get(name=os.environ.get('DJ_GROUP_FARRIERS'))
            user.groups.add(farrier_group)
            return user
        elif user.user_type == 3:
            stable_owners_group = Group.objects.get(name=os.environ.get('DJ_GROUP_STB_OWNERS'))
            user.groups.add(stable_owners_group)
            return user
        else:
            raise ValueError('You must choose your occupation!')

    def create_superuser(self, first_name, last_name, company_name, email, address, user_type, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            email=self.normalize_email(email),
            address=address,
            user_type=user_type,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    company_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=70, unique=True, verbose_name='email')
    address = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='accounts')
    user_type = models.SmallIntegerField(choices=enums.UserType.CHOICES, blank=True, null=True, default=0)
    date_join = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()

    def __str__(self):
        return self.company_name


class Address(models.Model):
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()
    apartment_number = models.IntegerField()
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=20, choices=pytz.country_names.items())
    postal_code = models.CharField(max_length=6)

