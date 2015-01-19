from django.conf.urls import patterns, url, include

steel_patterns = patterns(
    'metal.views',
    url(r'^form/$', 'steel_form_view', name='steel_form'),
    url(r'^details/(?P<pk>\d+)/$', 'steel_detail_view', name='steel_details'),
    url(r'^update/(?P<pk>\d+)/$', 'steel_update_view', name='steel_update'),
)


urlpatterns = patterns(
    'metal.views',
    url('', include(steel_patterns)),
)
