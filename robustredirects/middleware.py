from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone
from robustredirects.models import Redirect
from robustredirects.utils import replace_partial_url


class RedirectMiddleware(object):
    """
        Process the redirect patterns from redirects.dynamic_urls.
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            # No need to check for a redirect for non-404 responses.
            return response

        path = request.get_full_path()

        try:
            urlconf = 'robustredirects.dynamic_urls'
            redirect, args, kwargs = resolve(path, urlconf=urlconf)
            return redirect(request, **kwargs)
        except Resolver404:
            # No redirect was found. Try looking for a partial
            site_id = settings.SITE_ID
            db_filters = {
                'status': 1,
                'site': site_id,
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
