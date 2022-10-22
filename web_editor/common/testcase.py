from django.test import TestCase
from user.models import User

from rest_framework_simplejwt.tokens import RefreshToken

class TestCaseBase(TestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.get(id=1)

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}