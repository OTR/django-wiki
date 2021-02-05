import tempfile
from datetime import datetime

from django.test import TestCase
from wiki.core.http import send_file
from wiki.models import Article
from wiki.models import ArticleRevision
from wiki.models import URLPath


class URLPathTests(TestCase):
    def test_manager(self):

        root = URLPath.create_root()
        child = URLPath.create_urlpath(root, "child")

        self.assertEqual(root.parent, None)
        self.assertEqual(list(root.children.all().active()), [child])


class LineEndingsTests(TestCase):
    def test_manager(self):

        article = Article()
        article.add_revision(
            ArticleRevision(title="Root", content="Hello\nworld"), save=True
        )
        self.assertEqual("Hello\r\nworld", article.current_revision.content)


class HttpTests(TestCase):
    def test_send_file(self):
        fabricate_request = self.client.get("/").wsgi_request
        fobject = tempfile.NamedTemporaryFile("r")
        response = send_file(fabricate_request, fobject.name, filename="test.pdf")
        assert response.has_header("Content-Disposition")
        assert "inline" in response.get("Content-Disposition")
        response = send_file(fabricate_request, fobject.name, filename="test.jpeg")
        assert response.has_header("Content-Disposition")
        response = send_file(
            fabricate_request,
            fobject.name,
            filename="test.jpeg",
            last_modified=datetime.now(),
        )
        assert response.has_header("Content-Disposition")
        fobject.close()
