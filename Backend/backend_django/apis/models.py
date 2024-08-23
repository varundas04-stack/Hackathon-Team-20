from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ngo_admin', 'Ngo_Admin'),
        ('beneficiary', 'Beneficiary'),
        ('hospital_admin', 'Hospital_Admin'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='beneficiary')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    groups = models.ManyToManyField('auth.Group', related_name='customuser_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_permissions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email
    
class Project(models.Model):
    name = models.CharField(max_length=50)
    funding = models.IntegerField()
    disease = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    on_going_treatment = models.CharField(max_length = 50)

class Beneficiary(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    projects = models.ManyToManyField(Project, null=True, blank=True)

