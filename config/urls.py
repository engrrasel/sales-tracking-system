from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # accounts related URLs
    path("accounts/", include("accounts.urls")),

    # future apps
    # path("company/", include("company.urls")),
    # path("sales/", include("sales.urls")),
    path("company/", include("company.urls")),

    
]
