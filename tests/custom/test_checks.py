from django.core.checks import Error
from django.core.checks import registry
from django.test import TestCase

from wiki.checks import FIELDS_IN_CUSTOM_USER_MODEL
from wiki.checks import Tags

from ..base import wiki_override_settings


def _remove(settings, arg):
    return [setting for setting in settings if not setting.startswith(arg)]


class CheckTests(TestCase):

    def test_custom_user_model_mitigation_required(self):
        """
        Django check django.forms.ModelForm.Meta on definition, and raises an error if Meta.fields don't exist in Meta.model.
        This causes problems in wiki.forms.UserCreationForm and wiki.forms.UserUpdateForm when a custom user model doesn't have fields django-wiki assumes.
        There is some code in wiki.forms that detects this situation.
        This check asserts that Django are still raising an exception on definition, and asserts the mitigation code in wiki.forms,
        and that test_check_for_fields_in_custom_user_model below are required.
        """
        from django.core.exceptions import FieldError
        from django import forms
        from ..testdata.models import VeryCustomUser

        with self.assertRaisesRegex(
            FieldError,
            "Unknown field\\(s\\) \\((email|username|, )+\\) specified for VeryCustomUser",
        ):

            class UserUpdateForm(forms.ModelForm):
                class Meta:
                    model = VeryCustomUser
                    fields = ["username", "email"]

    def test_check_for_fields_in_custom_user_model(self):
        from django.contrib.auth import get_user_model

        with wiki_override_settings(
            WIKI_ACCOUNT_HANDLING=False, AUTH_USER_MODEL="testdata.VeryCustomUser"
        ):
            errors = registry.run_checks(tags=[Tags.fields_in_custom_user_model])
            self.assertEqual(errors, [])
        with wiki_override_settings(
            WIKI_ACCOUNT_HANDLING=True, AUTH_USER_MODEL="testdata.VeryCustomUser"
        ):
            errors = registry.run_checks(tags=[Tags.fields_in_custom_user_model])
            expected_errors = [
                Error(
                    "%s.%s.%s refers to a field that is not of type %s"
                    % (
                        get_user_model().__module__,
                        get_user_model().__name__,
                        field_fetcher,
                        required_field_type,
                    ),
                    hint="If you have your own login/logout views, turn off settings.WIKI_ACCOUNT_HANDLING",
                    obj=get_user_model(),
                    id="wiki.%s" % error_code,
                )
                for check_function_name, field_fetcher, required_field_type, error_code in FIELDS_IN_CUSTOM_USER_MODEL
            ]
            self.assertEqual(errors, expected_errors)
        with wiki_override_settings(WIKI_ACCOUNT_HANDLING=True):
            errors = registry.run_checks(tags=[Tags.fields_in_custom_user_model])
            self.assertEqual(errors, [])
