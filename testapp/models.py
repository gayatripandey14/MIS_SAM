from email.policy import default
from tkinter import CASCADE
from django.db import models

# Create your models here.
class AccountsSmscroutes(models.Model):
    smpp_smsc_id = models.IntegerField(unique=True)
    creation_type = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    operator = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    date = models.DateTimeField()
    country = models.CharField(max_length=100, blank=True, null=True)
    delete = models.BooleanField(blank=True, null=True,default = False)
    user = models.IntegerField(blank=False,null=False)


class AccountsSmppusers(models.Model):
    smpp_userdetails_id = models.CharField(max_length=100,unique=True)
    date = models.DateTimeField()
    on_submit = models.BooleanField(blank=True, null=True)
    sale_price = models.FloatField()
    route = models.ForeignKey(AccountsSmscroutes, models.CASCADE, blank=True, null=True)
    user = models.IntegerField(blank=False,null=False)
    delete = models.BooleanField(blank=True, null=True,default = False)
    assigned_to = models.IntegerField(blank=False,null=False)

