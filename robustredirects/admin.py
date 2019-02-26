from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import clear_url_caches
from django import forms
from models import Redirect
from utils import ignored_url_paths


class RedirectModelForm(forms.ModelForm):
    class Meta:
        model = Redirect
        fields = ('site', 'from_url', 'to_url', 'http_status', 'status', 'is_partial',
                  'uses_regex',)

    def clean(self):
        cleaned_data = super(RedirectModelForm, self).clean()

        if cleaned_data['is_partial'] and cleaned_data['uses_regex']:
            raise ValidationError('Redirect cannot be partial and also a regular expression.')

        ignored_urls = ignored_url_paths()
        from_url = cleaned_data['from_url']
        ignored_prefix = next((u for u in ignored_urls if from_url.startswith(u)), None)
        if ignored_prefix is not None:
            raise ValidationError('Redirect matches ignored path: %s' % ignored_prefix)


class RedirectAdmin(admin.ModelAdmin):
    list_display = ['from_url', 'to_url', 'is_partial', 'uses_regex', 'site', 'status']
    form = RedirectModelForm

    def save_model(self, request, object, form, change):
        import dynamic_urls
        instance = form.save()
        # for sites that are not in debug mode reload
        # the dynamic urls, i'm not sure if this is the
        # best way though
        reload(dynamic_urls)
        clear_url_caches()
        return instance

admin.site.register(Redirect, RedirectAdmin)
