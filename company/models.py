from django.db import models


# =========================================================
# Company
# =========================================================

class Company(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("active", "Active"),
        ("hold", "Hold"),
    )

    name = models.CharField(max_length=255)

    owner = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="owned_company",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================================================
# Company Designation
# =========================================================

class CompanyDesignation(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="designations",
    )

    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "title")
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.company.name})"
