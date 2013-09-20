# ReviewBoard-Persona Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension

class RBPersona(Extension):
    def __init__(self, *args, **kwargs):
        super(RBPersona, self).__init__(*args, **kwargs)
