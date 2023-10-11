import json
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Foo
from .serializers import FooSerializer
from .models import UploadedImage
from .serializers import UploadedImageSerializer

# tests for models

class FooModelTest(APITestCase):
    def setUp(self):
        self.foo = Foo.objects.create(
            title="Foo title",
            description="Foo description"
        )

    def test_foo(self):
        """"
        This test ensures that the foo created in the setup
        exists
        """
        self.assertEqual(self.foo.title, "Foo title")
        self.assertEqual(self.foo.description, "Foo description")
        self.assertEqual(str(self.foo), "Foo title - Foo description")

# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_foo(title="", description=""):
        """
        Create a record in the db
        :param title:
        :param description:
        :return:
        """
        if title != "" and description != "":
            Foo.objects.create(title=title, description=description)

    def make_a_request(self, kind="post", **kwargs):
        """
        Make a post request to create a record
        :param kind: HTTP VERB
        :return:
        """
        if kind == "post":
            return self.client.post(
                reverse(
                    "foo-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    def setUp(self):
        # add test data
        self.create_foo("foo bar 1", "bar description 1")
        self.create_foo("foo bar 2", "bar description 2")
        self.create_foo("foo bar 3", "bar description 3")
        self.create_foo("foo bar 4", "bar description 4")
        self.valid_data = {
            "title": "test title",
            "description": "test description"
        }
        self.invalid_data = {
            "title": "",
            "description": ""
        }
        self.valid_foo_id = 1
        self.invalid_foo_id = 100


class GetAllFooTest(BaseViewTest):

    def test_get_all_foo(self):
        """
        This test ensures that all records added in the setUp method
        exist when we make a GET request to the foo/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("foo-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Foo.objects.all()
        serialized = FooSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ImageApiTests(BaseViewTest):
    def setUp(self):
        self.client = APIClient()
        # Create a sample image for testing retrieval (you can use a fixture or create one)
        self.image = UploadedImage.objects.create(image='test-image.png')

        # Adjust the URL reversing based on your actual URL pattern structure
        self.upload_url = reverse('upload-image', kwargs={"version": "v1"})
        self.retrieve_url = reverse('retrieve-image', args=['v1', self.image.pk])


    def test_upload_image(self):
        # Create a sample image file for upload (you can use any image file)
        # Ensure the image file exists in your test directory or provide a valid file path
        image_file = open('static/test-image.png', 'rb')

        response = self.client.post(
            self.upload_url, 
            {'image': image_file}, 
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UploadedImage.objects.filter(image__isnull=False).exists())

    def test_retrieve_image(self):
        response = self.client.get(self.retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.image.pk)
        self.assertEqual('http://testserver/media/test-image.png', response.data['image'])
