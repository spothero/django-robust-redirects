from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import resolve, Resolver404
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone
from robustredirects.models import Redirect
from robustredirects.utils import ignored_url_paths, replace_partial_url

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # backwards compatibility for MIDDLEWARE_CLASSES
    MiddlewareMixin = object


class RedirectMiddleware(MiddlewareMixin):
    """
        Process the redirect patterns from redirects.dynamic_urls.
    """

    def try_resolve(self, path, request):
        urlconf = 'robustredirects.dynamic_urls'
        redirect, args, kwargs = resolve(path, urlconf=urlconf)
        return redirect(request, **kwargs)

    def process_response(self, request, response):
        if response.status_code != 404:
            # No need to check for a redirect for non-404 responses.
            return response

        if request.path.startswith(ignored_url_paths()):
            # Stop checking ignored urls
            return response

        path = request.get_full_path()
        try:
            return self.try_resolve(path, request)
        except Resolver404:
            pass

        # Try again by changing the slash
        try:
            # if not, check if adding/removing the trailing slash helps
            if path.endswith('/'):
                new_path = path[:-1]
            else:
                new_path = path + '/'

            return self.try_resolve(new_path, request)
        except Resolver404:
            pass

        current_site = get_current_site(request)

        # No regex redirect was found try a simple replace
        if path.startswith('/'):
            no_leading_slash_path = path[1:]
            leading_slash_path = path
        else:
            no_leading_slash_path = path
            leading_slash_path = '/' + path

        # Try looking for an exact match
        redirect = Redirect.objects.filter(
            Q(from_url__iexact=no_leading_slash_path) | Q(from_url__iexact=leading_slash_path),
            status=1,
            site=current_site).order_by('-pk').first()

        if redirect:
            if redirect.to_url == '':
                return HttpResponseGone()

            # Do a replace on the url and do a redirect
            path = replace_partial_url(path, redirect.from_url, redirect.to_url)

            if redirect.http_status == 301:
                return HttpResponsePermanentRedirect(path)
            elif redirect.http_status == 302:
                return HttpResponseRedirect(path)

        # Try looking for a true partial
        db_filters = {
            'status': 1,
            'site': current_site,
            'is_partial': True
        }

        redirects = Redirect.objects.filter(**db_filters)

        for redirect in redirects:
            if redirect.from_url in path:
                if redirect.to_url == '':
                    return HttpResponseGone()

                # Do a replace on the url and do a redirect
                path = replace_partial_url(path, redirect.from_url, redirect.to_url)

                if redirect.http_status == 301:
                    return HttpResponsePermanentRedirect(path)
                elif redirect.http_status == 302:
                    return HttpResponseRedirect(path)

        return response
