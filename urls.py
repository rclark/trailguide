from django.conf.urls import patterns, url, include

urlpatterns = patterns('trailguide.views',
    url(r'^/?$', 'home_page'),
    url(r'^map/', 'map_page'),
    url(r'^dashboard/', 'dashboard_page'),
    url(r'^route/(?P<route_slug>)/', 'route_page'),
    url(r'^api/', include('trailguide.api.urls')),
    url(r'^temp', 'temp')
)