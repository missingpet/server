"""Test cases for serializers."""
from django import test


class SerializersTestCases(test.TestCase):

    def setUp(self):
        pass

    @test.tag('announcement-serializer')
    def test_announcement_serializer(self):
        pass

    @test.tag('user-create-serializer')
    def test_user_create_serializer(self):
        pass

    def tearDown(self):
        pass
