from django.urls import path

from . import views

app_name = 'horses'

urlpatterns = [
    path('add-horse', views.add_horse_view, name='add_horse'),
    path('edit-horse/<slug:slug>', views.UpdateHorseView.as_view(), name='change_horse'),
    path('add-stable', views.add_stable_view, name='add_stable'),
    path('stable/<int:user_id>', views.StableView.as_view(), name='stable'),
    path('add-meal', views.AddMealPlan.as_view(), name='add_meal'),
    path('edit-meal/<int:pk>', views.UpdateMealView.as_view(), name='change_meal'),
    path('add-training', views.AddTrainingView.as_view(), name='add_training'),
    path('edit-training/<int:pk>', views.UpdateTrainingView.as_view(), name='change_training'),
    path('<slug:slug>', views.HorseDetailView.as_view(), name='horse_detail'),
]