"""
Almost all test cases covers both tag calling and template using.
"""
from django.conf import settings as django_settings
from wiki.conf import settings
from wiki.models import Article
from wiki.models import ArticleRevision
from wiki.templatetags.wiki_tags import wiki_render

from ...base import TemplateTestCase

if not django_settings.configured:
    django_settings.configure()

# TODO manage plugins in template
class WikiRenderTest(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {% wiki_render article pc %}
    """

    def tearDown(self):
        from wiki.core.plugins import registry

        registry._cache = {}
        super().tearDown()

    keys = ["article", "content", "preview", "plugins", "STATIC_URL", "CACHE_TIMEOUT"]

    def test_called_with_preview_content_and_article_have_current_revision(self):
        article = Article.objects.create()
        ArticleRevision.objects.create(
            article=article, title="Test title", content="Some beauty test text"
        )

        content = (
            """This is a normal paragraph\n"""
            """\n"""
            """Headline\n"""
            """========\n"""
        )

        expected = (
            """(?s).*<p>This is a normal paragraph</p>\n"""
            """<h1 id="wiki-toc-headline">Headline"""
            """.*</h1>.*"""
        )

        # monkey patch
        from wiki.core.plugins import registry

        registry._cache = {"spam": "eggs"}

        output = wiki_render({}, article, preview_content=content)
        self.assertCountEqual(self.keys, output)
        self.assertEqual(output["article"], article)
        self.assertRegexpMatches(output["content"], expected)
        self.assertIs(output["preview"], True)
        self.assertEqual(output["plugins"], {"spam": "eggs"})
        self.assertEqual(output["STATIC_URL"], django_settings.STATIC_URL)
        self.assertEqual(output["CACHE_TIMEOUT"], settings.CACHE_TIMEOUT)

        output = self.render({"article": article, "pc": content})
        self.assertRegexpMatches(output, expected)
