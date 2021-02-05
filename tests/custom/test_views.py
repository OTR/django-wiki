from django.contrib.messages import constants
from django.shortcuts import resolve_url

from ..base import ArticleWebTestUtils
from ..base import DjangoClientTestBase
from ..base import RequireRootArticleMixin
from ..base import SUPERUSER1_USERNAME

from ..testdata.models import CustomGroup

class SettingsViewTests(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def test_change_group(self):
        group = CustomGroup.objects.create()
        response = self.client.post(
            resolve_url("wiki:settings", article_id=self.root_article.pk) + "?f=form0",
            {"group": group.pk, "owner_username": SUPERUSER1_USERNAME},
            follow=True,
        )
        self.root_article.refresh_from_db()
        self.assertEqual(self.root_article.group, group)
        self.assertEqual(self.root_article.owner, self.superuser1)
        self.assertEqual(len(response.context.get("messages")), 1)
        message = response.context.get("messages")._loaded_messages[0]
        self.assertEqual(message.level, constants.SUCCESS)
        self.assertEqual(
            message.message, "Permission settings for the article were updated."
        )
