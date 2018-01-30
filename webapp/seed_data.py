import django, os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roasterui.settings")
django.setup()
application = get_wsgi_application()

from roasts.models import Roast, Bean, RoastLevel, Customer

expectedRoastLevels = ["Cinnamon", "New England", "American", "City", "Full City", "Vienna", "French", "Italian", "Spanish"]
roastLevels = RoastLevel.objects.all()

if len(roastLevels) != len(expectedRoastLevels):
    for rl in expectedRoastLevels:
        roastLevel = RoastLevel(name=rl)
        roastLevel.save()

expectedBeans = ["Guatemala Antigua Iglesias", "Indonesia Sulawesi"]
beans = Bean.objects.all()

if len(expectedBeans) != len(beans):
    for b in expectedBeans:
        bean = Bean(name=b)
        bean.save()

    c = Customer(name="House")
    c.save()



from roasterio.roaster import Roaster
roaster = Roaster()
roaster.start()

call_command('runserver',  '127.0.0.1:8000')


# rl = RoastLevel.objects.get(id=1)
# bean = Bean.objects.get(id=1)
#
# r = Roast(bean=bean, roast_level=rl, customer=c)
# r = r.save()
#
#
# roasts = Roast.objects.filter(id=3)
# roasts = Roast.objects.all()
#
# for r in roasts:
#     r1 = Roast.objects.get(id=r.id)
#     if r1.id:
#         print r1.id, r1.bean.name, r1.is_favorite
#         print "\t", r1.RoastSnapshot_set.all()
#
#         s = r1.RoastSnapshot_set.create(
#             heater=10,
#             drawfan=2,
#             scrollfan=0,
#             drum=1,
#             env_temp=841,
#             bean_temp=415
#         )
#
#         print s.roast
#
#         print r1.RoastSnapshot_set.all()
