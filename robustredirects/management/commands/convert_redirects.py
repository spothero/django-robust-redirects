from django.core.exceptions import ObjectDoesNotExist
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
                new_redirect = Redirect(from_url=redirect.old_path, to_url=redirect.new_path, site=redirect.site,
                                        http_status=301)
                new_redirect.fix_slashes()
                try:
                    Redirect.objects.get(from_url=new_redirect.from_url)
                    print("Redirect from {} already exists...skipping".format(redirect.old_path))
                except ObjectDoesNotExist:
                    redirect.save()
                    count += 1

        print("Copied {} redirects into robust redirects.".format(count))