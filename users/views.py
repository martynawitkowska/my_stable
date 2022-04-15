from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect, get_object_or_404
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
            if form1.cleaned_data['Stable owner'] == 'Stable owner':
                permission = Permission.objects.get(name='Can add horses')
                stable_owners_group = Group.objects.get(name='stable owners')
                user.groups.add(stable_owners_group)
                user.user_permissions.add(permission)
            elif form1.cleaned_data['Vet'] == 'Vet':
                permission = Permission.objects.get(name='Can add an appointments')
                veterinarians_group = Group.objects.get('veterinarians')
                user.groups.add(veterinarians_group)
                user.user_permissions.add(permission)
            elif form1.cleaned_data['Farrier'] == 'Farrier':
                permission = Permission.objects.get(name='Can add appointments')
                farriers_group = Group.objects.get('farriers')
                user.groups.add(farriers_group)
                user.user_permissions.add(permission)
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/registration.html', {'form1': form1, 'form2': form2})
