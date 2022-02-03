from django.db import models


# Create your models here.
class info(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    Email = models.EmailField(max_length=240)
class intak(models.Model):
    id = models.AutoField(primary_key=True)
    intakname = models.CharField(max_length=20)

class track(models.Model):
    id = models.AutoField(primary_key=True)
    trackname = models.CharField(max_length=20)

