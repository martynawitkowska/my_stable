# Generated by Django 4.0.3 on 2022-04-20 12:47
import os

from django.db import migrations


def create_address(apps, schema_editor):
    Address = apps.get_model('users', 'Address')

    DJANGO_SU_STREET = os.environ.get('DJANGO_SU_STREET')
    DJANGO_SU_HOUSE_NUMBER = os.environ.get('DJANGO_SU_HOUSE_NUMBER')
    DJANGO_SU_APARTMENT_NUMBER = os.environ.get('DJANGO_SU_APARTMENT_NUMBER')
    DJANGO_SU_CITY = os.environ.get('DJANGO_SU_CITY')
    DJANGO_SU_COUNTRY = os.environ.get('DJANGO_SU_COUNTRY')
    DJANGO_SU_POSTAL_CODE = os.environ.get('DJANGO_SU_POSTAL_CODE')

    address = Address(
        1,
        DJANGO_SU_STREET,
        DJANGO_SU_HOUSE_NUMBER,
        DJANGO_SU_APARTMENT_NUMBER,
        DJANGO_SU_CITY,
        DJANGO_SU_COUNTRY,
        DJANGO_SU_POSTAL_CODE,
    )
    address.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_groups_and_permissions'),
    ]

    operations = [
        migrations.RunPython(create_address)
    ]
