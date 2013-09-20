from django.conf.urls.defaults import patterns, url

from reviewboard_persona.extension import RBPersona


urlpatterns = patterns('reviewboard_persona.views',
    url(r'^$', 'configure'),
)
