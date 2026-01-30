from django.urls import path
from . import views

from .views import (
    company_setup,
    company_list_view,
    company_status_update_view,
)

app_name = "company"

urlpatterns = [
    # Company
    path("setup/", company_setup, name="setup"),
    path("list/", company_list_view, name="list"),
    path(
        "status/<int:company_id>/<str:status>/",
        company_status_update_view,
        name="status_update",
    ),

    # Designations
    path(
        "designations/",
        views.designation_list_view,
        name="designation_list",
    ),
    path(
        "designations/create/",
        views.designation_create_view,
        name="designation_create",
    ),
    path(
        "designations/<int:pk>/edit/",
        views.designation_edit_view,
        name="designation_edit",
    ),
    path(
        "designations/<int:pk>/delete/",
        views.designation_delete_view,
        name="designation_delete",
    ),
]
