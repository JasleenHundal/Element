from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(email, password, **extra_fields)
        
        if not user.is_staff:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not user.is_superuser:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user.save(using=self._db)
        return user        

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USER_ROLES = [('Admin', 'Admin'), ('Manager', 'Manager'), ('Staff', 'Staff')]
    role = models.CharField(max_length=10, choices=USER_ROLES)
    # Add any other fields you need

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

