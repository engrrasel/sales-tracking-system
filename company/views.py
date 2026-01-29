from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import Company


from django.http import HttpResponseForbidden
from accounts.utils import is_superadmin

from django.shortcuts import get_object_or_404
from .forms import CompanyForm






@login_required
def company_setup(request):

    # 🔥 superadmin কখনো company setup করবে না
    if request.user.is_superuser or request.user.role == "superadmin":
        return redirect("accounts:dashboard")

    # আগেই company থাকলে dashboard
    if Company.objects.filter(owner=request.user).exists():
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.status = "pending"
            company.save()
            return redirect("accounts:dashboard")
    else:
        form = CompanyForm()

    return render(request, "company/setup.html", {
        "form": form
    })


def company_list_view(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied")

    companies = Company.objects.all().order_by("-created_at")

    return render(
        request,
        "company/company_list.html",
        {"companies": companies}
    )





def company_status_update_view(request, company_id, status):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied")

    company = get_object_or_404(Company, id=company_id)

    if status in ["active", "hold"]:
        company.status = status
        company.save()

    return redirect("company:list")