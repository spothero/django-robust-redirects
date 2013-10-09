from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

HTTP_STATUS_CHOICES = (
    (301, _('301 - Permanent Redirect')),
    (302, _('302 - Temporary Redirect')),
)

STATUS_CHOICES = (
    (True, _('Active')),
    (False, _('Inactive')),
)

uses_regex_helptext = _('Check if the From URL uses a regular expression. '
                        'If so, it will be moved to the top the URL '
                        'patterns and processed first')

from_url_helptext = _('Absolute path, excluding the domain. '
                      'Example: \'/about/\''
                      )

to_url_helptext = _('Absolute path or full domain. Example: '
                    'http://www.example.com'
                    )

is_partial_helptext = _('The From and To URL are partial. They will be used is they partially match any part of the'
                        ' url. Can not be a regular expressions.')


class Redirect(models.Model):
    site = models.ForeignKey(Site, related_name='robust_redirects')

    from_url = models.CharField(_('From URL'), max_length=255, unique=True,
                                db_index=True, help_text=from_url_helptext)

    to_url = models.CharField(_('To URL'), max_length=255,
                              db_index=True, help_text=to_url_helptext, blank=True)

    http_status = models.SmallIntegerField(_('HTTP Status'),
                                           choices=HTTP_STATUS_CHOICES,
                                           default=301)

    status = models.BooleanField(choices=STATUS_CHOICES, default=True)

    is_partial = models.BooleanField(_('Is a partial url'),
                                     default=False,
                                     help_text=is_partial_helptext)

    uses_regex = models.BooleanField(_('Uses Regular Expression'),
                                     default=False,
                                     help_text=uses_regex_helptext)

    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        unique_together = (('site', 'from_url'),)
        ordering = ('-uses_regex',)

    def __unicode__(self):
        return _("Redirect: %(from)s --> %(to)s") % {'from': self.from_url, 'to': self.to_url}

    def save(self, *args, **kwargs):
        # strip slashes from beginning, add slashes to the end
        # only if not a regex
        if not self.uses_regex and not self.is_partial:
            self.from_url = self.from_url.lstrip('/')
            try:
                if self.from_url[-1] != '/':
                    self.from_url += '/'
            except IndexError:
                pass

        if self.from_url == '':
            # user wants to catch '/'
            self.from_url = '^$'
            self.uses_regex = True

        super(Redirect, self).save(args, kwargs)
