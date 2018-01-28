# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, reverse

from django.http import HttpResponse, HttpResponseRedirect
from roasts.models import Roast, Bean, RoastLevel, Customer
from roasts.forms import NewRoastModelForm


def index(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/index.html', context))

def newroast(request):
    form = NewRoastModelForm()
    context = {'form': form }
    return HttpResponse(render(request, 'roasts/newroast.html', context))

def update(request, roast_id):
    form = NewRoastModelForm(request.POST)
    roast = form.save()
    return HttpResponseRedirect(reverse('roasts:detail', args=(roast.id,)))

def completed(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/completed.html', context))

def upcoming(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/upcoming.html', context))

def detail(request, roast_id):
    r = get_object_or_404(Roast, pk=roast_id)
    context = { 'roast' : r }
    return HttpResponse(render(request, 'roasts/details.html', context))



def orders(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/orders.html', context))

def customers(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/customers.html', context))

def beans(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/beans.html', context))

def roastlevels(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/roastlevels.html', context))
