from django.contrib import admin

from IMPapp.models import Interface, AlertLevel, Alert, Metric, Threshold

# Register your models here.
admin.site.register(Interface)
admin.site.register(AlertLevel)
admin.site.register(Alert)
admin.site.register(Metric)
admin.site.register(Threshold)