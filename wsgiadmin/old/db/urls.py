from django.conf.urls.defaults import *
from wsgiadmin.old.db.views import DatabasesListView

urlpatterns = patterns('wsgiadmin.old.db.views',
    url(r'^add/(?P<dbtype>\w+)/$', 'add', name='db_add'),
    url(r'^show/(?P<dbtype>\w+)/$', DatabasesListView.as_view(), name='db_list'),
    url(r'^show/$', DatabasesListView.as_view(), name='db_list'),
    url(r'^rm/(?P<dbtype>\w+)/$', 'rm', name='db_remove'),
    url(r'^passwd/(?P<dbtype>\w+)/(?P<dbname>[a-zA-Z0-9\._\-]*)/$', 'passwd', name='db_passwd'),
)
