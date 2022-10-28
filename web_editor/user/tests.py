from django.test import TestCase

from passlib.handlers.django import django_pbkdf2_sha256
from rest_framework import status

from user.models import User
from common.testcase import TestCaseBase
from common.testcase import UserFactory

class PostUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            user_id='foo',
            username='foo_test',
            email='foo@test.com',
            password='fooPassword',
        )
        cls.post_data = {
            'user_id': 'bar',
            'username': 'bar_test',
            'email': 'bar@test.com',
            'password': 'barPassword',
        }

    def test_post_user_error_duplicate(self):
        data = {
            'user_id': 'foo',
            'username': 'foo_test',
            'email': 'foo@test.com',
            'password': 'fooPassword',
        }
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        # Duplicate User ID
        data = {
            'user_id': 'foo',
            'username': 'foo_test',
            'email': 'foo_not_duplicate@test.com',
            'password': 'fooPassword',
        }
        data.update({'email': 'bad_email'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        # Duplicate Email
        data = {
            'user_id': 'foo_not_duplicate',
            'username': 'foo_test',
            'email': 'foo@test.com',
            'password': 'fooPassword',
        }
        data.update({'email': 'bad_email'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_post_user_error_bad_request(self):
        # Invalid User ID
        data = self.post_data.copy()
        data.update({'user_id': 'very_long_user_id'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        # Invalid Username
        data = self.post_data.copy()
        data.update({'username': 'very_very_long_username'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        # Invalid Email
        data = self.post_data.copy()
        data.update({'email': 'bad_email'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        data = self.post_data.copy()
        data.update({'email': 'super_' * 15 + 'long_email@test.com'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_post_user(self):
        data = self.post_data.copy()
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        user_data = data['user']
        token = data['token']

        self.assertEqual(user_data['user_id'], 'bar')
        self.assertEqual(user_data['username'], 'bar_test')
        self.assertEqual(user_data['email'], 'bar@test.com')
        self.assertTrue(django_pbkdf2_sha256.verify('barPassword', user_data['password']))
        
        self.assertEqual(User.objects.count(), 2)


class GetUserTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_user_error_no_credentials(self):
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_error_not_found(self):
        response = self.client.get('/api/v1/users/100/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user(self):
        self.client.post('/api/v1/signup/', data={
            'user_id': 'bar',
            'username': 'bar_test',
            'email': 'bar@test.com',
            'password': 'barPassword',
        })
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(user_id='bar')
        response = self.client.get('/api/v1/users/' + str(user.pk) + '/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['user_id'], 'bar')
        self.assertEqual(data['username'], 'bar_test')
        self.assertEqual(data['email'], 'bar@test.com')

    def test_get_me(self):
        response = self.client.get('/api/v1/users/me/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['user_id'], 'foo')
        self.assertEqual(data['username'], 'foo_test')
        self.assertEqual(data['email'], 'foo@test.com')


class PutUserTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.put_data = {
            'username': 'foo_put_test',
            'email': 'foo_put_test@test.com',
        }

    def test_put_user_error(self):
        response = self.client.put('/api/v1/users/100/', data=self.put_data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_me_error_duplicate_email(self):
        self.client.post('/api/v1/signup/', data={
            'user_id': 'bar',
            'username': 'bar_test',
            'email': 'bar@test.com',
            'password': 'barPassword',
        })
        self.assertEqual(User.objects.count(), 2)
        data = self.put_data.copy()
        data.update({'email': 'bar@test.com'})
        response = self.client.put('/api/v1/users/me/', data=data, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_me_error_bad_request(self):
        # Try to change User ID
        data = self.put_data.copy()
        data['user_id'] = 'bad_user_id'
        response = self.client.put('/api/v1/users/me/', data=data, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid Username
        data = self.put_data.copy()
        data.update({'username': 'very_very_long_username'})
        response = self.client.put('/api/v1/users/me/', data=data, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid Email
        data = self.put_data.copy()
        data.update({'email': 'bad_email'})
        response = self.client.put('/api/v1/users/me/', data=data, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.put_data.copy()
        data.update({'email': 'super_' * 15 + 'long_email@test.com'})
        response = self.client.put('/api/v1/users/me/', data=data, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_me(self):
        response = self.client.put('/api/v1/users/me/', data=self.put_data, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['user_id'], 'foo')
        self.assertEqual(data['username'], 'foo_put_test')
        self.assertEqual(data['email'], 'foo_put_test@test.com')


class DeleteUserTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_delete_user_error(self):
        response = self.client.delete('/api/v1/users/100/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_me(self):
        response = self.client.delete('/api/v1/users/me/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.get(user_id='foo').is_active)
        self.assertFalse(self.client.login(user_id='foo', password='fooPassword'))


#class CSRFTokenTestCase(TestCase):

#    @classmethod
#    def setUpTestData(cls):
#        cls.user = UserFactory(
#            user_id='foo',
#            username='foo_test',
#            email='foo@test.com',
#            password='fooPassword',
#        )
#        cls.login_data = {
#            'username': 'foo_test',
#            'password': 'fooPassword',
#        }
#        #cls.client = Client(enforce_csrf_checks=True)
    
#    def test_csrf_check_invalid(self):
#        # before login for first time
#        response = self.client.get('/api/v1/verify/')
#        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
#    def test_csrf_check_valid(self):
#        token_value = 'csrftoken'
#        self.client.cookies['csrftoken'] = token_value
#        response = self.client.get('/api/v1/verify/')
#        data = response.json()
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertEqual(data['csrftoken'], token_value)
