from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, user_id, username, password=None):
        if not user_id:
            raise ValueError('Users must have an ID')

        user = self.model(
            user_id = user_id,
            username = username
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, username, password):
        user = self.create_user(
            user_id = user_id,
            password=password,
            username = username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.username