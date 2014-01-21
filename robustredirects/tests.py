from django.http import HttpResponseNotFound
from django.test import TestCase
from django.test.client import RequestFactory
from robustredirects.middleware import RedirectMiddleware
from robustredirects.models import Redirect
from django.contrib.sites.models import get_current_site

class TestRedirectMiddleWare(TestCase):
    def setUp(self):
        super(TestRedirectMiddleWare, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @staticmethod
    def run_redirect(request):
        import dynamic_urls

        reload(dynamic_urls)
        middleware = RedirectMiddleware()
        response = HttpResponseNotFound()
        new_response = middleware.process_response(request, response)
        return new_response

    def test_redirect_request_permanent(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='test/(?P<pk>\d+)/', to_url='somethingelse/(?P<pk>\d+)/',
                            site=get_current_site(request), uses_regex=True)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 301)
        assert 'somethingelse' in new_response.serialize_headers()

    def test_redirect_request_gone(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='test/(?P<pk>\d+)/', to_url='',
                            site=get_current_site(request), uses_regex=True)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 410)

    def test_redirect_request_temporary(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='test/(?P<pk>\d+)/', to_url='somethingelse/(?P<pk>\d+)/',
                            site=get_current_site(request), http_status=302, uses_regex=True)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 302)
        assert 'somethingelse' in new_response.serialize_headers()

    def test_redirect_request_partial_temporary(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='/test/', to_url='/partialtest/', is_partial=True,
                            site=get_current_site(request), http_status=302)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 302)
        assert 'partialtest' in new_response.serialize_headers()

    def test_redirect_request_partial_permanent(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='/test/', to_url='/partialtest/', is_partial=True,
                            site=get_current_site(request), http_status=301)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 301)
        assert 'partialtest' in new_response.serialize_headers()

    def test_redirect_request_partial_gone(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='/test/', to_url='', is_partial=True,
                            site=get_current_site(request), http_status=301)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 410)

    def test_redirect_request_partial_prepend_slash(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url='/test/', to_url='partialtest/', is_partial=True,
                            site=get_current_site(request), http_status=302)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 302)
        assert '/partialtest/123/' in new_response.serialize_headers()
