from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.views.generic import DetailView, CreateView

from . import forms, models, enums


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
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
    login_url = reverse_lazy('users:login')

    def get(self, request, user_id):
        if models.Stable.objects.filter(owner_id=user_id).exists():
            horses = models.Horse.objects.filter(stable_owner=user_id)
            stable = models.Stable.objects.get(owner=user_id)
            return render(request, 'horses/stable.html', context={'horses': horses, 'stable': stable})
        else:
            return redirect(reverse_lazy('horses:add_stable'))


class HorseDetailView(DetailView, LoginRequiredMixin):
    login_url = reverse_lazy('users:login')
    model = models.Horse
    context_object_name = 'horse'

    def get_context_data(self, **kwargs):
        context = super(HorseDetailView, self).get_context_data(**kwargs)
        context['meal1'] = models.Feeding.objects.all().filter(horse=self.object, meal=1).latest('date_created')
        context['meal2'] = models.Feeding.objects.all().filter(horse=self.object, meal=2).latest('date_created')
        context['meal3'] = models.Feeding.objects.all().filter(horse=self.object, meal=3).latest('date_created')
        context['meal_names'] = enums.Meals.CHOICES
        return context


class AddMealPlan(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('users:login')
    template_name = 'horses/add_meal.html'
    permission_required = 'horses.add_feeding'
    form_class = forms.AddFeedingForm
    context_object_name = 'horse'
    success_url = reverse_lazy('home:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # def get_success_url(self):
    #     return reverse_lazy('horses:horse_detail', kwargs={'horse': self.kwargs.get('slug')})
