from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import SignupForm, LoginForm, EmployeeCreateForm
from .models import User

import secrets
from django.contrib.auth.hashers import make_password


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = "company_admin"   # 🔥 new user = company_admin
        user.save()
        login(request, user)
        return redirect("accounts:dashboard")

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )

        if user:
            login(request, user)
            return redirect("accounts:dashboard")

        form.add_error(None, "Invalid email or password")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def dashboard_view(request):

    # 🔥 superadmin bypass
    if request.user.is_superuser or request.user.role == "superadmin":
        return render(request, "accounts/dashboard.html")

    # only users who need company
    if getattr(request.user, "needs_company", False):
        has_company = hasattr(request.user, "owned_company")
        if not has_company:
            return redirect("company:setup")

    return render(request, "accounts/dashboard.html")



@login_required
def employee_list_view(request):
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    if not hasattr(request.user, "owned_company"):
        return redirect("company:setup")

    company = request.user.owned_company

    if company.status != "active":
        return HttpResponseForbidden("Your company is not approved yet.")

    employees = (
        company.employees
        .filter(role="salesman")
        .select_related("designation")
    )

    return render(
        request,
        "accounts/employee_list.html",
        {
            "employees": employees,
        }
    )



DEFAULT_EMPLOYEE_PASSWORD = "12345678"


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import EmployeeCreateForm


@login_required
def employee_create_view(request):
    # 🔐 Only company admin
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    # 🏢 Company must exist
    if not hasattr(request.user, "owned_company"):
        return redirect("company:setup")

    company = request.user.owned_company

    # ✅ Company must be approved
    if company.status != "active":
        return HttpResponseForbidden("Your company is not approved yet.")

    # 📋 Form
    form = EmployeeCreateForm(
        request.POST or None,
        company=company
    )

    if request.method == "POST" and form.is_valid():
        employee = form.save()
        return redirect("accounts:employee_list")

    return render(
        request,
        "accounts/employee_create.html",
        {"form": form}
    )


@login_required
@require_POST
def employee_delete_view(request, employee_id):

    # only company admin
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    # company must exist
    if not hasattr(request.user, "owned_company"):
        return redirect("company:setup")

    company = request.user.owned_company

    # company must be active
    if company.status != "active":
        return HttpResponseForbidden("Company not active")

    # employee must belong to same company
    employee = get_object_or_404(
        User,
        id=employee_id,
        role="salesman",
    )

    # ❌ extra safety: owner cannot delete himself
    if employee == request.user:
        return HttpResponseForbidden("You cannot delete yourself")

    employee.delete()

    return redirect("accounts:employee_list")
