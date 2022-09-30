import os
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def add_permissions(sender, **kwargs):
    """
    A function to automatically add permissions to groups that are created
    in users/migrations/0002_create_groups.py It is placed in horses/apps.py,
    because it runs after post migration signal, and all permissions are in database to get.
    """
    from django.contrib.auth.models import Group, Permission

    stable_owners = Group.objects.get(name=os.environ.get('DJ_GROUP_STB_OWNERS'))
    veterinarians = Group.objects.get(name=os.environ.get('DJ_GROUP_VETERINARIANS'))
    farriers = Group.objects.get(name=os.environ.get('DJ_GROUP_FARRIERS'))

    add_horse = Permission.objects.get(codename='add_horse')
    add_training = Permission.objects.get(codename='add_training')
    add_stable = Permission.objects.get(codename='add_stable')
    change_training = Permission.objects.get(codename='change_training')
    change_horse = Permission.objects.get(codename='change_horse')
    add_feeding = Permission.objects.get(codename='add_feeding')
    change_feeding = Permission.objects.get(codename='change_feeding')
    add_vaccinesdates = Permission.objects.get(codename='add_vaccinesdates')
    change_vaccinesdates = Permission.objects.get(codename='change_vaccinesdates')
    view_farrierappointment = Permission.objects.get(codename='view_farrierappointment')
    view_vetappointment = Permission.objects.get(codename='view_vetappointment')
    view_stable = Permission.objects.get(codename='view_stable')
    view_horse = Permission.objects.get(codename='view_horse')
    add_v_appointment = Permission.objects.get(codename='add_vetappointment')
    add_f_appointment = Permission.objects.get(codename='add_farrierappointment')

    stable_owner_permissions = [
        add_horse,
        change_horse,
        add_training,
        add_stable,
        change_training,
        add_feeding,
        change_feeding,
        add_vaccinesdates,
        change_vaccinesdates,
        view_vetappointment,
        view_farrierappointment,
    ]

    vet_permissions = [
        add_v_appointment,
        view_stable,
        view_horse,
    ]

    farrier_permissions = [
        add_f_appointment,
        view_stable,
        view_horse,
    ]

    stable_owners.permissions.set(stable_owner_permissions)
    veterinarians.permissions.set(vet_permissions)
    farriers.permissions.set(farrier_permissions)


class HorsesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'horses'

    def ready(self):
        post_migrate.connect(add_permissions, sender=self)
