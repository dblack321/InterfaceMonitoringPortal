from django.http import HttpResponse
from django.shortcuts import render

from IMPapp.models import InterfaceAlert

import random

def acknowledgeAlert(request, alert_id):
    try:
        alert = InterfaceAlert.objects.get(id=alert_id)
        alert.status = 'ACKNOWLEDGED'
        alert.save()
        return render(request, "home.html", {"alerts": InterfaceAlert.objects.all()})
    except InterfaceAlert.DoesNotExist:
        return HttpResponse("Alert not found.", status=404)
    
def removeAlert(request, alert_id):
    try:
        alert = InterfaceAlert.objects.get(id=alert_id)
        alert.delete()
        return render(request, "home.html", {"alerts": InterfaceAlert.objects.all()})
    except InterfaceAlert.DoesNotExist:
        return HttpResponse("Alert not found.", status=404)
    
def createDummyAlerts(request):
    # This function would create some dummy alerts for testing purposes.
    for i in range(5):
        InterfaceAlert.objects.create(
            interface_name=f"Dummy Interface {i+1}",
            description="This is a dummy alert for testing.",
            status="NEW",
            alert_type_id=random.randint(1,3)  # Assuming an AlertType with ID 1 exists
        )
    return render(request, "home.html", {"alerts": InterfaceAlert.objects.all()})