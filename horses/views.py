from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View

from . import forms, models


@login_required
@permission_required('horses.add_horse', login_url='users:login')
def add_horse_view(request):
    form = forms.AddHorseForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            horse = form.save(commit=False)
            horse.stable_owner = request.user
            horse.save()
            return redirect(reverse_lazy('home:home'))
    else:
        form = forms.AddHorseForm()
    return render(request, 'horses/add_horse.html', {'form': form})


@login_required
@permission_required('horses.add_stable', raise_exception=True)
def add_stable_view(request):
    form = forms.AddStableForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            stable = form.save(commit=False)
            stable.owner = request.user
            stable.save()
            return redirect(reverse_lazy('home:home'))
    else:
        form = forms.AddStableForm()
    return render(request, 'horses/add_stable.html', {'form': form})


class StableView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        horses = models.Horse.objects.filter(stable_owner=user_id)
        stable = models.Stable.objects.get(owner=user_id)

        return render(request, 'horses/stable.html', context={'horses': horses, 'stable': stable})


