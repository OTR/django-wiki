from ...base import TemplateTestCase


class PluginEnabled(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {% if "wiki.plugins.attachments"|plugin_enabled %}It is enabled{% endif %}
    """

    def test_true(self):
        output = self.render({})
        self.assertIn("It is enabled", output)
