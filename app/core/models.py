from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """MANAGER for User"""

    def create_user(self, email, password=None, organization=None,
                    package=None, role=None, is_admin=False, **extra_fields):
        """Create and save a user"""
        if is_admin is False:
            if not email:
                raise ValueError("User must have an email.")

            if not organization:
                raise ValueError("User must have an organization.")

            if package is None:
                package = Package.objects.get(name='basic')

            if role is None:
                role = UserRole.objects.get(name='admin')

            user = self.model(email=self.normalize_email(email),
                              organization=organization, package=package,
                              role=role, **extra_fields)
            user.set_password(password)
            user.save(using=self.db)
        else:
            user = self.model(email=self.normalize_email(email),
                              organization=organization, package=package,
                              role=role, **extra_fields)
            user.set_password(password)
            user.save(using=self.db)

        return user

    def create_superuser(self, email, password, organization=None,
                         package=None, role=None, **extra_fields):
        """Create and return new superuser"""

        user = self.create_user(email=email, password=password,
                                organization=organization, package=package,
                                role=role, is_admin=True, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class UserRole(models.Model):
    name = models.CharField(max_length=255, default="admin")
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=255, default="basic")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=3000, null=True)
    linkedin_profile = models.URLField(null=True)
    industry = models.CharField(max_length=1000, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """USER in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=True, blank=True
        )
    package = models.ForeignKey(
        'Package', null=True, blank=True, on_delete=models.PROTECT, default=1
        )
    role = models.ForeignKey(
        'UserRole', null=True, blank=True, on_delete=models.PROTECT, default=1
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
