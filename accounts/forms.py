from django import forms
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = "general_user"
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)




class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "employee"
        user.is_active = True
        user.set_password("123456")  # default password

        if commit:
            user.save()

        return user
