from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import CreateBookingForm, UpdateBookingForm, DriverUpdateStatusForm
from .models import Booking
from owners.models import Owner
from drivers.models import Driver
from mycabs.decorators import owner_required, driver_required
import logging
import json

logger = logging.getLogger(__name__)


@owner_required
def booking_list(request):
    """Display the list of bookings for the logged-in owner."""
    status_class_map = {
        'Pending': 'text-warning',
        'Confirmed': 'text-primary',
        'Completed': 'text-success',
        'Cancelled': 'text-danger',
    }
    owner = get_object_or_404(Owner, user=request.user)
    # Order bookings by updated_at field in descending order
    bookings = owner.bookings_as_owner.all().order_by('-updated_at')

    return render(request, 'bookings/booking_list.html', {'bookings': bookings, 'status_class_map': status_class_map})


def create_booking(request):
    owner = get_object_or_404(Owner, user=request.user)

    if request.method == 'POST':
        form = CreateBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = owner

            if form.cleaned_data['journey_type'] == 'Multiple Locations':
                multi_locations = form.cleaned_data.get('multi_locations')
                if multi_locations:
                    booking.multi_locations = json.loads(multi_locations)
                    booking.pickup_location = booking.drop_location = None
                else:
                    form.add_error(None, "Multiple locations are required for this journey type.")
                    return render(request, 'bookings/create_booking.html', {'form': form})
            else:
                booking.multi_locations = None

            booking.save()
            messages.success(request, 'Booking created successfully.')
            return redirect('booking_list')

        messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CreateBookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form})


def update_booking(request, booking_id):
    owner = get_object_or_404(Owner, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, owner=owner)

    if request.method == 'POST':
        form = UpdateBookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save(commit=False)
            journey_type = form.cleaned_data['journey_type']

            if journey_type == 'Multiple Locations':
                multi_locations = request.POST.get('multi_locations')
                if multi_locations:
                    try:
                        parsed_locations = json.loads(multi_locations)
                        if parsed_locations:
                            updated_booking.multi_locations = parsed_locations
                            updated_booking.pickup_location = updated_booking.drop_location = None
                        else:
                            form.add_error(None,
                                           "At least one location is required for multiple locations journey type.")
                            return render(request, 'bookings/update_booking.html', {'form': form, 'booking': booking})
                    except json.JSONDecodeError:
                        form.add_error(None, "Invalid multi-location data.")
                        return render(request, 'bookings/update_booking.html', {'form': form, 'booking': booking})
                else:
                    form.add_error(None, "Multiple locations are required for this journey type.")
                    return render(request, 'bookings/update_booking.html', {'form': form, 'booking': booking})
            else:
                updated_booking.multi_locations = None

            updated_booking.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('booking_list')

        messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UpdateBookingForm(instance=booking)

    multi_locations_json = json.dumps(booking.multi_locations or [])

    return render(request, 'bookings/update_booking.html', {
        'form': form,
        'booking': booking,
        'multi_locations_json': multi_locations_json
    })


@owner_required
def view_booking(request, booking_id):
    """View an existing booking for the logged-in owner."""
    owner = get_object_or_404(Owner, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, owner=owner)

    if request.method == 'POST':
        form = UpdateBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            logger.info(f"Booking {booking_id} updated successfully by user {request.user.id}")
            return redirect('booking_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
            logger.warning(f"Invalid form submission for booking {booking_id}: {form.errors}")
    else:
        form = UpdateBookingForm(instance=booking)

    multi_locations_json = json.dumps(booking.multi_locations or [])
    additional_charges_json = json.dumps(booking.additional_charges or {})
    return render(request, 'bookings/view_booking.html', {
        'form': form,
        'booking': booking,
        'multi_locations_json': multi_locations_json,
        'additional_charges': additional_charges_json
    })


@owner_required
def create_invoice(request, booking_id):
    pass


@driver_required
def driver_bookings(request):
    """Display the list of bookings for the logged-in driver."""
    driver = get_object_or_404(Driver, user=request.user)
    bookings = driver.bookings_as_driver.all()

    return render(request, 'bookings/driver_booking_list.html', {'bookings': bookings})


@driver_required
def driver_complete_booking(request, booking_id):
    """Update the status of a booking for the logged-in driver."""
    booking = get_object_or_404(Booking, id=booking_id)
    driver = get_object_or_404(Driver, user=request.user)

    if booking.driver != driver:
        messages.error(request, 'You are not authorized to edit this booking.')
        return redirect('driver_bookings')

    if request.method == 'POST':
        form = DriverUpdateStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking status updated successfully!')
            return redirect('driver_bookings')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = DriverUpdateStatusForm(instance=booking)

    return render(request, 'bookings/driver_complete_booking.html', {'form': form, 'booking': booking})
