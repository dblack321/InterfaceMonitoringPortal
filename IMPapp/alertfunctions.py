from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from IMPapp.models import Alert, Interface
from . import views


import random


#
# Acknowledge an alert
#
@login_required
def acknowledgeAlert(request, alert_id):

    # validate user author
    if not validateUserAuthorisation(request, 'change_alert'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to edit alerts.', 'redirect_url': 'home'})

    try:
        alert = Alert.objects.get(id=alert_id)
        alert.status = 'ACKNOWLEDGED'
        alert.acknowledged_at = datetime.now()
        alert.acknowledged_by = request.user.username
        alert.save()
        return redirect(views.home)
    except Alert.DoesNotExist:
        return views.error(request, {'error' : '404 Not Found', 'message': 'Alert not found.', 'redirect_url': 'home'})


#
# Remove an alert
#
@login_required
def removeAlert(request, alert_id):

    # validate user author
    if not validateUserAuthorisation(request, 'delete_alert'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove alerts.', 'redirect_url': 'home'})

    try:
        alert = Alert.objects.get(id=alert_id)
        alert.delete()
        return redirect(views.home) 
    except Alert.DoesNotExist:
        return views.error(request, {'error' : '404 Not Found', 'message': 'Alert not found.', 'redirect_url': 'home'})


#
# Create some dummy alerts for testing
#
@login_required
def createDummyAlerts(request):
    
    # validate user author
    if not validateUserAuthorisation(request, 'add_alert'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add alerts.', 'redirect_url': 'home'})

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


#
# Acknowledge all new alerts
#
@login_required
def acknowledgeAllAlerts(request):
    
     # validate user author
    if not validateUserAuthorisation(request, 'change_alert'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to edit alerts.', 'redirect_url': 'home'})
    
    for alert in Alert.objects.filter(status='NEW'):
        acknowledgeAlert(request, alert.id)
    return redirect(views.home)


#
# Remove all acknowledged alerts
#
@login_required
def removeAllAlerts(request):    
    
     # validate user author
    if not validateUserAuthorisation(request, 'delete_alert'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove alerts.', 'redirect_url': 'home'})
    
    # remove each alert
    for alert in Alert.objects.filter(status='ACKNOWLEDGED'):
        removeAlert(request, alert.id)

    # return to home page
    return redirect(views.home)



# 
# validate user can complete action
#
def validateUserAuthorisation(request, permission_codename):
    for group in request.user.groups.all():
        for perm in group.permissions.all():
            if perm.codename == permission_codename:
                return True