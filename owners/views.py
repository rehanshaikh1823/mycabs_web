from django.shortcuts import render, redirect
from .models import Owner
from .forms import OwnerProfileForm
from django.contrib import messages
from mycabs.decorators import owner_required


# @login_required
# def owner_dashboard(request):
#     owner = Owner.objects.get(user=request.user)
#     context = {'owner': owner}
#     return render(request, 'owners/dashboard.html', context)

@owner_required
def owner_dashboard(request):
    return render(request, 'owners/dashboard.html')


@owner_required
def update_owner_profile(request):
    owner, created = Owner.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('update_owner_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OwnerProfileForm(instance=owner)
    return render(request, 'owners/update_profile.html', {'form': form})
