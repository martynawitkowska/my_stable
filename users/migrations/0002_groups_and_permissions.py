# Generated by Django 4.0.3 on 2022-04-21 08:20

import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_groups(apps, schema_editor):
    Account = get_user_model()
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    stable_owners = Group(name=os.environ.get('DJ_GROUP_STB_OWNERS'))
    stable_owners.save()

    veterinarians = Group(name=os.environ.get('DJ_GROUP_VETERINARIANS'))
    veterinarians.save()

    farriers = Group(name=os.environ.get('DJ_GROUP_FARRIERS'))
    farriers.save()

    add_horse = Permission.objects.get(codename='add_horse')
    add_training = Permission.objects.get(codename='add_training')
    change_training = Permission.objects.get(codename='change_training')
    change_horse = Permission.objects.get(codename='change_horse')
    add_feeding = Permission.objects.get(codename='add_feeding')
    change_feeding = Permission.objects.get(codename='change_feeding')
    view_farrierappointment = Permission.objects.get(codename='view_farrierappointment')
    view_vetappointment = Permission.objects.get(codename='view_vetappointment')
    view_horse = Permission.objects.get(codename='view_horse')
    add_v_appointment = Permission.objects.get(codename='add_vetappointment')
    add_f_appointment = Permission.objects.get(codename='add_farrierappointment')

    stable_owner_permissions = [
        add_horse,
        change_horse,
        add_training,
        change_training,
        add_feeding,
        change_feeding,
        view_vetappointment,
        view_farrierappointment,
    ]

    vet_permissions = [
        add_v_appointment,
        view_horse,
    ]

    farrier_permissions = [
        add_f_appointment,
        view_horse,
    ]

    stable_owners.permissions.set(stable_owner_permissions)
    veterinarians.permissions.set(vet_permissions)
    farriers.permissions.set(farrier_permissions)

    for user in Account.objects.all():
        if user.user_type == 3:
            stable_owners.user_set.add(user)
        elif user.user_type == 1:
            veterinarians.user_set.add(user)
        elif user.user_type == 2:
            farriers.user_set.add(user)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
