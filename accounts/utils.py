def is_superadmin(user):
    return (
        user.is_authenticated
        and user.is_superuser
        and getattr(user, "role", None) == "superadmin"
    )
