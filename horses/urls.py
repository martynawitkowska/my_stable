from django.urls import path

from . import views

app_name = 'horses'

urlpatterns = [
    path('add-horse', views.add_horse_view, name='add_horse'),
    path('add-stable', views.add_stable_view, name='add_stable'),
    path('stable/<int:user_id>', views.StableView.as_view(), name='stable')
]