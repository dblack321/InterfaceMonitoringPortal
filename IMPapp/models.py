from django.db import models

# Create your models here.
class Interface(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

class AlertLevel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

class Alert(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('ACKNOWLEDGED', 'Acknowledged'),
    ]

    id = models.AutoField(primary_key=True)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    alert_level = models.ForeignKey(AlertLevel, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.CharField(max_length=100, null=True, blank=True)

class Metric(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=100)

class Threshold(models.Model):
    id = models.AutoField(primary_key=True)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    alert_level = models.ForeignKey(AlertLevel, on_delete=models.CASCADE)
    upper_limit = models.FloatField()
    lower_limit = models.FloatField()
    description = models.TextField()
