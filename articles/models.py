from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email
from django.db import models


class UserManger(BaseUserManager):
    
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Field email is required')
        if not first_name:
            raise ValueError('Field first_name is required')
        if not last_name:
            raise ValueError('Field last_name is required')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Field email is required')
        if not first_name:
            raise ValueError('Field first_name is required')
        if not last_name:
            raise ValueError('Field last_name is required')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    
    email      = models.EmailField(unique=True, validators=[validate_email])
    first_name = models.CharField(max_length=40)
    last_name  = models.CharField(max_length=50)
    is_active  = models.BooleanField(default=True)
    is_admin   = models.BooleanField(default=False)
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManger()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Article(models.Model):
    
    title     = models.CharField(max_length=120)
    text      = models.TextField()
    views     = models.IntegerField(default=0)
    likes     = models.IntegerField(default=0)
    author_id = models.ForeignKey('User', related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.title