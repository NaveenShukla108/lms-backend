from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = (
    ("trainer", "TRAINER"),
    ("admin", "ADMIN"),
    ("student", "STUDENT"),
    ("guest", "GUEST")
)

class User(AbstractUser):

    full_name = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField(max_length=150, null=False, blank=False, unique=True)
    role = models.CharField(choices=USER_ROLES, default="guest", null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    is_verified = models.BooleanField(default=False)

    active_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} {self.role}"
    
    
