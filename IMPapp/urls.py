from django.urls import include, path
from . import views
from . import alertfunctions
from . import masterdatafunctions

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('home/', views.home, name='home'),
    path('masterdata/', views.masterdata, name='masterdata'),
    path('about/', views.about, name='about'),
    path('error/', views.error, name='error'),
    
    
    # Management Pages
    path('manageThreshold/<str:action>/', views.managethreshold, name='manageThresholdAdd'),
    path('manageThreshold/<str:action>/<int:threshold_id>/', views.managethreshold, name='manageThresholdEdit'),
    path('manageInterface/<str:action>/', views.manageinterface, name='manageInterfaceAdd'),
    path('manageInterface/<str:action>/<int:interface_id>/', views.manageinterface, name='manageInterfaceEdit'),
    path('manageMetric/<str:action>/', views.manageMetric, name='manageMetricAdd'),
    path('manageMetric/<str:action>/<int:metric_id>/', views.manageMetric, name='manageMetricEdit'),
   
    # Alert Functions
    path('acknowledgeAlert/<int:alert_id>/', alertfunctions.acknowledgeAlert, name='acknowledgeAlert'),
    path('removeAlert/<int:alert_id>/', alertfunctions.removeAlert, name='removeAlert'),
    path('createDummyAlerts/', alertfunctions.createDummyAlerts, name='createDummyAlerts'),
    path('acknowledgeAllAlerts/', alertfunctions.acknowledgeAllAlerts, name='acknowledgeAllAlerts'),
    path('removeAllAlerts/', alertfunctions.removeAllAlerts, name='removeAllAlerts'),
    
    # Threshold Functions
    path('addThreshold/', masterdatafunctions.addThreshold, name='addThreshold'),
    path('editThreshold/<int:threshold_id>/', masterdatafunctions.editThreshold, name='editThreshold'),
    path('removeThreshold/<int:threshold_id>/', masterdatafunctions.removeThreshold, name='removeThreshold'),

    # Interface Functions
    path('addInterface/', masterdatafunctions.addInterface, name='addInterface'),
    path('editInterface/<int:interface_id>/', masterdatafunctions.editInterface, name='editInterface'),
    path('removeInterface/<int:interface_id>/', masterdatafunctions.removeInterface, name='removeInterface'),

    # Metric Functions
    path('addMetric/', masterdatafunctions.addMetric, name='addMetric'),
    path('editMetric/<int:metric_id>/', masterdatafunctions.editMetric, name='editMetric'),
    path('removeMetric/<int:metric_id>/', masterdatafunctions.removeMetric, name='removeMetric'),

]
