from django.conf.urls import patterns, url

urlpatterns = patterns('trailguide.api.controllers',
    url(r'^(?P<model_name>[^/]+)$', 'collection'),
    url(r'^(?P<model_name>[^/]+)/(?P<pk>\d+)/$', 'single')                        
)