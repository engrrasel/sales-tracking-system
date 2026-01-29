from django.urls import path
from .views import (
    company_setup,
    company_list_view,
    company_status_update_view,
)

app_name = "company"

urlpatterns = [
    path("setup/", company_setup, name="setup"),
    path("list/", company_list_view, name="list"),
    path(
        "status/<int:company_id>/<str:status>/",
        company_status_update_view,
        name="status_update",
    ),
]
