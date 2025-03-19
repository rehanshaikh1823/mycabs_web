from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('update-profile/', views.update_owner_profile, name='update_owner_profile'),
]
