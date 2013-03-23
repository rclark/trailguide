from django.conf.urls import patterns, url

urlpatterns = patterns('trailguide.api',
    url(r'^docs/(?P<doc_name>.*)$', 'docs'),
    url(r'^(?P<model_name>[^/]+)$', 'controllers.collection'),
    url(r'^(?P<model_name>[^/]+)/(?P<pk>\d+)/$', 'controllers.single')
)