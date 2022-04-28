from django.contrib import admin
from django.urls import re_path
from django.http import HttpResponse
from django.views.generic import View


class TestView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse('Testing')


admin.autodiscover()

urlpatterns = [
    re_path(r'^partialtest/(?P<pk>\d+)/', TestView.as_view()),
    re_path(r'^admin/', admin.site.urls),
]
