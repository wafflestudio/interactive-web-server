from django.test import TestCase
from factory.django import DjangoModelFactory
from project.models import Project
from freezegun import freeze_time
from user.tests import UserFactory
from user.models import User
import datetime
class ProjectFactory(DjangoModelFactory):
    model = Project
    
    @classmethod
    def create(cls, **validated_data):
        project = Project.objects.create(**validated_data)
        return project
    
class PostProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            user_id='foo',
            username='foo_test',
            email='foo@test.com',
            password='fooPassword',
        )
        cls.data = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.project = ProjectFactory(**cls.data)

    def setUp(self):
        self.client.login(user_id='foo', password='fooPassword')
        self.freezer = freeze_time("2022-02-22 00:00:00")
        self.freezer.start()
        
    def tearDown(self):
        self.freezer.stop()
        
    def test_post_no_title(self):
        user = User.objects.get(user_id="foo")
        data = {
            "writer" : user
        }
        response = self.client.post("/api/v1/project/", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.count(), 1)
        
    def test_post_no_writer(self):
        data = {
            "title" : "no writer"
        }
        response = self.client.post("/api/v1/project/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 2)
        
    def test_post_project(self):
        data = {
            "title" : "title2",
            "writer" : self.user
        }
        response = self.client.post("/api/v1/project/", data)
        self.assertEqual(response.json()['writer']['username'], "foo_test")
        self.assertEqual(response.json()['title'], "title2")
        self.assertEqual(Project.objects.count(), 2)
        
    def test_post_project_created_at(self):
        data = {
            "title" : "title2",
            "writer" : self.user
        }
        self.client.post("/api/v1/project/", data)
        project = Project.objects.get(title="title2")
        self.assertEqual(project.created_at, datetime.datetime.strptime("2022-02-22 00:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc))
    
class GetProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            user_id='foo',
            username='foo_test',
            email='foo@test.com',
            password='fooPassword',
        )
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
        self.client.login(user_id='foo', password='fooPassword')
        
    def test_get_single_project(self):
        data = self.data1.copy()
        data.update({"title" : "title3"})
        post_response = self.client.post("/api/v1/project/", data)
        pk = post_response.json()['id']
        response = self.client.get("/api/v1/project/" + str(pk) + "/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "title3")
        
    def test_get_my_project(self):
        response = self.client.get("/api/v1/project/me/")
        self.assertEqual(len(response.json()), 2)
        
    def test_get_my_project_none(self):
        self.client.login(user_id='foo2', password='fooPassword')
        response = self.client.get("/api/v1/project/me/")
        self.assertEqual(len(response.json()), 0)

    def test_get_project_list(self):
        response = self.client.get("/api/v1/project/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        
    def test_get_wrong_project(self):
        response = self.client.get("/api/v1/project/0/")
        self.assertEqual(response.status_code, 400)
        
class PutProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            user_id='foo',
            username='foo_test',
            email='foo@test.com',
            password='fooPassword',
        )
        cls.data = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.project = ProjectFactory(**cls.data)
        
    def setUp(self):
        self.client.login(user_id='foo', password='fooPassword')
        self.freezer = freeze_time("2022-02-22 00:00:00")
        self.freezer.start()
        
    def tearDown(self):
        self.freezer.stop()
        
    def test_update_project_title(self):
        id = Project.objects.get(title="title1").id
        data = {"title" : "title2"}
        response = self.client.put("/api/v1/project/" + str(id) + "/", data, content_type="application/json")
        self.assertEqual(response.json()["title"], "title2")
        
    def test_update_project_updated_at(self):
        id = Project.objects.get(title="title1").id
        data = {"title" : "title2"}
        self.client.put("/api/v1/project/" + str(id) + "/", data, content_type="application/json")
        project = Project.objects.get(title="title2")

        self.assertEqual(project.updated_at, datetime.datetime.strptime("2022-02-22 00:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc))
        
    def test_update_nothing(self):
        id = Project.objects.get(title="title1").id
        self.client.put("/api/v1/project/" + str(id) + "/", {}, content_type="application/json")
        project = Project.objects.get(title="title1")

        self.assertEqual(project.title, "title1")
        self.assertEqual(project.updated_at, datetime.datetime.strptime("2022-02-22 00:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc))
        
    def test_update_wrong_project(self):
        response = self.client.put("/api/v1/project/0/")
        self.assertEqual(response.status_code, 400)
        
    def test_update_project_writer(self):
        id = Project.objects.get(title="title1").id
        wrong_user = UserFactory(
            user_id='foo2',
            username='foo2_test',
            email='foo2@test.com',
            password='fooPassword',
        )
        self.client.put("/api/v1/project/" + str(id) + "/", {"writer" : wrong_user.id}, content_type="application/json")
        project = Project.objects.get(title="title1")
        self.assertNotEqual(project.writer, wrong_user)
        self.assertEqual(project.writer, self.user)        
        
class DeleteProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            user_id='foo',
            username='foo_test',
            email='foo@test.com',
            password='fooPassword',
        )
        cls.data = {
            "title" : "title1",
            "writer" : cls.user
        }
        cls.project = ProjectFactory(**cls.data)
        data = cls.data.copy()
        data.update({"title" : "title2"})
        ProjectFactory(**data)
        
    def setUp(self):
        self.client.login(user_id='foo', password='fooPassword')
        
    def test_delete_project(self):
        project = Project.objects.get(title="title2")
        response = self.client.delete("/api/v1/project/" + str(project.id) + "/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        response = self.client.get("/api/v1/project/" + str(project.id) + "/")
        self.assertEqual(response.status_code, 400)
        
    def test_delete_wrong_project(self):
        response = self.client.delete("/api/v1/project/0/")
        self.assertEqual(response.status_code, 400)