from django import forms

from .models import ManufacturingPlan, ManufacturingPlanProductResources


class ManufacturingPlanForm(forms.ModelForm):

    class Meta:
        model = ManufacturingPlan
        fields = ('name', )


class ManufacturingPlanProductResourcesForm(forms.ModelForm):

    class Meta:
        model = ManufacturingPlanProductResources
        fields = ('product_resources', 'amount')