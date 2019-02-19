from django.conf.urls import url
from django.conf import settings
from models import Redirect
from robustredirects import views


def ignored_url_paths():
    return getattr(settings, "ROBUST_REDIRECTS_IGNORED_PREFIXES", ())

def group_arguments(seq, group=254):
    """
        group the list into lists of 254 items each.

        This is due to argument restrictions in python.
        http://docs.djangoproject.com/en/dev/topics/http/urls/#patterns
    """
    return (seq[pos:pos + group] for pos in range(0, len(seq), group))


def get_redirect_patterns():
    """
        Gets the redirect patterns out of the database
        and assigns them to the django patterns object.
    """
    site_id = settings.SITE_ID
    url_patterns = []
    url_list = []
    db_filters = {
        'status': 1,
        'site': site_id,
        'is_partial': False,
        'uses_regex': True
    }

    redirects = Redirect.objects.filter(**db_filters)
    for redirect in redirects:
        extra = {}
        pattern = r'^%s$' % redirect.from_url

        extra.update({'url': '%s' % redirect.to_url})

        if redirect.http_status == 302:
            extra.update({'permanent': False})
            url_list.append(url(pattern, views.redirect_to, extra))
        else:
            url_list.append(url(pattern, views.redirect_to, extra))

    arg_groups = list(group_arguments(url_list))
    for args in arg_groups:
        url_patterns += list(args)

    return url_patterns


def replace_partial_url(starting_url, replace_from, replace_to):
    """
    Simple helper at this point. Maybe useful if we want to try supporting regex in the future.
    """
    new_url = starting_url.replace(replace_from, replace_to)

    if not new_url.startswith('/'):
        new_url = '/' + new_url

    return new_url
