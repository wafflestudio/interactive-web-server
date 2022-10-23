from django.test import TestCase
from user.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from factory.django import DjangoModelFactory
from freezegun import freeze_time

class UserFactory(DjangoModelFactory):
    class Meta:
       model = User

    email = 'test@test.com'

    @classmethod
    def create(cls, **kwargs):
        user = User.objects.create(**kwargs)
        user.set_password(kwargs.get('password', ''))
        user.save()
        return user

class TestCaseBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            user_id='foo',
            username='foo_test',
            email='foo@test.com',
            password='fooPassword',
        )
        
        freezer = freeze_time("2022-02-22 00:00:00")
        freezer.start()
        refresh = RefreshToken.for_user(cls.user)
        cls.bearer_token = {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}
