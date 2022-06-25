from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView

from . import forms, models, enums


@login_required(login_url='users:login')
@permission_required('horses.add_horse', login_url='users:login')
def add_horse_view(request):
    """
    Form to add a horse. User has to fill out all filed in order to add a horse.
    When submit button is clicked user is redirected to homepage, this is
    supposed to be changed in near future. User should be redirected to a just added
    horse detail view in order to add more details like training, feeding etc.
    """
    form = forms.AddHorseForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            horse = form.save(commit=False)
            horse.stable_owner = request.user
            horse.save()
            # TODO narrow choice for vet and farrier to users in assigned user group
            # TODO after adding a horse user should be redirected to a corresponding horse detail view
            return redirect(reverse_lazy('home:home'))
    else:
        form = forms.AddHorseForm()
    return render(request, 'horses/add_horse.html', {'form': form, 'form_name': 'Add horse', 'button_val': 'Add horse'})


class UpdateHorseView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Update view for changing horse data in database. Overridden get_success_url to redirect user to a dedicated detail
    view of horse + context data for shortening the amount of code.
    """
    login_url = reverse_lazy('users:login')
    permission_required = 'horses.change_horse'
    model = models.Horse
    form_class = forms.AddHorseForm
    template_name = 'horses/add_horse.html'

    def get_success_url(self):
        return reverse_lazy('horses:horse_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(UpdateHorseView, self).get_context_data(**kwargs)
        context['form_name'] = 'Edit horse'
        context['button_val'] = 'Save'
        return context


@login_required(login_url='users:login')
@permission_required('horses.add_stable', raise_exception=True)
def add_stable_view(request):
    """
     Form to add a stable. User has to fill out all fields in order to add a stable.
    After submitting the form user should be redirected to a stable view to start
    adding horses to the stable
    """
    form = forms.AddStableForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            stable = form.save(commit=False)
            stable.owner = request.user
            stable.save()
            # TODO after adding stable user should be redirected to a corresponding stable view
            return redirect(reverse_lazy('home:home'))
    else:
        form = forms.AddStableForm()
    return render(request, 'horses/add_stable.html', {'form': form})


class StableView(LoginRequiredMixin, View):
    """
    View of stable. Only LoginRequiredMixin is used to allow other users see the profile
    and see the details of horses. It is important to give access to other users groups.
    When user clicks in a field with a name of horse than it redirects to a corresponding
    horse detail view.
    """
    login_url = reverse_lazy('users:login')

    def get(self, request, user_id):
        if models.Stable.objects.filter(owner_id=user_id).exists():
            horses = models.Horse.objects.filter(stable_owner=user_id)
            stable = models.Stable.objects.get(owner=user_id)
            return render(request, 'horses/stable.html', context={'horses': horses, 'stable': stable})
        else:
            return redirect(reverse_lazy('horses:add_stable'))


class HorseDetailView(LoginRequiredMixin, DetailView):
    """
    This is a place where user can see details of horse. It is a work in progress page
    so queries are not perfect yet. Honestly it is a mess now.
    """
    login_url = reverse_lazy('users:login')
    model = models.Horse
    context_object_name = 'horse'

    def get_context_data(self, **kwargs):
        """
        Overridden get_context_data method to pass queries for view.
        """
        context = super(HorseDetailView, self).get_context_data(**kwargs)
        try:
            context['feeding'] = models.Feeding.objects.filter(horse=self.object).latest('date_created')
            horse_training = models.HorseTraining.objects.filter(horse=self.object).latest('id')
            context['horse_training'] = horse_training
            context['weekdays'] = enums.WeekDays.CHOICES
            context['trainings'] = models.Training.objects.filter(horse=horse_training)
        except models.Feeding.DoesNotExist or models.Training.objects.DoesNotExist:
            context['feeding'] = None
            context['trainings'] = None
        return context


class AddMealPlan(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    A form view for adding one meal. In select field user can only choose a horse
    that were added with a corresponding user ID.
    """
    login_url = reverse_lazy('users:login')
    template_name = 'horses/add_meal.html'
    permission_required = 'horses.add_feeding'
    context_object_name = 'horse'
    success_url = reverse_lazy('home:home')
    form_class = forms.AddFeedingForm

    def get_context_data(self, **kwargs):
        context = super(AddMealPlan, self).get_context_data(**kwargs)
        context['form_name'] = 'Add feeding plan'
        context['button_val'] = 'Submit'
        return context

    def get_form_kwargs(self):
        """
        Overridden get_form_kwargs method to pass request to form in order to
        provide queryset information.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class UpdateMealView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    login_url = reverse_lazy('users:login')
    permission_required = 'horses.change_feeding'
    model = models.Feeding
    fields = ['breakfast', 'dinner', 'supper']
    template_name = 'horses/add_meal.html'
    success_url = reverse_lazy('home:home')

    def get_context_data(self, **kwargs):
        context = super(UpdateMealView, self).get_context_data(**kwargs)
        context['form_name'] = 'Edit feeding plan'
        context['button_val'] = 'Save'
        return context


class AddTrainingView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.HorseTraining
    form_class = forms.TrainingForm
    object = None
    template_name = 'horses/add_training.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'horses.add_training'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.TrainingFormSet()
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.TrainingFormSet(self.request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            for form_day in formset:
                one_day = form_day.save(commit=False)
                one_day.horse = models.HorseTraining.objects.latest('id')
                one_day.save()
            return redirect(reverse_lazy('home:home'))
        else:
            return super().form_invalid(form, formset)


class UpdateTrainingView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    permission_required = 'horses.change_training'
    model = models.HorseTraining
    object = None
    form_class = forms.TrainingForm
    formset_class = forms.TrainingFormSet
    template_name = 'horses/add_training.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateTrainingView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = forms.TrainingFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = forms.TrainingFormSet(instance=self.object)
        print(context)
        return context

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     formset = forms.TrainingFormSet()
    #     print(self.get_context_data(form=form))
    #     for form in formset:
    #         print(form)
    #     return self.render_to_response(self.get_context_data(form=form, formset=formset))


# TODO: add update view for training
# TODO: add shots for horse
# TODO: assign farrier to horse
# TODO: assign vet to horse
