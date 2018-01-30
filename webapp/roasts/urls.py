from django.conf.urls import url

from . import views

app_name = 'roasts'

urlpatterns = [
    # /roasts/
    url(r'^$', views.index, name='index'),
    # /roasts/newroast
    url(r'^newroast$', views.newroast, name='newroast'),
    # /roasts/completed
    url(r'^completed$', views.completed, name='completed'),
    # /roasts/upcoming
    url(r'^upcoming', views.upcoming, name='upcoming'),

    # /roasts/4
    url(r'^(?P<roast_id>[0-9]+)/$', views.detail, name='detail'),
    # /roasts/4/update
    url(r'^(?P<roast_id>[0-9]+)/update$', views.update, name='update'),
    # /roasts/4/snapshots
    url(r'^(?P<roast_id>[0-9]+)/snapshots', views.snapshots, name='snapshots'),
    # /roasts/4/specupdate
    url(r'^(?P<roast_id>[0-9]+)/specupdate', views.specupdate, name='specupdate'),
    # /roasts/4/roastctrl
    url(r'^(?P<roast_id>[0-9]+)/roastctrl', views.roastctrl, name='roastctrl'),

    # /roasts/orders
    url(r'^orders$', views.orders, name='orders'),

    # /roasts/customers
    url(r'^customers', views.customers, name='customers'),

    # /roasts/beans
    url(r'^beans', views.beans, name='beans'),

    # /roasts/roastlevels
    url(r'^roastlevels', views.roastlevels, name='roastlevels'),
]
