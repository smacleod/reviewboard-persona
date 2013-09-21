# ReviewBoard-Persona Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import TemplateHook

class RBPersona(Extension):
    def __init__(self, *args, **kwargs):
        super(RBPersona, self).__init__(*args, **kwargs)
        self.script_injection = TemplateHook(self, "base-scripts-post",
            template_name="reviewboard_persona/base.html")