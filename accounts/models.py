from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # email = models.EmailField(
    # null=True,
    # blank=True
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



