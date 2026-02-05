from datetime import datetime, timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from IMPapp.models import Alert, Interface
from . import views


import random

@login_required
def acknowledgeAlert(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.status = 'ACKNOWLEDGED'
        alert.acknowledged_at = datetime.now()
        alert.acknowledged_by = request.user.username
        alert.save()
        return redirect(views.home)
    except Alert.DoesNotExist:
        return views.error404(request, {'message': 'Alert not found.'})

@login_required
def removeAlert(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.delete()
        return redirect(views.home) 
    except Alert.DoesNotExist:
        return views.error404(request, {'message': 'Alert not found.'})

@login_required 
def createDummyAlerts(request):
    # This function would create some dummy alerts for testing purposes.
    dummyInterface = Interface.objects.all().filter(name="dummyInterface").first()

    for i in range(5):
        Alert.objects.create(
            interface= dummyInterface,
            message="This is a dummy alert for testing.",
            status="NEW",
            alert_level_id=random.randint(1,3)
        )
    return redirect(views.home)

@login_required
def acknowledgeAllAlerts(request):
    for alert in Alert.objects.filter(status='NEW'):
        acknowledgeAlert(request, alert.id)
    return redirect(views.home)

@login_required
def removeAllAlerts(request):
    for alert in Alert.objects.filter(status='ACKNOWLEDGED'):
        removeAlert(request, alert.id)
    return redirect(views.home)