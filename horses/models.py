from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from . import enums


class Horse(models.Model):
    name = models.CharField(max_length=64)
    mother = models.CharField(max_length=64)
    father = models.CharField(max_length=64)
    birth_date = models.DateField()
    age = models.SmallIntegerField()
    stall = models.IntegerField()
    stable_owner = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.PROTECT)
    horse_owner = models.CharField(max_length=125, null=True)
    picture = models.ImageField(upload_to='images', default='images/my_stb_def.jpg', null=True)
    farrier = models.ManyToManyField(get_user_model(), related_name='f_horses', null=True)
    vet = models.ManyToManyField(get_user_model(), related_name='v_horses', null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + self.mother + self.father + str(self.birth_date))
        super().save(*args, **kwargs)


class Stable(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(get_user_model(), null=True, related_name='%(class)s_related', on_delete=models.PROTECT)
    description = models.TextField()
    stalls_quantity = models.IntegerField()
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + self.description[0:10])
        super().save(*args, **kwargs)


class Training(models.Model):
    weekday = models.SmallIntegerField(choices=enums.WeekDays.CHOICES, default=0)
    horse = models.ManyToManyField('Horse', related_name='Trainings')
    horse_bit = models.ManyToManyField('BitsToUse', related_name='Trainings')
    description = models.TextField()
    trainer = models.CharField(max_length=64)
    duration = models.DurationField()
    hour = models.TimeField()

    def __str__(self):
        return self.weekday


class BitsToUse(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()


class Feeding(models.Model):
    horse = models.ForeignKey('Horse', on_delete=models.PROTECT, related_name='feeding_plans')
    meal = models.SmallIntegerField(choices=enums.Meals.CHOICES, default=0)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class VetAppointment(models.Model):
    vet = models.ForeignKey(get_user_model(), related_name='%(class)s_related', on_delete=models.PROTECT)
    horse = models.ForeignKey('Horse', related_name='%(class)s_related', on_delete=models.PROTECT)
    day = models.DateTimeField()


class FarrierAppointment(models.Model):
    farrier = models.ForeignKey(get_user_model(), related_name='%(class)s_related', on_delete=models.PROTECT)
    horse = models.ForeignKey('Horse', related_name='%(class)s_related', on_delete=models.PROTECT)
    day = models.DateTimeField()


class Vaccines(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()


class VaccinesDates(models.Model):
    shot = models.ManyToManyField('Vaccines', related_name='vaccines')
    horse = models.ManyToManyField('Horse', related_name='horses')
    date = models.DateField()
