from django.forms import inlineformset_factory

from cost import models

from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify


class MaterialForm(forms.ModelForm):

    class Meta:
        model = models.Material
        fields = ['name', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        material = super().save(commit=False)
        new_slug = slugify(material.name)

        if new_slug == "create":
            raise ValidationError("Slug may not be 'create'.")

        if models.Material.objects.filter(slug__iexact=new_slug).exists():
            raise ValidationError("Slug must be unique.")

        material.slug = new_slug

        if commit:
            material.save()

        return material


class DetailForm(forms.ModelForm):
    class Meta:
        model = models.Detail
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        detail = super().save(commit=False)
        new_slug = slugify(detail.name)

        if new_slug == "create":
            raise ValidationError("Slug may not be 'create'.")

        if models.Detail.objects.filter(slug__iexact=new_slug).exists():
            raise ValidationError("Slug must be unique.")

        detail.slug = new_slug

        if commit:
            detail.save()

        return detail
