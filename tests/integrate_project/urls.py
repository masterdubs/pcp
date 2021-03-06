from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    ('^about/$', TemplateView.as_view(template_name='about.html')),
    # reverse url lookups
    (r'^', include('wsgiadmin.useradmin.urls')),
)

