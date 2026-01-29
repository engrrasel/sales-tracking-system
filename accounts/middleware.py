from django.shortcuts import redirect
from django.urls import reverse
from company.models import Company


class CompanySetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # user object না থাকলে
        if not hasattr(request, "user"):
            return self.get_response(request)

        # login না থাকলে
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 🔥 FULL SUPERADMIN BYPASS (MOST IMPORTANT)
        if request.user.is_superuser or getattr(request.user, "role", None) == "superadmin":
            return self.get_response(request)

        setup_url = reverse("company:setup")

        # loop prevent (setup page নিজেকে redirect করবে না)
        if request.path.startswith(setup_url):
            return self.get_response(request)

        # শুধু যাদের company দরকার
        if getattr(request.user, "needs_company", False):
            has_company = Company.objects.filter(owner=request.user).exists()
            if not has_company:
                return redirect("company:setup")

        return self.get_response(request)
