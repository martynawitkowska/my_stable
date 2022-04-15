from django.db import models

from . import enums


class Horse(models.Model):
    name = models.CharField(max_length=64)
    mother = models.CharField(max_length=64)
    father = models.CharField(max_length=64)
    birth_date = models.DateField()
    age = models.SmallIntegerField()
    stall = models.IntegerField()
    owner = models.CharField(max_length=64)
    picture = models.ImageField()


class Training(models.Model):
    weekday = models.SmallIntegerField(choices=enums.WeekDays.CHOICES, default=0)
    horse = models.ManyToManyField('Horse', on_delete=models.PROTECT, related_name='Trainings')
    horse_bit = models.ManyToManyField('HorseBits', on_delete=models.PROTECT, related_name='Trainings')
    description = models.TextField()
    trainer = models.CharField(max_length=64)
    duration = models.DurationField()
    hour = models.TimeField()

