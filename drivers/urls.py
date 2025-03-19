
from django.urls import path
from . import views

urlpatterns = [
    # owner login required
    path('', views.list_drivers, name='list_drivers'),
    path('list-drivers/', views.list_drivers, name='list_drivers'),
    path('toggle-driver-status/', views.toggle_driver_status, name='toggle_driver_status'),
    path('assign-cab/', views.assign_cab_to_driver, name='assign_cab_to_driver'),

    # driver login required
    path('dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('update-driver-profile/', views.update_driver_profile, name='update_driver_profile'),

]
