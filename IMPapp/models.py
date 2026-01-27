from django.db import models

# Create your models here.
class AlertType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class AlertStatus(models.TextChoices):
    NEW = 'NEW', 'New'
    ACKOWLEDGED = 'ACKNOWLEDGED', 'Acknowledged'

class InterfaceAlert(models.Model):
    id = models.AutoField(primary_key=True)
    interface_name = models.CharField(max_length=100)
    alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=AlertStatus.choices, default=AlertStatus.NEW)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

