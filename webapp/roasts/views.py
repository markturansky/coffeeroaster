# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, reverse

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
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

def specupdate(request, roast_id):
    roast = get_object_or_404(Roast, pk=roast_id)
    roast.heater = request.GET.get('heater')
    roast.drawfan = request.GET.get('drawfan')
    roast.scrollfan = request.GET.get('scrollfan')
    roast.drum = request.GET.get('drum')
    roast.save()
    return HttpResponse("OK")

def roastctrl(request, roast_id):
    roast = get_object_or_404(Roast, pk=roast_id)
    roast.is_active_roast = request.GET.get('onoff') in ["true", 1]
    roast.save()
    return HttpResponse("OK")

def snapshots(request, roast_id):
    roast = get_object_or_404(Roast, pk=roast_id)
    data = []
    last = request.GET.get('last')
    ss = None
    if last:
       ss = roast.roastsnapshot_set.filter(id__gt=last)
    else:
        ss = roast.roastsnapshot_set.all()
    for s in ss:
        data.append(s.dict())
    return JsonResponse(data, safe=False)

def completed(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/completed.html', context))

def upcoming(request):
    r = Roast.objects.all()
    context = { 'roasts' : r, 'count': len(r) }
    return HttpResponse(render(request, 'roasts/upcoming.html', context))

def detail(request, roast_id):
    roast = get_object_or_404(Roast, pk=roast_id)
    active = Roast.objects.filter(is_active_roast=1)
    context = { 'roast' : roast, 'active': active }
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
