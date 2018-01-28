import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roasterui.settings")
django.setup()

from roasts.models import Roast, Bean, RoastLevel, Customer

for rl in ["Cinnamon", "New England", "American", "City", "Full City", "Vienna", "French", "Italian", "Spanish"]:
    roastLevel = RoastLevel(name=rl)
    roastLevel.save()

for b in ["Guatemala Antigua Iglesias", "Indonesia Sulawesi"]:
    bean = Bean(name=b)
    bean.save()

c = Customer(name="House")
c.save()


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
