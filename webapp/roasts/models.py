# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class RoastLevel(models.Model):
    name = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.name

class Bean(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    original_amt = models.FloatField(null=True)
    current_amt = models.FloatField(null=True)
    def __str__(self):
        return self.name

class Roast(models.Model):
    bean = models.ForeignKey(Bean)
    roast_level = models.ForeignKey(RoastLevel)
    customer = models.ForeignKey(Customer)
    roast_date = models.DateTimeField(name='roastdate', auto_now_add=True)
    target_temp = models.IntegerField(null=True)
    weight_before = models.FloatField(null=True)
    weight_after = models.FloatField(null=True)
    description = models.CharField(max_length=255,null=True)
    notes = models.CharField(max_length=255,null=True)
    is_favorite = models.BooleanField(default=False)

    # only 1 Roast must have this set to True at a time.
    # the Roaster thread will watch this roast for any spec changes.
    is_active_roast = models.BooleanField(default=False)

    # spec fields written to one place and observed.
    # snapshots saved as RoastSnapshot w/ timestamp and temperatures
    heater = models.IntegerField(null=True)
    drawfan = models.IntegerField(null=True)
    scrollfan = models.IntegerField(null=True)
    drum = models.IntegerField(null=True)

    def __str__(self):
        return "%s %s %s" % (self.id, self.bean.name, self.roast_level.name)

class RoastSnapshot(models.Model):
    roast = models.ForeignKey(Roast, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(name='data point timestamp', auto_now_add=True)
    heater = models.IntegerField()
    drawfan = models.IntegerField()
    scrollfan = models.IntegerField()
    drum = models.IntegerField()
    env_temp = models.IntegerField()
    bean_temp = models.IntegerField()
    def __str__(self):
        return "%s %s %s" % (self.heater, self.drawfan, self.scrollfan)
    def dict(self):
        return {
            "id": self.id,
            "heater": self.heater,
            "drawfan": self.drawfan,
            "scrollfan": self.scrollfan,
            "drum": self.drum,
            "env_temp": self.env_temp,
            "bean_temp": self.bean_temp
        }

