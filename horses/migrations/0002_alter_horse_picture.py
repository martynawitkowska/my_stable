# Generated by Django 4.0.3 on 2022-04-18 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horse',
            name='picture',
            field=models.ImageField(upload_to='images'),
        ),
    ]