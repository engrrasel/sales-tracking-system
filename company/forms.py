from django import forms

from .models import Company, CompanyDesignation


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name",)


class CompanyDesignationForm(forms.ModelForm):
    class Meta:
        model = CompanyDesignation
        fields = ("title",)
