from django import forms

from . import models


class AddHorseForm(forms.ModelForm):
    class Meta:
        model = models.Horse
        fields = ('name', 'mother', 'father',
                  'birth_date', 'age', 'stall',
                  'owner', 'picture', 'farrier', 'vet')