# mycabs/views.py

from django.shortcuts import render


def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)
