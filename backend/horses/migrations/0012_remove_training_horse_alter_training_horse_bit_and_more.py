# Generated by Django 4.0.3 on 2022-04-28 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0011_training_raider_alter_training_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='horse',
        ),
        migrations.AlterField(
            model_name='training',
            name='horse_bit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='horses.bitstouse'),
        ),
        migrations.CreateModel(
            name='HorseTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='horses.horse')),
                ('training', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='horses.training')),
            ],
        ),
    ]