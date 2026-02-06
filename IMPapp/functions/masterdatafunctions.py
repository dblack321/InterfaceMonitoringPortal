from datetime import datetime
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from IMPapp.models import AlertLevel, Interface, Metric, Threshold, Alert
from .generalfunctions import validateUserAuthorisation
from .. import views
import random


# add a new threshold
@login_required
def addThreshold(request):
    
    # is the user authroirsised for this action
    if not validateUserAuthorisation(request, 'add_threshold'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add thresholds.', 'redirect_url': 'masterdata'})
    
    # create a new threshold
    Threshold.objects.create(
         interface=get_object_or_404(Interface, id=request.POST.get('interface')),
         alert_level=get_object_or_404(AlertLevel, id=request.POST.get('alert_level')),
         metric=get_object_or_404(Metric, id=request.POST.get('metric')),
         upper_limit=request.POST.get('upper_limit'),
         lower_limit=request.POST.get('lower_limit'),
         description=request.POST.get('description')
    )
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# edit an existing threshold
@login_required
def editThreshold(request, threshold_id):
    
    # is the user authorised for this action
    
    if not validateUserAuthorisation(request, 'change_threshold'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to edit thresholds.', 'redirect_url': 'masterdata'})
    
    # alter the attributes of the threshold
    threshold = get_object_or_404(Threshold, id=threshold_id)
    threshold.interface=get_object_or_404(Interface, id=request.POST.get('interface'))
    threshold.alert_level=get_object_or_404(AlertLevel, id=request.POST.get('alert_level'))
    threshold.metric=get_object_or_404(Metric, id=request.POST.get('metric'))
    threshold.upper_limit=request.POST.get('upper_limit')
    threshold.lower_limit=request.POST.get('lower_limit')
    threshold.description=request.POST.get('description')
    threshold.save()
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# remove an existing threshold
@login_required
def removeThreshold(request, threshold_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'delete_threshold'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove thresholds.', 'redirect_url': 'masterdata'})
    
    # remove the threshold
    threshold = get_object_or_404(Threshold, id=threshold_id)
    threshold.delete()
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# add a new interface
@login_required
def addInterface(request):
    
    # is the user authroised for this action
    if not validateUserAuthorisation(request, 'add_interface'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add interfaces.', 'redirect_url': 'masterdata'})
    
    # create a new interface
    Interface.objects.create(
         name=request.POST.get('name'),
         description=request.POST.get('description')
    )
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# edit an existing interface
@login_required
def editInterface(request, interface_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'change_interface'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to edit interfaces.', 'redirect_url': 'masterdata'})
    
    # edit the existing interface
    interface = get_object_or_404(Interface, id=interface_id)
    interface.name=request.POST.get('name')
    interface.description=request.POST.get('description')
    interface.save()
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# remove an existing interface
@login_required
def removeInterface(request, interface_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'delete_interface'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove interfaces.', 'redirect_url': 'masterdata'})

    # get the interface
    interface = get_object_or_404(Interface, id=interface_id)
    
    # validate not assigned to a threshold
    for threshold in Threshold.objects.all():
        if threshold.interface.id == interface.id:
            return views.error(request, {'error' : 'Interface in use', 'message': 'Interface is still assigned to a threshold.', 'redirect_url': 'masterdata'})
   
    # validate not assigned to any existing alerts
    for alert in Alert.objects.all():
        if alert.interface.id == interface.id:
            return views.error(request, {'error' : 'Interface in use', 'message': 'There are still active alerts for this Interface.', 'redirect_url': 'masterdata'})
    
    # validation passed, now remove the alert
    interface.delete()
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# add a new metric
@login_required
def addMetric(request):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'add_metric'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add metrics.', 'redirect_url': 'masterdata'})
    
    # create the metric
    Metric.objects.create(
         name=request.POST.get('name'),
         unit_of_measure=request.POST.get('unit_of_measure'),
    )
    
    # redirect to the masterdata page
    return redirect(views.masterdata)


# edit an existing metric
@login_required
def editMetric(request, metric_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'change_metric'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to edit metrics.', 'redirect_url': 'masterdata'})
    
    # edit the metric
    metric = get_object_or_404(Metric, id=metric_id)
    metric.name=request.POST.get('name')
    metric.unit_of_measure=request.POST.get('unit_of_measure')
    metric.save()
   
    # redirect to the masterdata page
    return redirect(views.masterdata)


# remove an existing metric
@login_required
def removeMetric(request, metric_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'delete_metric'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove metrics.', 'redirect_url': 'masterdata'})
    
    # get the metric
    metric = get_object_or_404(Metric, id=metric_id)

     # validate not assigned to a threshold
    for threshold in Threshold.objects.all():
        if threshold.metric.id == metric.id:
            return views.error(request, {'error' : 'Metric in use', 'message': 'Metric is still assigned to a threshold.', 'redirect_url': 'masterdata'})

    # validation passed, now remove the metric
    metric.delete()
    
    # redirect to the masterdata page
    return redirect(views.masterdata)