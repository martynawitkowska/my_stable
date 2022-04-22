from django import forms

from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class AddHorseForm(forms.ModelForm):

    class Meta:
        model = models.Horse
        fields = ('name', 'mother', 'father', 'birth_date', 'age', 'stall',
                  'horse_owner', 'picture', 'farrier', 'vet')
        widgets = {'birth_date': DateInput()}


class AddStableForm(forms.ModelForm):

    class Meta:
        model = models.Stable
        fields = ('name', 'description', 'stalls_quantity')
