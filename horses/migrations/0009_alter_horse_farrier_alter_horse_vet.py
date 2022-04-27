# Generated by Django 4.0.3 on 2022-04-25 14:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('horses', '0008_alter_feeding_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horse',
            name='farrier',
            field=models.ManyToManyField(blank=True, related_name='f_horses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='horse',
            name='vet',
            field=models.ManyToManyField(blank=True, related_name='v_horses', to=settings.AUTH_USER_MODEL),
        ),
    ]