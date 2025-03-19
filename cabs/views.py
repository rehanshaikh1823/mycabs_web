from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import CabForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CabLocationForm
from .models import Cab
from owners.models import Owner
from drivers.models import Driver
from mycabs.decorators import owner_required, driver_required
from django.views.decorators.csrf import csrf_exempt

import logging
import json

logger = logging.getLogger(__name__)


@owner_required
def add_cabs(request):
    try:
        owner = Owner.objects.get(user=request.user)
    except Owner.DoesNotExist:
        messages.error(request, "Owner profile does not exist.")
        logger.error(f"Owner profile does not exist for user: {request.user}")
        return redirect('some_error_page')  # Define an appropriate error page

    if request.method == 'POST':
        form = CabForm(request.POST)
        if form.is_valid():
            cab = form.save(commit=False)
            cab.owner = owner
            cab.save()
            messages.success(request, 'Cab added successfully.')
            logger.info(f"Cab {cab.vehicle_number} added for owner: {owner.business_name}")
            return redirect('list_cabs')
        else:
            messages.error(request, 'Please correct the errors below.')
            logger.error("CabForm is not valid")
    else:
        form = CabForm()

    return render(request, 'cabs/add_cab.html', {'form': form})


@owner_required
def update_cab(request, cab_id):
    owner = get_object_or_404(Owner, user=request.user)
    cab = get_object_or_404(Cab, id=cab_id, owner=owner)

    if request.method == 'POST':
        form = CabForm(request.POST, instance=cab)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cab updated successfully.')
            logger.info(f"Cab {cab.vehicle_number} updated for owner: {owner.business_name}")
            return redirect('list_cabs')
        else:
            messages.error(request, 'Please correct the errors below.')
            logger.error("CabForm is not valid")
    else:
        form = CabForm(instance=cab)

    return render(request, 'cabs/update_cab.html', {'form': form})


@owner_required
def list_cabs(request):
    owner = get_object_or_404(Owner, user=request.user)
    cabs = Cab.objects.filter(owner=owner)
    return render(request, 'cabs/list_cabs.html', {'cabs': cabs})


@owner_required
@require_POST
def toggle_cab_status(request):
    cab_id = request.POST.get('cab_id')
    is_active = request.POST.get('is_active') == 'true'

    try:
        cab = get_object_or_404(Cab, id=cab_id, owner__user=request.user)
        cab.is_active = is_active
        cab.save()
        logger.info(f"Cab {cab.vehicle_number} status updated to {'active' if is_active else 'inactive'}")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error updating cab status: {str(e)}")
        return JsonResponse({'status': 'error'}, status=400)


@owner_required
def cabs_location(request):
    owner = get_object_or_404(Owner, user=request.user)
    cabs = Cab.objects.filter(owner=owner, is_active=True).select_related('driver', 'driver__user')

    if request.method == 'POST':
        cab_id = request.POST.get('cab_id')
        cab = get_object_or_404(Cab, id=cab_id, owner=owner)
        form = CabLocationForm(request.POST, instance=cab)
        if form.is_valid():
            cab = form.save(commit=False)
            cab.current_location = form.cleaned_data['current_location']
            cab.save()
            return JsonResponse({
                'status': 'success',
                'current_location': cab.current_location,
                'latitude': cab.latitude,
                'longitude': cab.longitude,
                'vehicle_number': cab.vehicle_number
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = CabLocationForm()

    return render(request, 'cabs/cabs_location.html', {'cabs': cabs, 'form': form})


@owner_required
@require_POST
@csrf_exempt
def toggle_cab_availability(request, cab_id):
    cab = get_object_or_404(Cab, id=cab_id, owner__user=request.user)
    data = json.loads(request.body)
    cab.is_available = data.get('is_available', not cab.is_available)
    cab.save()
    return JsonResponse({'status': 'success', 'is_available': cab.is_available})


from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from mycabs.serializers import LoginSerializer, LocationUpdateSerializer
from rest_framework import exceptions

User = get_user_model()


@api_view(['POST'])
@csrf_exempt
def driver_login(request):
    logger.info('Login attempt started')
    logger.debug(f'Request data: {request.data}')

    serializer = LoginSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except exceptions.ValidationError as e:
        logger.error(f'Validation error: {e}')
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']
    if user.is_driver:
        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f'Successful login for user: {user.username}')
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        logger.warning(f'Login attempt by non-driver user: {user.username}')
        return Response({'error': 'User is not a driver'}, status=status.HTTP_403_FORBIDDEN)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @driver_required
# def update_location(request):
#     logger.warning(f'within update location')
#     serializer = LocationUpdateSerializer(data=request.data)
#     try:
#         serializer.is_valid(raise_exception=True)
#     except exceptions.ValidationError as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#     driver = get_object_or_404(Driver, user=request.user)
#     cab = driver.assigned_cab
#     if cab:
#         cab.latitude = serializer.validated_data['latitude']
#         cab.longitude = serializer.validated_data['longitude']
#         cab.current_location = serializer.validated_data.get('address', f"{cab.latitude:.4f}, {cab.longitude:.4f}")
#         cab.save()
#         return Response({'status': 'Location updated successfully'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'No cab assigned'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@driver_required
def update_location(request):
    logger.info(f'Update location attempt by user: {request.user.username}')

    serializer = LocationUpdateSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        logger.debug(f'Validated location data: {serializer.validated_data}')
    except exceptions.ValidationError as e:
        logger.error(f'Validation error for user {request.user.username}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    driver = get_object_or_404(Driver, user=request.user)
    logger.info(f'Found driver record for user: {request.user.username}')

    cab = driver.assigned_cab
    if cab:
        cab.latitude = serializer.validated_data['latitude']
        cab.longitude = serializer.validated_data['longitude']
        cab.current_location = serializer.validated_data.get('address', f"{cab.latitude:.4f}, {cab.longitude:.4f}")
        cab.save()
        logger.info(f'Updated location for cab {cab.id} assigned to driver {driver.id}')
        return Response({'status': 'Location updated successfully'}, status=status.HTTP_200_OK)
    else:
        logger.warning(f'No cab assigned to driver {driver.id}')
        return Response({'error': 'No cab assigned'}, status=status.HTTP_400_BAD_REQUEST)
