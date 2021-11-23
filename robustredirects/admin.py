from django import forms
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.urls import clear_url_caches
from six.moves import reload_module

from robustredirects.models import Redirect
from robustredirects.utils import ignored_url_paths


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
    form = RedirectModelForm
    list_display = ['from_url', 'to_url', 'is_partial', 'uses_regex', 'site', 'status', 'edit']
    readonly_fields = ["edit"]
    change_list_template = "change_form.html"

    def save_model(self, request, object, form, change):
        from robustredirects import dynamic_urls
        instance = form.save()
        # for sites that are not in debug mode reload
        # the dynamic urls, i'm not sure if this is the
        # best way though
        reload_module(dynamic_urls)
        clear_url_caches()
        return instance

    def logs(self, **filters):
        content_type = ContentType.objects.get_for_model(self.model)
        return LogEntry.objects.filter(content_type=content_type, **filters).order_by('-pk')

    def edit(self, obj):
        log = self.logs(object_id=obj.id).first()
        return "{} ({})".format(log.action_time.strftime("%Y-%m-%d %H:%M %Z"), log.user)

    def history(self):
        return [{
            "description": log,
            "id": log.object_id,
            "user": log.user,
            "time": log.action_time.strftime("%Y-%m-%d %H:%M %Z"),
        } for log in self.logs()[:20]]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["history"] = self.history
        return super(RedirectAdmin, self).changelist_view(request, extra_context)


admin.site.register(Redirect, RedirectAdmin)
