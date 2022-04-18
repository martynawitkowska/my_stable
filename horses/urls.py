from django.urls import path

from . import views

app_name = 'horses'

urlpatterns = [
    path('add-horse', views.add_horse_view, name='add_horse'),
]