from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from IMPapp.models import Alert, AlertLevel, Interface, Metric, Threshold

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
def masterdata(request):
    return render(request, "masterdata.html", {"interfaces": Interface.objects.all(),
                                               "thresholds": Threshold.objects.all(),
                                               "metrics": Metric.objects.all()})

@login_required
def about(request):
    return render(request, "about.html")

@login_required
def error(request, context):
    return render(request, "error.html", context)

@login_required
def managethreshold(request, action, threshold_id=None):
    
    context = {"action": action}
    if threshold_id is not None:
        threshold = Threshold.objects.get(id=threshold_id)
        if not threshold:
            return error(request, {"error" : "404 Not Found", "message": "Threshold not found.", "redirect_url": "masterdata"})
        context["threshold"] = threshold

    context["interfaces"] = Interface.objects.all()
    context["metrics"] = Metric.objects.all()
    context["alert_levels"] = AlertLevel.objects.all()
    
    return render(request, "manageThreshold.html", context)

@login_required
def manageinterface(request, action, interface_id=None):
    
    context = {"action": action}
    if interface_id is not None:
        interface = Interface.objects.get(id=interface_id)
        if not interface:
            return error(request, {"error" : "404 Not Found", "message": "Interface not found.", "redirect_url": "masterdata"})
        context["interface"] = interface
    
    return render(request, "manageInterface.html", context)

@login_required
def manageMetric(request, action, metric_id=None):
    
    context = {"action": action}
    if metric_id is not None:
        metric = Metric.objects.get(id=metric_id)
        if not metric:
            return error(request, {"error" : "404 Not Found", "message": "Metric not found.", "redirect_url": "masterdata"})
        context["metric"] = metric
    
    return render(request, "manageMetric.html", context)