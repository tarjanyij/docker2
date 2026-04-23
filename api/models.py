from django.db import models

class Reading(models.Model):
    device_id=models.CharField(max_length=50)
    t1=models.FloatField(null=True, blank=True)
    h1=models.FloatField(null=True, blank=True)
    t2=models.FloatField(null=True, blank=True)
    h2=models.FloatField(null=True, blank=True)
    t3=models.FloatField(null=True, blank=True)
    h3=models.FloatField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Threshold(models.Model):
    SENSOR_CHOICES = [
        ('t1','Hőmérséklet 1'),
        ('h1','Páratartalom 1'),
        ('t2','Hőmérséklet 2'),
        ('h2','Páratartalom 2'),
        ('t3','Hőmérséklet 3'),
        ('h3','Páratartalom 3'),
    ]

    device_id = models.CharField(max_length=50)
    sensor = models.CharField(max_length=10, choices=SENSOR_CHOICES)
    threshold_value = models.FloatField()
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('device_id', 'sensor')]

class AlertRecipient(models.Model):
    device_id=models.CharField(max_length=50)
    sensor=models.CharField(max_length=10,choices=Threshold.SENSOR_CHOICES)
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('device_id', 'sensor', 'email')]

class AlertStatus(models.Model):
    device_id = models.CharField(max_length=50)
    sensor = models.CharField(max_length=10, choices=Threshold.SENSOR_CHOICES)
    is_alerted = models.BooleanField(default=False)
    last_alert_time = models.DateTimeField(null=True, blank=True)
    last_reset_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('device_id', 'sensor')]
