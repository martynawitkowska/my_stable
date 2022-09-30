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
    farrier = models.ManyToManyField(get_user_model(), related_name='f_horses', blank=True)
    vet = models.ManyToManyField(get_user_model(), related_name='v_horses', blank=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
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
    horse = models.ForeignKey('HorseTraining', on_delete=models.PROTECT, null=True, blank=True)
    weekday = models.SmallIntegerField(choices=enums.WeekDays.CHOICES, default=0)
    horse_bit = models.ForeignKey('BitsToUse', on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(blank=True)
    trainer = models.CharField(max_length=64, default='Add trainer name')
    # TODO: typo in word rider
    raider = models.CharField(max_length=64, default='Add raider name')
    duration = models.DurationField(null=True)
    hour = models.TimeField(blank=True, null=True)


class HorseTraining(models.Model):
    horse = models.ForeignKey('Horse', on_delete=models.PROTECT, null=True, blank=True)
    training_name = models.CharField(max_length=100, null=True)


class BitsToUse(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()


class Feeding(models.Model):
    horse = models.ForeignKey('Horse', on_delete=models.PROTECT, related_name='feeding_plans')
    breakfast = models.TextField(null=True)
    dinner = models.TextField(null=True)
    supper = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.horse} feeding plan created {self.date_created}'


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

    def __str__(self):
        return self.name


class VaccinesDates(models.Model):
    # TODO: change many to many to a foreign key on shot and horse
    shot = models.ManyToManyField('Vaccines', related_name='vaccines')
    horse = models.ManyToManyField('Horse', related_name='horses')
    date = models.DateField()
