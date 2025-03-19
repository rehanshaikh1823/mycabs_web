from mycabs.decorators import owner_required
from bookings.models import Booking
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .models import Invoice
from .forms import CreateInvoiceForm
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from weasyprint import HTML
import urllib.parse

@owner_required
def create_or_update_invoice(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)
        if request.user != booking.owner.user:
            raise PermissionDenied

        with transaction.atomic():
            invoice, created = Invoice.objects.get_or_create(
                booking=booking,
                defaults={
                    'invoice_number': f"INV-{booking.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                }
            )

        if request.method == 'POST':
            form = CreateInvoiceForm(request.POST, instance=invoice)
            if form.is_valid():
                invoice = form.save(commit=False)
                invoice.save()
                messages.success(request, 'Invoice created/updated successfully!')
                return generate_pdf_response(request, booking_id)
        else:
            form = CreateInvoiceForm(instance=invoice)

        context = {
            'form': form,
            'booking': booking,
            'owner': booking.owner,
            'driver': booking.driver,
            'cab': booking.cab,
            'invoice': invoice,
            'is_update': not created,
        }
        return render(request, 'invoices/create_invoice.html', context)
    except PermissionDenied:
        messages.error(request, "You don't have permission to create/update an invoice.")
        return redirect('home')


@owner_required
def download_invoice(request, booking_id):
    return generate_pdf_response(request, booking_id)


@owner_required
def send_invoice_whatsapp(request, booking_id):
    whatsapp_number = "918208879725"  # The fixed number you provided
    download_url = request.build_absolute_uri(reverse('download_invoice', args=[booking_id]))

    booking = get_object_or_404(Booking, id=booking_id)
    invoice = get_object_or_404(Invoice, booking=booking)

    message = f"Here's your invoice (#{invoice.invoice_number}) for booking {booking_id}. You can download it from this link: {download_url}"

    whatsapp_url = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={urllib.parse.quote(message)}"

    return redirect(whatsapp_url)


def generate_pdf_response(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    invoice = get_object_or_404(Invoice, booking=booking)
    context = {
        'booking': booking,
        'owner': booking.owner,
        'driver': booking.driver,
        'cab': booking.cab,
        'invoice': invoice,
    }
    html_string = render_to_string('invoices/invoice_pdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{invoice.invoice_number}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    response.write(result)
    return response

# def generate_pdf_response(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     invoice = get_object_or_404(Invoice, booking=booking)
#
#     context = {
#         'booking': booking,
#         'owner': booking.owner,
#         'driver': booking.driver,
#         'cab': booking.cab,
#         'invoice': invoice,
#     }
#
#     html_string = render_to_string('invoices/invoice_pdf.html', context)
#     html = HTML(string=html_string)
#     result = html.write_pdf()
#
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=invoice_{invoice.invoice_number}.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#     response.write(result)
#
#     return response
