from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import login_success
from .views import custom_permission_denied_view
from cabs.views import toggle_cab_availability
urlpatterns = [
    path('', login_success, name='login_success'),
    path('admin/', admin.site.urls, name='django_admin'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout URL
    path('users/', include('users.urls')),
    path('owners/', include('owners.urls')),
    path('drivers/', include('drivers.urls')),
    path('cabs/', include('cabs.urls')),
    path('bookings/', include('bookings.urls')),
    path('invoices/', include('invoices.urls')),


]

handler403 = custom_permission_denied_view
