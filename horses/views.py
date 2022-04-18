from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import forms


def add_horse_view(request):
    form = forms.AddHorseForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('home:home'))
    return render(request, 'horses/add_horse.html', {'form': form})
