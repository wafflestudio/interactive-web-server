from django.test import TestCase
from factory.django import DjangoModelFactory
from rest_framework import status

from object.models import Object
from user.tests import UserFactory
from common.testcase import TestCaseBase
from rest_framework_simplejwt.tokens import RefreshToken

class ObjectFactory(DjangoModelFactory):
    class Meta:
        model = Object

    @classmethod
    def create(cls, **kwargs):
        instance = Object.objects.create(**kwargs)
        instance.save()
        return instance


class PostObjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.object = ObjectFactory(
            user=cls.user,
            project_name='foo',
            tag={},
            visibility=True,
            z_index=0,
            svg_type=Object.PATH,
            fill='dummy_fill',
            stroke='dummy_stroke',
            d_string='dummy_d_string',
            src_url='https://dummy.com/image-source',
            x=0,
            y=0,
            w=0,
            h=0,
        )
        cls.post_data = {
            'project_name': 'foo',
            'tag': '{"size": "3", "0": "string", "1": "array", "2": "test", "test": "success"}',
            'visibility': True,
            'z_index': 5,
            'svg_type': 'RE',
            'fill': 'rgba(255,255,255,0)',
            'stroke': 'rgba(255,255,255,0)',
            'd_string': 'M10 10 H 90 V 90 H 10 L 10 10',
            'src_url': 'https://webgam.com/dummy-image-source-url',
            'x': 100,
            'y': -100,
            'h': 30,
            'w': 50
        }

    def test_post_object_error_bad_request(self):
        # Invalid Visibility
        data = self.post_data.copy()
        data.update({'visibility': 'Invalid'})
        response = self.client.post('/api/v1/objects/', data=data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Object.objects.count(), 1)
        # Invalid Svg type
        data = self.post_data.copy()
        data.update({'svg_type': 'Rectangle'})
        response = self.client.post('/api/v1/objects/', data=data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Object.objects.count(), 1)
        # Invalid Source URL
        data = self.post_data.copy()
        data.update({'src_url': 'image'})
        response = self.client.post('/api/v1/objects/', data=data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Object.objects.count(), 1)
        # Invalid Integer
        data = self.post_data.copy()
        data.update({'x': 'NaN'})
        response = self.client.post('/api/v1/objects/', data=data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Object.objects.count(), 1)

    def test_post_object(self):
        data = self.post_data.copy()
        response = self.client.post('/api/v1/objects/', data=data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Object.objects.count(), 2)

        data = response.json()
        self.assertEqual(data['user'], self.user.pk)
        self.assertEqual(data['project_name'], self.post_data['project_name'])
        self.assertEqual(data['tag'], {'size': '3', '0': 'string', '1': 'array', '2': 'test', 'test': 'success'})
        self.assertEqual(data['visibility'], self.post_data['visibility'])
        self.assertEqual(data['z_index'], self.post_data['z_index'])
        self.assertEqual(data['svg_type'], self.post_data['svg_type'])
        self.assertEqual(data['fill'], self.post_data['fill'])
        self.assertEqual(data['stroke'], self.post_data['stroke'])
        self.assertEqual(data['d_string'], self.post_data['d_string'])
        self.assertEqual(data['src_url'], self.post_data['src_url'])
        self.assertEqual(data['x'], self.post_data['x'])
        self.assertEqual(data['y'], self.post_data['y'])
        self.assertEqual(data['h'], self.post_data['h'])
        self.assertEqual(data['w'], self.post_data['w'])


class GetObjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.dummy_user = UserFactory(
            user_id='bar',
            username='bar_test',
            email='bar@test.com',
            password='barPassword',
        )
        cls.objects = []
        for i in range(10):
            cls.objects.append(
                ObjectFactory(
                    user=cls.user,
                    project_name='foo' if i < 5 else 'no_foo',
                    tag={},
                    visibility=True,
                    z_index=0,
                    svg_type=Object.PATH,
                    fill='dummy_fill',
                    stroke='dummy_stroke',
                    d_string='dummy_d_string',
                    src_url='https://dummy.com/image-source',
                    x=0,
                    y=0,
                    w=0,
                    h=0,
                )
            )

    def test_get_object_error_not_found(self):
        # Invalid Object PK
        response = self.client.get('/api/v1/objects/100/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Invalid User
        refresh = RefreshToken.for_user(self.dummy_user)
        wrong_user_bearer_token = {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}

        response = self.client.get('/api/v1/objects/1/', **wrong_user_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/api/v1/objects/', {'project_name': 'foo'}, **wrong_user_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_objects(self):
        response = self.client.get('/api/v1/objects/', {'project_name': 'foo'}, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 5)
        for instance in data:
            self.assertEqual(instance['project_name'], 'foo')

        response = self.client.get('/api/v1/objects/', {'project_name': 'no_foo'}, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 5)
        for instance in data:
            self.assertEqual(instance['project_name'], 'no_foo')

    def test_get_object(self):
        response = self.client.get('/api/v1/objects/' + str(self.objects[0].pk) + '/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['user'], self.user.pk)
        self.assertEqual(data['project_name'], self.objects[0].project_name)
        self.assertEqual(data['tag'], self.objects[0].tag)
        self.assertEqual(data['visibility'], self.objects[0].visibility)
        self.assertEqual(data['z_index'], self.objects[0].z_index)
        self.assertEqual(data['svg_type'], self.objects[0].svg_type)
        self.assertEqual(data['fill'], self.objects[0].fill)
        self.assertEqual(data['stroke'], self.objects[0].stroke)
        self.assertEqual(data['d_string'], self.objects[0].d_string)
        self.assertEqual(data['src_url'], self.objects[0].src_url)
        self.assertEqual(data['x'], self.objects[0].x)
        self.assertEqual(data['y'], self.objects[0].y)
        self.assertEqual(data['h'], self.objects[0].h)
        self.assertEqual(data['w'], self.objects[0].w)


class PatchObjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.object = ObjectFactory(
            user=cls.user,
            project_name='foo',
            tag={},
            visibility=True,
            z_index=0,
            svg_type=Object.PATH,
            fill='dummy_fill',
            stroke='dummy_stroke',
            d_string='dummy_d_string',
            src_url='https://dummy.com/image-source',
            x=0,
            y=0,
            w=0,
            h=0,
        )

    def test_patch_object_error_not_found(self):
        response = self.client.patch('/api/v1/objects/100/', data={}, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_object_error_bad_request(self):
        # Change user
        response = self.client.patch('/api/v1/objects/' + str(self.object.pk) + '/', data={'user': 'bar'}, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Change project
        response = self.client.patch('/api/v1/objects/' + str(self.object.pk) + '/', data={'project_name': 'bar'}, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_object(self):
        response = self.client.patch('/api/v1/objects/' + str(self.object.pk) + '/', data={'tag': '{"patch": "test"}'}, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['tag'], '{"patch": "test"}')
        self.assertEqual(Object.objects.count(), 1)
        response = self.client.patch('/api/v1/objects/' + str(self.object.pk) + '/', data={'visibility': True}, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['visibility'], True)
        self.assertEqual(Object.objects.count(), 1)
        response = self.client.patch('/api/v1/objects/' + str(self.object.pk) + '/', data={'z_index': 10}, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['z_index'], 10)
        self.assertEqual(Object.objects.count(), 1)
        response = self.client.patch('/api/v1/objects/' + str(self.object.pk) + '/', data={'svg_type': 'TE'}, content_type='application/json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['svg_type'], 'TE')
        self.assertEqual(Object.objects.count(), 1)


class DeleteObjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
        cls.object = ObjectFactory(
            user=cls.user,
            project_name='foo',
            tag={},
            visibility=True,
            z_index=0,
            svg_type=Object.PATH,
            fill='dummy_fill',
            stroke='dummy_stroke',
            d_string='dummy_d_string',
            src_url='https://dummy.com/image-source',
            x=0,
            y=0,
            w=0,
            h=0,
        )

    def test_delete_object_error_not_found(self):
        response = self.client.delete('/api/v1/objects/100/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_object(self):
        response = self.client.delete('/api/v1/objects/' + str(self.object.pk) + '/', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['object'].get('id'), None)
        self.assertTrue(response.json()['success'])
