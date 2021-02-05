from wiki.conf import settings as wiki_settings
from wiki.models import reverse

from ..base import RequireRootArticleMixin
from ..base import TestBase
from ..base import wiki_override_settings
from ..testdata.models import CustomUser

class SignupViewTests(RequireRootArticleMixin, TestBase):
    @wiki_override_settings(ACCOUNT_HANDLING=True, ACCOUNT_SIGNUP_ALLOWED=True)
    def test_signup(self):
        response = self.client.post(
            wiki_settings.SIGNUP_URL,
            data={
                "password1": "wiki",
                "password2": "wiki",
                "username": "wiki",
                "email": "wiki@wiki.com",
            },
        )
        self.assertIs(CustomUser.objects.filter(email="wiki@wiki.com").exists(), True)
        self.assertRedirects(response, reverse("wiki:login"))
