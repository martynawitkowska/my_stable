from django import forms
from django.forms import inlineformset_factory

from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class AddHorseForm(forms.ModelForm):

    class Meta:
        model = models.Horse
        fields = ('name', 'mother', 'father', 'birth_date', 'age', 'stall',
                  'horse_owner', 'picture', 'farrier', 'vet')
        widgets = {'birth_date': DateInput()}

    def __init__(self, *args, **kwargs):
        super(AddHorseForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False


class AddStableForm(forms.ModelForm):

    class Meta:
        model = models.Stable
        fields = ('name', 'description', 'stalls_quantity')


class AddFeedingForm(forms.ModelForm):

    class Meta:
        model = models.Feeding
        fields = ['breakfast', 'dinner', 'supper', 'horse']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['horse'].queryset = models.Horse.objects.filter(stable_owner=user)


class TrainingForm(forms.ModelForm):

    class Meta:
        model = models.HorseTraining
        exclude = ('name', )


TrainingFormSet = inlineformset_factory(
    models.HorseTraining,
    models.Training,
    fields=('horse', 'weekday', 'description', 'trainer', 'raider', 'duration', 'hour'),
    extra=2,
    max_num=7,
    absolute_max=7,
    can_delete=True,
)
