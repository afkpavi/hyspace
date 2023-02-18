from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from uuid import uuid4
from datetime import datetime


class AccountManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        email = self.normalize_email(email)

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):

        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        for field in ['is_active', 'is_staff', 'is_superuser']:
            kwargs.setdefault(field, True)

            if kwargs.get(field) is not True:
                raise Exception(f'{field} value should be True for super_user')

        return self.create_user(email, password, **kwargs)


class Account(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid4)
    full_name = models.CharField(null=False, max_length=250)
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    objects = AccountManager()

    def __str__(self) -> str:
        return self.full_name

