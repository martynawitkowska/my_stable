from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View


from . import forms, models


@login_required
@permission_required('add_horse', raise_exception=True)
def add_horse_view(request):
    form = forms.AddHorseForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home:home'))
    else:
        form = forms.AddHorseForm()
    return render(request, 'horses/add_horse.html', {'form': form})


@login_required
@permission_required('stable.add_stable', raise_exception=True)
def add_stable_view(request):
    form = forms.AddStableForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home:home'))
    else:
        form = forms.AddStableForm()
    return render(request, 'horses/add_stable.html', {'form': form})


class StableView(LoginRequiredMixin, View):
    def get(self, request, owner_id):
        horses = models.Stable.objects.select_related('horse')
        stable = models.Stable.objects.filter(owner_id=owner_id)

        return render(request, 'horses/stable.html', context={'horses': horses, 'stable': stable})


