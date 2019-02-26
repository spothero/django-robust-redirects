from django.conf import settings
from django.http import HttpResponseNotFound
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import clear_url_caches

from robustredirects.middleware import RedirectMiddleware
from robustredirects.models import Redirect


class TestRedirectMiddleWare(TestCase):
    def setUp(self):
        super(TestRedirectMiddleWare, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # tests should start with an empty url cache
        clear_url_caches()
        settings.ROBUST_REDIRECTS_IGNORED_URL_PATHS = None

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

        redirect = Redirect(from_url=r'test/(?P<pk>\d+)/', to_url=r'somethingelse/(?P<pk>\d+)/',
                            site=get_current_site(request), uses_regex=True)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 301)
        assert 'somethingelse' in new_response.serialize_headers()

    def test_redirect_request_gone(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url=r'test/(?P<pk>\d+)/', to_url='',
                            site=get_current_site(request), uses_regex=True)

        redirect.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 410)

    def test_redirect_request_temporary(self):
        # Create a redirect
        request = self.factory.get('/test/123/')

        redirect = Redirect(from_url=r'test/(?P<pk>\d+)/', to_url=r'somethingelse/(?P<pk>\d+)/',
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

    def test_redirect_request_two_partial_entries_permanent(self):
        # Create a redirect
        old_route = '/invalidroot/partialtest'
        redirected_route = '/test/partialtest'
        request = self.factory.get(old_route)

        redirect = Redirect(from_url='/invalidroot', to_url=redirected_route, is_partial=True,
                            site=get_current_site(request), http_status=301)

        redirect.save()
        redirect2 = Redirect(from_url=old_route, to_url=redirected_route, is_partial=True,
                             site=get_current_site(request), http_status=301)

        redirect2.save()
        new_response = self.run_redirect(request)

        self.assertEqual(new_response.status_code, 301)
        self.assertEqual(new_response.url, redirected_route)

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

    def test_redirect_exclusion(self):
        # Create a redirect
        request = self.factory.get('/api/test/123/')

        settings.ROBUST_REDIRECTS_IGNORED_PREFIXES = '/api'

        redirect = Redirect(from_url='/test/', to_url='partialtest/', is_partial=True,
                            site=get_current_site(request), http_status=302)

        redirect.save()
        redirect2 = Redirect(from_url=r'/api/test/(?P<pk>\d+)/', to_url=r'somethingelse/(?P<pk>\d+)/',
                             site=get_current_site(request), http_status=302, uses_regex=True)

        redirect2.save()
        new_response = self.run_redirect(request)

        # no redirect should happen
        self.assertEqual(new_response.status_code, 404)
