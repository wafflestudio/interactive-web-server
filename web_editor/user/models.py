from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, user_id, email, password, **extra_fields):
        if not user_id:
            raise ValueError("Users must have an ID")

        email = self.normalize_email(email)
        user = self.model(
            user_id=user_id,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, email, password=None, **extra_fields):

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(user_id, email, password, **extra_fields)

    def create_superuser(self, user_id, email, password, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError("Wrong role for admin")

        return self._create_user(user_id, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username
