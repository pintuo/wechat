import datetime
from django.db import models

# Create your models here.

class User(models.Model):
    openid = models.CharField(max_length=40)
    vipid=models.CharField(max_length=20)
    cardno=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    sex=models.CharField(max_length=4)
    jlzt=models.CharField(max_length=1)

    def __unicode__(self):
        return self.name

class Netbar(models.Model):
    numb=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    boss_name=models.CharField(max_length=20)
    jlzt=models.CharField(max_length=1)

    def __unicode__(self):
        return self.name
class Computer(models.Model):
    numb=models.CharField(max_length=20)
    netbar_name=models.CharField(max_length=20)
    usable=models.CharField(max_length=4)
    jlzt=models.CharField(max_length=1)

    def __unicode__(self):
        return self.numb

class User_comp(models.Model):
    openid = models.CharField(max_length=40)
    comp_numb=models.CharField(max_length=20)
    kssj=models.DateTimeField()
    jssj=models.DateTimeField()
    zje=models.FloatField(max_length=10)
    xfje=models.FloatField(max_length=10)
    jlzt=models.CharField(max_length=1)


