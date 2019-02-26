from django.contrib import admin
from django.conf.urls import url, include
from django.http import HttpResponse
from django.views.generic import View


class TestView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse('Testing')


admin.autodiscover()

urlpatterns = [
    url(r'^partialtest/(?P<pk>\d+)/', TestView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
