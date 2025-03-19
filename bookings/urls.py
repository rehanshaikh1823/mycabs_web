from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('list-bookings/', views.booking_list, name='booking_list'),
    path('create/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/update/', views.update_booking, name='update_booking'),
    path('<int:booking_id>/view/', views.view_booking, name='view_booking'),
    path('<int:booking_id>/create-invoice/', views.create_invoice, name='create_invoice'),

    # driver bookings
    path('driver-bookings/', views.driver_bookings, name='driver_bookings'),
    path('<int:booking_id>/complete/', views.driver_complete_booking, name='driver_complete_booking'),

]
