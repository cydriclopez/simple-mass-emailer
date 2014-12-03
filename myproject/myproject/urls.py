
from django.conf.urls import patterns, include, url
from django.contrib import admin
from simple_mass_emailer.views import (EnrollFormView,
    EnrollSuccessTemplateView, EnrollCancelTemplateView,
    EnrollTest2TemplateView)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^enroll-email/', EnrollFormView.as_view(), name='enroll-email'),
    url(r'^enroll-email/(?P<md5hash>[-\w]+)/', EnrollFormView.as_view(), name='enroll-email'),
    url(r'^enroll-success/(?P<md5hash>[-\w]+)/', EnrollSuccessTemplateView.as_view(), name='enroll-success'),
    url(r'^enroll-cancel/(?P<md5hash>[-\w]+)/', EnrollCancelTemplateView.as_view(), name='enroll-cancel'),
    url(r'^enroll-form2/', EnrollTest2TemplateView.as_view(), name='enroll-form2'),
)
