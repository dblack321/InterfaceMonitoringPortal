from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from IMPapp.models import InterfaceAlert

# Create your views here.
@login_required
def home(request):
    return render(request, "home.html", {"alerts": InterfaceAlert.objects.order_by('-timestamp'), 
                                         "new_alerts_count": InterfaceAlert.objects.filter(status='NEW').count(), 
                                         "acknowledged_alerts_count": InterfaceAlert.objects.filter(status='ACKNOWLEDGED').count(),
                                         "critical_alerts_count": InterfaceAlert.objects.filter(alert_type__name='critical').count(),
                                         "warning_alerts_count": InterfaceAlert.objects.filter(alert_type__name='warning').count(),
                                         "minor_alerts_count": InterfaceAlert.objects.filter(alert_type__name='minor').count()})

@login_required
def masterData(request):
    return render(request, "masterdata.html")

@login_required
def error404(request, context):
    return render(request, "404.html", context, status=404)