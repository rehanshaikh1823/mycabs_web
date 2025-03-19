from django.contrib.auth.decorators import login_required
from .forms import OwnerSignUpForm
from .forms import DriverSignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from owners.models import Owner
from drivers.models import Driver
from mycabs.decorators import owner_required

import logging

logger = logging.getLogger(__name__)


def is_not_authenticated(user):
    return not user.is_authenticated


@user_passes_test(is_not_authenticated, login_url='login_success')
def signup(request):
    if request.method == 'POST':
        form = OwnerSignUpForm(request.POST)
        logger.debug(f"POST data: {request.POST}")
        if form.is_valid():
            logger.debug("Form is valid")
            try:
                user = form.save(commit=False)
                user.is_owner = True
                user.save()
                login(request, user)
                return redirect('owner_dashboard')
            except Exception as e:
                logger.error(f"Error saving user: {str(e)}")
    else:
        form = OwnerSignUpForm()
    return render(request, 'users/signup.html', {'form': form})


@owner_required
def create_driver(request):
    if request.method == 'POST':
        form = DriverSignUpForm(request.POST)
        logger.debug(f"POST data: {request.POST}")
        if form.is_valid():
            logger.debug("Form is valid")
            try:
                user = form.save(commit=False)
                user.is_driver = True
                user.save()
                create_driver_entry(user, request.user)

                return redirect('list_drivers')
            except Exception as e:
                logger.error(f"Error saving user: {str(e)}")
    else:
        form = DriverSignUpForm()
    return render(request, 'users/driver_signup.html', {'form': form})


def create_driver_entry(user, owner_user):
    try:
        owner = Owner.objects.get(user=owner_user)
        Driver.objects.create(
            user=user,
            owner=owner,
        )
    except Owner.DoesNotExist:
        raise ValueError("The logged-in user is not associated with an Owner instance.")


@user_passes_test(is_not_authenticated, login_url='login_success')
def custom_login(request):
    logger.info('Custom login view called')
    if request.method == 'POST':
        logger.info('POST request received')
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info(f'Received username: {username}')

        if not username or not password:
            logger.warning('Username or password not provided')
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.info(f'User {username} authenticated successfully')
            login(request, user)
            if user.is_owner:
                logger.info('Redirecting to owner_dashboard')
                return redirect('owner_dashboard')
            elif user.is_driver:
                logger.info('Redirecting to driver_dashboard')
                return redirect('driver_dashboard')
            else:
                logger.info('Redirecting to some_default_view')
                return redirect('admin:index')  # Define a default view for other users
        else:
            logger.warning(f'Authentication failed for user {username}')
            messages.error(request, 'Invalid username or password.')
    else:
        logger.info('GET request received')

    return render(request, 'login.html')


@login_required
def login_success(request):
    if request.user.is_driver:
        return redirect('driver_dashboard')
    elif request.user.is_owner:
        return redirect('owner_dashboard')
    else:
        return redirect('admin:index')
