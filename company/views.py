from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from accounts.utils import is_superadmin

from .models import Company, CompanyDesignation
from .forms import CompanyForm, CompanyDesignationForm


# =========================================================
# Company Setup
# =========================================================

@login_required
def company_setup(request):
    # superadmin কখনো company setup করবে না
    if request.user.is_superuser or request.user.role == "superadmin":
        return redirect("accounts:dashboard")

    # আগেই company থাকলে dashboard
    if Company.objects.filter(owner=request.user).exists():
        return redirect("accounts:dashboard")

    form = CompanyForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        company = form.save(commit=False)
        company.owner = request.user
        company.status = "pending"
        company.save()
        return redirect("accounts:dashboard")

    return render(
        request,
        "company/setup.html",
        {"form": form},
    )


# =========================================================
# Company List (Superadmin)
# =========================================================

@login_required
def company_list_view(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied")

    companies = Company.objects.all().order_by("-created_at")

    return render(
        request,
        "company/company_list.html",
        {"companies": companies},
    )


# =========================================================
# Company Status Update
# =========================================================

@login_required
def company_status_update_view(request, company_id, status):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied")

    company = get_object_or_404(Company, id=company_id)

    if status in ["active", "hold"]:
        company.status = status
        company.save()

    return redirect("company:list")


# =========================================================
# Designation List
# =========================================================

@login_required
def designation_list_view(request):
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    company = getattr(request.user, "owned_company", None)
    if not company:
        return redirect("company:setup")

    designations = company.designations.all()

    return render(
        request,
        "company/designation_list.html",
        {"designations": designations},
    )


# =========================================================
# Designation Create
# =========================================================

@login_required
def designation_create_view(request):
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    company = getattr(request.user, "owned_company", None)
    if not company:
        return redirect("company:setup")

    form = CompanyDesignationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        designation = form.save(commit=False)
        designation.company = company
        designation.save()
        return redirect("company:designation_list")

    return render(
        request,
        "company/designation_create.html",
        {
            "form": form,
            "company": company,
        },
    )


# =========================================================
# Designation Edit
# =========================================================

@login_required
def designation_edit_view(request, pk):
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    company = request.user.owned_company

    designation = get_object_or_404(
        CompanyDesignation,
        pk=pk,
        company=company,
    )

    form = CompanyDesignationForm(
        request.POST or None,
        instance=designation,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("company:designation_list")

    return render(
        request,
        "company/designation_edit.html",
        {"form": form},
    )


# =========================================================
# Designation Delete
# =========================================================

@login_required
def designation_delete_view(request, pk):
    if request.user.role != "company_admin":
        return HttpResponseForbidden("Access denied")

    company = request.user.owned_company

    designation = get_object_or_404(
        CompanyDesignation,
        pk=pk,
        company=company,
    )

    # Employee থাকলে delete হবে না
    if designation.employees.exists():
        return HttpResponseForbidden(
            "এই designation এর অধীনে employee আছে, delete করা যাবে না"
        )

    if request.method == "POST":
        designation.delete()

    return redirect("company:designation_list")
