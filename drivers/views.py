from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import Driver
from owners.models import Owner
from .forms import DriverDetailsUpdateForm, DriverUpdateForm
from django.contrib import messages
from mycabs.decorators import driver_required
from mycabs.decorators import owner_required
from cabs.models import Cab
import logging

logger = logging.getLogger(__name__)


@owner_required
def list_drivers(request):
    owner = get_object_or_404(Owner, user=request.user)

    drivers = Driver.objects.filter(owner=owner).select_related('user', 'assigned_cab')
    available_cabs = Cab.objects.filter(owner=owner, driver__isnull=True)

    return render(request, 'drivers/list_drivers.html', {
        'drivers': drivers,
        'available_cabs': available_cabs
    })

@owner_required
@require_POST
def assign_cab_to_driver(request):
    driver_id = request.POST.get('driver_id')
    cab_id = request.POST.get('cab_id')

    if not driver_id:
        return JsonResponse({'status': 'error', 'message': 'Missing driver_id'}, status=400)

    driver = get_object_or_404(Driver, id=driver_id, owner__user=request.user)

    # Safely get assigned cab or None
    assigned_cab = getattr(driver, 'assigned_cab', None)

    # Unassign the current cab if any
    if assigned_cab:
        assigned_cab.driver = None
        assigned_cab.save()

    if cab_id:  # Assign new cab
        try:
            cab = Cab.objects.get(id=cab_id, owner__user=request.user)
            cab.driver = driver
            cab.save()
            driver.assigned_cab = cab
            driver.save()
            message = f"Successfully assigned cab {cab.vehicle_number} to driver {driver.user.get_full_name()}"
        except Cab.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cab not found or does not belong to you'}, status=404)
    else:  # Set cab free
        driver.assigned_cab = None
        driver.save()
        message = f"Successfully unassigned cab from driver {driver.user.get_full_name()}"

    available_cabs = Cab.objects.filter(owner__user=request.user, driver__isnull=True)
    cab_options = [{"id": cab.id, "vehicle_number": cab.vehicle_number} for cab in available_cabs]

    return JsonResponse({
        'status': 'success',
        'message': message,
        'available_cabs': cab_options
    })


@owner_required
@require_POST
def toggle_driver_status(request):
    driver_id = request.POST.get('driver_id')
    is_active = request.POST.get('is_active') == 'true'

    try:
        driver = get_object_or_404(Driver, id=driver_id, owner__user=request.user)
        driver.user.is_active = is_active  # Update is_active on the User model
        driver.user.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error updating driver status: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@driver_required
def update_driver_profile(request):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, 'Driver profile does not exist.')
        return redirect('driver_dashboard')

    if request.method == 'POST':
        user_form = DriverDetailsUpdateForm(request.POST, instance=request.user)
        driver_form = DriverUpdateForm(request.POST, instance=driver)
        if user_form.is_valid() and driver_form.is_valid():
            user_form.save()
            driver_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('update_driver_profile')
    else:
        user_form = DriverDetailsUpdateForm(instance=request.user)
        driver_form = DriverUpdateForm(instance=driver)

    context = {
        'user_form': user_form,
        'driver_form': driver_form
    }
    return render(request, 'drivers/update_profile.html', context)


@driver_required
def driver_dashboard(request):
    return render(request, 'drivers/dashboard.html')
