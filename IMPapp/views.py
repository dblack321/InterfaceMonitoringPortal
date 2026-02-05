from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from IMPapp.models import Alert

# Create your views here.
@login_required
def home(request):
    return render(request, "home.html", {"new_alerts_count": Alert.objects.filter(status='NEW').count(), 
                                         "acknowledged_alerts_count": Alert.objects.filter(status='ACKNOWLEDGED').count(),
                                         "total_alerts_count": Alert.objects.all().count(),
                                         "critical_alerts": Alert.objects.filter(alert_level__name='critical'),
                                         "warning_alerts": Alert.objects.filter(alert_level__name='warning'),
                                         "minor_alerts": Alert.objects.filter(alert_level__name='minor')})

@login_required
def about(request):
    return render(request, "about.html")

@login_required
def error404(request, context):
    return render(request, "404.html", context, status=404)