from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create-driver/', views.create_driver, name='create_driver'),
]
