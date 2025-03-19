# mycabs/decorators.py

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def owner_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_owner:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def driver_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_driver:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
