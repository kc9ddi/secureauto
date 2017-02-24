from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=40)

class Reading(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)