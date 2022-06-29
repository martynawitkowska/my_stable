import os

from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from durationwidget.widgets import TimeDurationWidget

from . import models


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class AddHorseForm(forms.ModelForm):
    User = get_user_model()

    class Meta:
        model = models.Horse
        fields = ('name', 'mother', 'father', 'birth_date', 'age', 'stall',
                  'horse_owner', 'picture', 'farrier', 'vet')
        widgets = {'birth_date': DatePickerInput}

    def __init__(self, *args, **kwargs):
        super(AddHorseForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False
        self.fields['vet'].queryset = self.User.objects.filter(groups__name=os.environ.get('DJ_GROUP_VETERINARIANS'))
        self.fields['farrier'].queryset = self.User.objects.filter(groups__name=os.environ.get('DJ_GROUP_FARRIERS'))


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
    widgets={'duration': TimeDurationWidget(show_days=False, show_seconds=False), 'hour': TimePickerInput},
    extra=7,
    can_delete_extra=True,
)
