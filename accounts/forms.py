from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# =========================================================
# Signup Form
# =========================================================

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
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


# =========================================================
# Login Form
# =========================================================

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# =========================================================
# Employee Create Form
# =========================================================

class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "designation")

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        if self.company:
            self.fields["designation"].queryset = (
                self.company.designations.all()
            )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = "salesman"
        user.is_active = True
        user.company = self.company   # 🔥 MUST
        user.set_password("12345678")

        if commit:
            user.save()

        return user
