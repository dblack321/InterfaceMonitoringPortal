from django.contrib import admin

from IMPapp.models import AlertType, InterfaceAlert

# Register your models here.
admin.site.register(AlertType)
admin.site.register(InterfaceAlert)