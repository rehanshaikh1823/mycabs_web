from django.urls import path
from . import views

urlpatterns = [
    path('<int:booking_id>/create-or-update-invoice/', views.create_or_update_invoice, name='create_or_update_invoice'),
    path('booking/<int:booking_id>/download-invoice/', views.download_invoice, name='download_invoice'),
    path('booking/<int:booking_id>/send-invoice-whatsapp/', views.send_invoice_whatsapp, name='send_invoice_whatsapp'),
]
