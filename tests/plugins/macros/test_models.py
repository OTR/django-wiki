from django.test.testcases import TestCase

from wiki.models import Article
from wiki.models import ArticleRevision


class ArticleModelTest(TestCase):

    def test_cache(self):
        a = Article.objects.create()
        ArticleRevision.objects.create(article=a, title="test", content="# header")
        expected = """<h1 id="wiki-toc-header">header""" """.*</h1>"""
        # cached content does not exist yet. this will create it
        self.assertRegexpMatches(a.get_cached_content(), expected)
        # actual cached content test
        self.assertRegexpMatches(a.get_cached_content(), expected)
