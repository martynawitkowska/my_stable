import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from horses.models import Stable
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
            user.address = Address.objects.latest('id')
            user.is_active = True
            user.save()
            if form1.cleaned_data['user_type'] == 3:
                stable_owners_group = Group.objects.get(name=os.environ.get('DJ_GROUP_STB_OWNERS'))
                user.groups.add(stable_owners_group)
                permissions = stable_owners_group.permissions.all()
                user.user_permissions.set(permissions)
            elif form1.cleaned_data['user_type'] == 1:
                veterinarians_group = Group.objects.get(name=os.environ.get('DJ_GROUP_VETERINARIANS'))
                user.groups.add(veterinarians_group)
                permissions = veterinarians_group.permissions.all()
                user.user_permissions.set(permissions)
            elif form1.cleaned_data['user_type'] == 2:
                farriers_group = Group.objects.get(name=os.environ.get('DJ_GROUP_FARRIERS'))
                user.groups.add(farriers_group)
                permissions = farriers_group.permissions.all()
                user.user_permissions.set(permissions)
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/registration.html', {'form1': form1, 'form2': form2})
