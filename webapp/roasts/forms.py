from django import forms

from roasts.models import Roast, Bean, RoastLevel, Customer

customers = Customer.objects.all()
roastLevels = RoastLevel.objects.all()
beans = Bean.objects.all()

class NewRoastModelForm(forms.ModelForm):
    class Meta:
        model = Roast
        fields = [
            'bean',
            'roast_level',
            'customer'
            # 'target_temp',
            # 'weight_before',
            # 'description',
            # 'notes'
        ]

#
# class NewRoastForm(forms.Form):
#     target_temp = forms.CharField(label="Target Temp (F)", max_length=500)
#     weight_before = forms.FloatField(label="Weight Before (oz)")
#     notes = forms.CharField(label="Notes", max_length=500)
#     description = forms.CharField(label="Description", max_length=500)
#
#     roastLevels = RoastLevel.objects.all()
#     choices = []
#     for i in roastLevels:
#         choices.append((i.id, i.name))
#     roastLevel = forms.ChoiceField(widget=forms.Select, choices=choices)
#
#     customers = Customer.objects.all()
#     choices = []
#     for i in customers:
#         choices.append((i.id, i.name))
#     customer = forms.ChoiceField(widget=forms.Select, choices=choices)
#
#     beans = Bean.objects.all()
#     choices = []
#     for i in beans:
#         choices.append((i.id, i.name))
#     bean = forms.ChoiceField(widget=forms.Select, choices=choices)
