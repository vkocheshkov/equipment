from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @classmethod
    def get_superuser(cls):
        superuser = cls.objects.filter(is_superuser=True).first()
        return superuser
