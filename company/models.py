from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Company(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("active", "Active"),
        ("hold", "On Hold"),
    )

    name = models.CharField(max_length=255)

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="owned_company"  # 🔥 এখানে পরিবর্তন
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
