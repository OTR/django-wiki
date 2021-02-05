from django.test import TestCase

from wiki.conf import settings as wiki_settings
from wiki.forms import Group

from ..base import wiki_override_settings
from ..testdata.models import CustomGroup

class CustomGroupTests(TestCase):
    @wiki_override_settings(WIKI_GROUP_MODEL="auth.Group")
    def test_setting(self):
        self.assertEqual(wiki_settings.GROUP_MODEL, "auth.Group")

    def test_custom(self):
        self.assertEqual(Group, CustomGroup)
        self.assertEqual(wiki_settings.GROUP_MODEL, "testdata.CustomGroup")
