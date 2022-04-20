import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import forms
from .models import Address


def login_user_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(email=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # TODO change redirect to corresponding user profile
                    return redirect(reverse_lazy('home:home'))
    else:
        form = forms.LoginForm()

        return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))


def registration_view(request):
    form2 = forms.AddressForm(request.POST or None, request.FILES or None)
    form1 = forms.RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid():
            form2.save()
            user = form1.save(commit=False)
            address = Address.objects.latest('id')
            user.address = address
            user.is_active = True
            user.save()
            # if form1.cleaned_data['Stable owner'] == 'stable owner':
            #     stable_owners_group = Group.objects.get(name=os.environ.get('DJ_GROUP_STB_OWNERS'))
            #     user.groups.add(stable_owners_group)
            # elif form1.cleaned_data['Vet'] == 'Vet':
            #     veterinarians_group = Group.objects.get(name=os.environ.get('DJ_GROUP_VETERINARIANS'))
            #     user.groups.add(veterinarians_group)
            # elif form1.cleaned_data['Farrier'] == 'Farrier':
            #     farriers_group = Group.objects.get(name=os.environ.get('DJ_GROUP_FARRIERS'))
            #     user.groups.add(farriers_group)
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/registration.html', {'form1': form1, 'form2': form2})
