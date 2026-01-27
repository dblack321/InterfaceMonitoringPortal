from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from IMPapp.models import InterfaceAlert
from . import views


import random

@login_required
def acknowledgeAlert(request, alert_id):
    try:
        alert = InterfaceAlert.objects.get(id=alert_id)
        alert.status = 'ACKNOWLEDGED'
        alert.save()
        return redirect(views.home)
    except InterfaceAlert.DoesNotExist:
        return views.error404(request, {'message': 'Alert not found.'})

@login_required
def removeAlert(request, alert_id):
    try:
        alert = InterfaceAlert.objects.get(id=alert_id)
        alert.delete()
        return redirect(views.home) 
    except InterfaceAlert.DoesNotExist:
        return views.error404(request, {'message': 'Alert not found.'})

@login_required 
def createDummyAlerts(request):
    # This function would create some dummy alerts for testing purposes.
    for i in range(5):
        InterfaceAlert.objects.create(
            interface_name=f"Dummy Interface {i+1}",
            description="This is a dummy alert for testing.",
            status="NEW",
            alert_type_id=random.randint(1,3)
        )
    return redirect(views.home)