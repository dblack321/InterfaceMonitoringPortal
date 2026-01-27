from django.urls import include, path
from . import views
from . import functions

urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('home/', views.home, name='home'),
    path('masterData/', views.masterData, name='masterData'),
    path('acknowledgeAlert/<int:alert_id>/', functions.acknowledgeAlert, name='acknowledgeAlert'),
    path('removeAlert/<int:alert_id>/', functions.removeAlert, name='removeAlert'),
    path('createDummyAlerts/', functions.createDummyAlerts, name='createDummyAlerts'),
    path('error404/', views.error404, name='error404'),
]
