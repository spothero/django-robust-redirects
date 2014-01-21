from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from models import Redirect
import dynamic_urls


class RedirectModelForm(forms.ModelForm):
    class Meta:
        model = Redirect

    def clean(self):
        cleaned_data = super(RedirectModelForm, self).clean()

        if cleaned_data['is_partial'] and cleaned_data['uses_regex']:
            raise ValidationError('Redirect can not be partial and also a regular expression.')


class RedirectAdmin(admin.ModelAdmin):
    list_display = ['from_url', 'to_url', 'is_partial', 'uses_regex', 'site', 'status']
    form = RedirectModelForm

    def save_model(self, request, object, form, change):
        instance = form.save()
        # for sites that are not in debug mode reload
        # the dynamic urls, i'm not sure if this is the
        # best way though
        reload(dynamic_urls)
        return instance

admin.site.register(Redirect, RedirectAdmin)
