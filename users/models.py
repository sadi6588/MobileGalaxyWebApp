from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        if self.is_staff and not self.pk:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if User.objects.filter(is_staff=True).count() >= 5:
                raise ValidationError("Maximum of 5 admin users allowed.")
        super().save(*args, **kwargs)
