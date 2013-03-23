from django.test import TestCase
from django.test.client import Client

class ApiDocsTestCase(TestCase):
    """Test functions that provide the API documents"""
    docs_url = "/api/docs/"

    def setUp(self):
        self.c = Client()

    def tearDown(self):
        pass

    def test_api_gets_proper_template(self):
        """Check that the function returns the UI when no file is specified"""
        response = self.c.get(self.docs_url)
        self.assertEqual(response.status_code, 200) # Got a response

        templates = [ template.name for template in response.templates ]
        self.assertEqual(templates, [ "trailguide/api/docs/swagger.html" ])

    def test_api_sets_proper_context(self):
        """Check that the function properly sets context"""
        response = self.c.get(self.docs_url)
        self.assertEqual(response.status_code, 200) # Got a response

        expected_host = "http://127.0.0.1:8000/api/"
        expected_discovery = expected_host.rstrip("/") + "/docs/api-docs.json"
        self.assertEqual(response.context.get("host"), expected_host)
        self.assertEqual(response.context.get("discovery"), expected_discovery)

    def test_swagger_doc_nulls(self):
        """Check that Swagger docs 404 when you request a non-existent doc"""
        response = self.c.get("%sgarbage" % self.docs_url)
        self.assertEqual(response.status_code, 404)

    def test_swagger_docs(self):
        """Check that Swagger docs return as expected"""
        docs = [
            "api-docs.json",
            "segment.json"
        ]

        for doc in docs:
            response = self.c.get("%s%s" % (self.docs_url, doc))
            self.assertEqual(response.status_code, 200)
            templates = [ template.name for template in response.templates ]
            self.assertEqual(templates, [ "trailguide/api/docs/%s" % doc ])