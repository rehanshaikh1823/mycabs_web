from django.urls import path
from . import views

urlpatterns = [
    path('add-cab/', views.add_cabs, name='add_cab'),
    path('', views.list_cabs, name='list_cabs'),
    path('list-cabs/', views.list_cabs, name='list_cabs'),
    path('toggle-cab-status/', views.toggle_cab_status, name='toggle_cab_status'),
    path('update-cab/<int:cab_id>/', views.update_cab, name='update_cab'),
    path('cabs-location/', views.cabs_location, name='cabs_location'),
    path('toggle-cab-availability/<int:cab_id>/', views.toggle_cab_availability, name='toggle_cab_availability'),

    path('api/app_driver_login/', views.driver_login, name='app_driver_login'),
    path('api/app_update_location/', views.update_location, name='app_update_location'),

]
