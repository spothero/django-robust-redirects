from django.core.management.base import BaseCommand, CommandError
from robustredirects.models import Redirect
from django.contrib.redirects.models import Redirect as DjangoRedirect


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        count = 0
        for redirect in DjangoRedirect.objects.all():
            Redirect.objects.create(from_url=redirect.old_path, to_url=redirect.new_path, site=redirect.site,
                                    http_status=301)
            count += 1

        print "Copied {} number of redirects into robust redirects."