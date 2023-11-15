from django.db import models

class Client(models.Model):
    org_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    estimation = models.FloatField()
