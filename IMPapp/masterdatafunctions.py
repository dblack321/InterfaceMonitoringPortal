from datetime import datetime
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from IMPapp.models import AlertLevel, Interface, Metric, Threshold

from . import views


import random

@login_required
def addThreshold(request):

    Threshold.objects.create(
         interface=get_object_or_404(Interface, id=request.POST.get('interface')),
         alert_level=get_object_or_404(AlertLevel, id=request.POST.get('alert_level')),
         metric=get_object_or_404(Metric, id=request.POST.get('metric')),
         upper_limit=request.POST.get('upper_limit'),
         lower_limit=request.POST.get('lower_limit'),
         description=request.POST.get('description')
    )

    return redirect(views.masterdata)

@login_required
def editThreshold(request, threshold_id):
    
    threshold = get_object_or_404(Threshold, id=threshold_id)
    threshold.interface=get_object_or_404(Interface, id=request.POST.get('interface'))
    threshold.alert_level=get_object_or_404(AlertLevel, id=request.POST.get('alert_level'))
    threshold.metric=get_object_or_404(Metric, id=request.POST.get('metric'))
    threshold.upper_limit=request.POST.get('upper_limit')
    threshold.lower_limit=request.POST.get('lower_limit')
    threshold.description=request.POST.get('description')
    threshold.save()

    return redirect(views.masterdata)

@login_required
def removeThreshold(request, threshold_id):
    
    threshold = get_object_or_404(Threshold, id=threshold_id)
    threshold.delete()

    return redirect(views.masterdata)

@login_required
def addInterface(request):
    
    Interface.objects.create(
         name=request.POST.get('name'),
         description=request.POST.get('description')
    )

    return redirect(views.masterdata)

@login_required
def editInterface(request, interface_id):
    
    interface = get_object_or_404(Interface, id=interface_id)
    interface.name=request.POST.get('name')
    interface.description=request.POST.get('description')
    interface.save()
    
    return redirect(views.masterdata)

@login_required
def removeInterface(request, interface_id):
    
    interface = get_object_or_404(Interface, id=interface_id)
    interface.delete()

    return redirect(views.masterdata)

@login_required
def addMetric(request):
    
    Metric.objects.create(
         name=request.POST.get('name'),
         unit_of_measure=request.POST.get('unit_of_measure'),
    )

    return redirect(views.masterdata)

@login_required
def editMetric(request, metric_id):
    
    metric = get_object_or_404(Metric, id=metric_id)
    metric.name=request.POST.get('name')
    metric.unit_of_measure=request.POST.get('unit_of_measure')
    metric.save()

    return redirect(views.masterdata)

@login_required
def removeMetric(request, metric_id):
    
    metric = get_object_or_404(Metric, id=metric_id)
    metric.delete()

    return redirect(views.masterdata)