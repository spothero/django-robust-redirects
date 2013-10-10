from django.core.management.base import BaseCommand, CommandError
from robustredirects.models import Redirect
from django.contrib.redirects.models import Redirect as DjangoRedirect
from django.db import transaction

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        with transaction.commit_on_success():
            count = 0
            for redirect in DjangoRedirect.objects.all():
                Redirect(from_url=redirect.old_path, to_url=redirect.new_path, site=redirect.site, http_status=301)
                count += 1

        print "Copied {} number of redirects into robust redirects."