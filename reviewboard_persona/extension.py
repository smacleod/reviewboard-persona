# ReviewBoard-Persona Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import TemplateHook

from reviewboard_persona.resources import (persona_login_resource,
                                           persona_logout_resource)

class RBPersona(Extension):

    metadata = {
        'Name': 'Review Board Persona',
        'Author': 'Steven MacLeod, Mike Conley',
    }

    resources = [
        persona_login_resource,
        persona_logout_resource,
    ]

    def __init__(self, *args, **kwargs):
        super(RBPersona, self).__init__(*args, **kwargs)
        self.script_injection = TemplateHook(self, "base-scripts-post",
            template_name="reviewboard_persona/base.html")