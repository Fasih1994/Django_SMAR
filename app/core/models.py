from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """MANAGER for User"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a user"""
        if not email:
            raise ValueError("User must have an email.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_role_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    def __str__(self):
        return self.user_role_name


class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=255)
    package_price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    def __str__(self):
        return self.package_name


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=255)
    description = models.CharField(max_length=3000)
    linkedin_profile = models.URLField()
    industry = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    def __str__(self):
        return self.organization_name


class PackageStatus(models.Model):
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    package_status = models.CharField(max_length=50)
    package_start_date = models.DateField()
    package_end_date = models.DateField()
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(null=True, blank=True)
    last_update_login = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization_id', 'package_id'],
                                    name='package_status_id')
        ]

    def __str__(self):
        return self.package_status


class User(AbstractBaseUser, PermissionsMixin):
    """USER in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    user_role = models.ForeignKey(UserRole, on_delete=models.PROTECT,default=1)
    organization = models.ForeignKey(
    Organization, on_delete=models.CASCADE,default=1
    )
    package = models.ForeignKey(Package, on_delete=models.PROTECT,default=1)

    objects = UserManager()

    USERNAME_FIELD = "email"
