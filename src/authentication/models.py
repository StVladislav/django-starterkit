from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.mixins import CreatedAtMixin


class UserManager(BaseUserManager):
    """
    Rewrite create_user and crete_superuser for using email as authentication.
    """
    def create_user(self, email, first_name, last_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault('last_name', '')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email=email, first_name=first_name, password=password, **extra_fields)


class User(AbstractBaseUser, CreatedAtMixin, PermissionsMixin):
    """
    If you add or delete fields don't forget to reflect 
    the changes in the CustomUserCreateSerializer serializer.py 
    and in the UserManager.

    How to add new user's field?
    1. Add field to this model
    2. Add field to the UserManager create_user and create_superuser
    3. Add field to the CustomUserCreateSerializer
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # User is active by default
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
