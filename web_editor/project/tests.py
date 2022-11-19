from django.test import TestCase
from factory.django import DjangoModelFactory
from project.models import Project
from freezegun import freeze_time
from user.tests import UserFactory
from user.models import User
import datetime
from common.testcase import TestCaseBase
from rest_framework_simplejwt.tokens import RefreshToken

class ProjectFactory(DjangoModelFactory):
    model = Project
    
    @classmethod
    def create(cls, **validated_data):
        project = Project.objects.create(**validated_data)
        return project
    
class PostProjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.project = ProjectFactory(**cls.data)

    def setUp(self):
        self.freezer = freeze_time("2022-02-22 00:00:00")
        self.freezer.start()
        
    def tearDown(self):
        self.freezer.stop()
        
    def test_post_no_title(self):
        data = {
            "writer" : self.user
        }
        response = self.client.post("/api/v1/project/", data, **self.bearer_token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.count(), 1)
        
    def test_post_no_writer(self):
        data = {
            "title" : "no writer"
        }
        response = self.client.post("/api/v1/project/", data, **self.bearer_token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 2)
        
    def test_post_project(self):
        data = {
            "title" : "title2"
        }
        response = self.client.post("/api/v1/project/", data, **self.bearer_token)
        self.assertEqual(response.json()["writer"]["username"], "foo_test")
        self.assertEqual(response.json()["title"], "title2")
        self.assertEqual(Project.objects.count(), 2)
        
    def test_post_project_created_at(self):
        data = {
            "title" : "title2"
        }
        self.client.post("/api/v1/project/", data, **self.bearer_token)
        project = Project.objects.get(title="title2")
        self.assertEqual(project.created_at, datetime.datetime.strptime("2022-02-22 00:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc))
    
class GetProjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data1 = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.data2 = {
            "title" : "title2",
            "writer" : cls.user
        }
        cls.project1 = ProjectFactory(**cls.data1)
        cls.project2 = ProjectFactory(**cls.data2)
        cls.wrong_user = UserFactory(
            user_id='foo2',
            username='foo2_test',
            email='foo2@test.com',
            password='fooPassword',
        )
        
    def setUp(self):
        pass
        
    def test_get_single_project(self):
        data = self.data1.copy()
        data.update({"title" : "title3"})
        post_response = self.client.post("/api/v1/project/", data, **self.bearer_token)
        pk = post_response.json()['id']
        response = self.client.get("/api/v1/project/" + str(pk) + "/", **self.bearer_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "title3")
        
    def test_get_my_project(self):
        response = self.client.get("/api/v1/project/me/", **self.bearer_token)
        self.assertEqual(len(response.json()), 2)
        
    def test_get_my_project_none(self):
        refresh = RefreshToken.for_user(self.wrong_user)
        wrong_user_bearer_token = {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}

        response = self.client.get("/api/v1/project/me/", **wrong_user_bearer_token)
        self.assertEqual(len(response.json()), 0)

    def test_get_project_list(self):
        response = self.client.get("/api/v1/project/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        
    def test_get_wrong_project(self):
        response = self.client.get("/api/v1/project/0/", **self.bearer_token)
        self.assertEqual(response.status_code, 400)
        
class PutProjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.project = ProjectFactory(**cls.data)
        
    def setUp(self):
        self.freezer = freeze_time("2022-02-22 00:00:00")
        self.freezer.start()
        
    def tearDown(self):
        self.freezer.stop()
        
    def test_update_project_title(self):
        id = self.project.id
        data = {"title" : "title2"}
        response = self.client.put("/api/v1/project/" + str(id) + "/", data, content_type="application/json", **self.bearer_token)
        self.assertEqual(response.json()["title"], "title2")
        
    def test_update_project_updated_at(self):
        id = self.project.id 
        data = {"title" : "title2"}
        self.client.put("/api/v1/project/" + str(id) + "/", data, content_type="application/json", **self.bearer_token)
        project = Project.objects.get(title="title2")

        self.assertEqual(project.updated_at, datetime.datetime.strptime("2022-02-22 00:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc))
        
    def test_update_nothing(self):
        id = self.project.id
        self.client.put("/api/v1/project/" + str(id) + "/", {}, content_type="application/json", **self.bearer_token)
        project = Project.objects.get(title="title1")

        self.assertEqual(project.title, "title1")
        self.assertEqual(project.updated_at, datetime.datetime.strptime("2022-02-22 00:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc))
        
    def test_update_wrong_project(self):
        response = self.client.put("/api/v1/project/0/", **self.bearer_token)
        self.assertEqual(response.status_code, 400)
        
    def test_update_project_writer(self):
        id = self.project.id
        wrong_user = UserFactory(
            user_id='foo2',
            username='foo2_test',
            email='foo2@test.com',
            password='fooPassword',
        )
        self.client.put("/api/v1/project/" + str(id) + "/", {"writer" : wrong_user.id}, content_type="application/json", **self.bearer_token)
        project = Project.objects.get(title="title1")
        self.assertNotEqual(project.writer, wrong_user)
        self.assertEqual(project.writer, self.user)        
        
class DeleteProjectTestCase(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.project = ProjectFactory(**cls.data)
        data = cls.data.copy()
        data.update({"title" : "title2"})
        ProjectFactory(**data)
        
    def setUp(self):
        pass
        
    def test_delete_project(self):
        project = Project.objects.get(title="title2")
        response = self.client.delete("/api/v1/project/" + str(project.id) + "/", **self.bearer_token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        response = self.client.get("/api/v1/project/" + str(project.id) + "/", **self.bearer_token)
        self.assertEqual(response.status_code, 400)
        
    def test_delete_wrong_project(self):
        response = self.client.delete("/api/v1/project/0/", **self.bearer_token)
        self.assertEqual(response.status_code, 400)