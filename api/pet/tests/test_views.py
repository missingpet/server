"""Test cases for views."""

from django.test import tag
from rest_framework.test import APITestCase


class ApiTestCases(APITestCase):

    def setUp(self):
        pass

    @tag('create-user')
    def test_create_user(self):
        pass

    @tag("create-announcement")
    def test_create_announcement(self):
        pass

    @tag('retrieve-announcement')
    def test_retrieve_announcement(self):
        pass

    @tag('delete-announcement')
    def test_delete_announcement(self):
        pass

    @tag('all-announcements')
    def test_get_all_announcements(self):
        pass

    @tag('announcements-of-user')
    def test_get_announcements_of_user(self):
        pass

    @tag('feed-for-user')
    def test_get_feed_for_user(self):
        pass

    @tag('all-announcements-map')
    def test_get_all_announcements_map(self):
        pass

    @tag('feed_announcements-map-for-user')
    def test_get_feed_announcements_map_for_user(self):
        pass

    def tearDown(self):
        pass
