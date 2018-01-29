# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Bean, RoastLevel, Roast, Customer, RoastSnapshot

admin.site.register(Roast)
admin.site.register(RoastLevel)
admin.site.register(RoastSnapshot)
admin.site.register(Bean)
admin.site.register(Customer)
