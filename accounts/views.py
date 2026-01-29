from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import SignupForm, LoginForm, EmployeeCreateForm
from .models import User


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

    employees = User.objects.filter(
        owned_company=request.user.owned_company,
        role="salesman"   # ⚠️ employee না, salesman
    )

    return render(
        request,
        "accounts/employee_list.html",
        {"employees": employees}
    )


@login_required
def employee_create_view(request):
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    if not hasattr(request.user, "owned_company"):
        return redirect("company:setup")

    company = request.user.owned_company

    if company.status != "active":
        return HttpResponseForbidden("Company not active")

    form = EmployeeCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        employee = form.save(commit=False)
        employee.owned_company = company
        employee.save()
        return redirect("accounts:employee_list")

    return render(
        request,
        "accounts/employee_create.html",
        {"form": form}
    )
