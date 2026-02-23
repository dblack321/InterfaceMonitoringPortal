from datetime import datetime
from urllib import request, response
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from IMPapp.models import AlertLevel, Interface, Metric, Threshold, Alert
from .generalfunctions import handleResponse, validateUserAuthorisation
from .. import views
from .databaseFunctions import AlertDatabaseFunctions, ThresholdDatabaseFunctions, InterfaceDatabaseFunctions, MetricDatabaseFunctions
import random


# add a new threshold
@login_required
def addThreshold(request):
    
    # is the user authroirsised for this action
    if not validateUserAuthorisation(request, 'add_threshold'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add thresholds.', 'redirect_url': 'masterdata'})
    
    # create a new threshold
    threshold = Threshold(
         interface=get_object_or_404(Interface, id=request.POST.get('interface')),
         alert_level=get_object_or_404(AlertLevel, id=request.POST.get('alert_level')),
         metric=get_object_or_404(Metric, id=request.POST.get('metric')),
         upper_limit=request.POST.get('upper_limit'),
         lower_limit=request.POST.get('lower_limit'),
         description=request.POST.get('description'),
    )
    
    response = ThresholdDatabaseFunctions.add_threshold(request, threshold)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


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
    
    response = ThresholdDatabaseFunctions.update_threshold(request, threshold)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


# remove an existing threshold
@login_required
def removeThreshold(request, threshold_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'delete_threshold'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove thresholds.', 'redirect_url': 'masterdata'})
    
    # remove the threshold
    threshold = get_object_or_404(Threshold, id=threshold_id)
    
    response = ThresholdDatabaseFunctions.delete_threshold(request, threshold)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


# add a new interface
@login_required
def addInterface(request):
    
    # is the user authroised for this action
    if not validateUserAuthorisation(request, 'add_interface'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add interfaces.', 'redirect_url': 'masterdata'})
    
    # create a new interface
    interface = Interface(
         name=request.POST.get('name'),
         description=request.POST.get('description')
    )

    response = InterfaceDatabaseFunctions.add_interface(request, interface)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


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
    
    response = InterfaceDatabaseFunctions.update_interface(request, interface)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


# remove an existing interface
@login_required
def removeInterface(request, interface_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'delete_interface'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove interfaces.', 'redirect_url': 'masterdata'})

    # get the interface
    interface = get_object_or_404(Interface, id=interface_id)
    
    response = InterfaceDatabaseFunctions.delete_interface(request, interface)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


# add a new metric
@login_required
def addMetric(request):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'add_metric'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to add metrics.', 'redirect_url': 'masterdata'})
    
    # create the metric
    metric = Metric(
         name=request.POST.get('name'),
         unit_of_measure=request.POST.get('unit_of_measure'),
    )

    response = MetricDatabaseFunctions.add_metric(request, metric)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


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
   
    response = MetricDatabaseFunctions.update_metric(request, metric)
   
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)


# remove an existing metric
@login_required
def removeMetric(request, metric_id):
    
    # is the user authorised for this action
    if not validateUserAuthorisation(request, 'delete_metric'):
        return views.error(request, {'error' : '403 Forbidden', 'message': 'You do not have permission to remove metrics.', 'redirect_url': 'masterdata'})
    
    # get the metric
    metric = get_object_or_404(Metric, id=metric_id)

    # validation passed, now remove the metric
    response = MetricDatabaseFunctions.delete_metric(request, metric)
    
    # redirect to the masterdata page
    return handleResponse(request, response, views.masterdata)