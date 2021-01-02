from django.test import tag

from rest_framework.test import APITestCase


class ApiTestCases(APITestCase):
    def setUp(self):
        pass

    @tag("create-announcement")
    def test_create_announcement(self):
        pass

    def tearDown(self):
        pass
