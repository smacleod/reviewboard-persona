import urllib2
import urllib

from django.contrib.sites.models import Site
from django.utils import simplejson

from djblets.siteconfig.models import SiteConfiguration
from djblets.webapi.decorators import webapi_response_errors, \
                                      webapi_request_fields
from djblets.webapi.errors import INVALID_FORM_DATA

from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import WebAPIResource


class PersonaLoginResource(WebAPIResource):
    """Resource for logging in using Mozilla Persona.

    The provided assertion will be verified by contact a remote server.
    If the assertion is verified, the user should be logged in and a
    200 response be returned. In the event that the assertion cannot
    be verified, a 500 will be returned.
    """
    name = 'persona_login'
    allowed_methods = ('GET', 'POST',)

    VERIFICATION_URL = "https://verifier.login.persona.org/verify"

    @webapi_check_local_site
    @webapi_response_errors(INVALID_FORM_DATA)
    @webapi_request_fields(
        required={
            'assertion': {
                'type': str,
                'description': 'The login assertion to be verified.'
            },
        },
    )
    def create(self, request, assertion, *args, **kwargs):
        """Attempts to verify an assertion and login the user."""
        if not assertion:
            # The assertion was empty
            return INVALID_FORM_DATA, {
                'fields': {
                    'assertion': 'The assertion was empty',
                },
            }

        try:
            response = self.verify_assertion(assertion)

            if 'status' not in response or response['status'] != "okay":
                # The assertion could not be verified
                return 500, {}

            email = response.email

        except Exception, e:
            # There was a problem verifying the assertion
            return 500, {}

        return 200, {}

    def get_audience_url(self):
        """Return the domain and port of this Review Board instance."""
        protocol = SiteConfiguration.objects.get_current().get("site_domain_method")
        domain = Site.objects.get_current().domain
        return '%s://%s' % (protocol, domain)

    def  verify_assertion(self, assertion):
        """Make an assertion verification request and return the response."""
        fields = {
            'assertion': assertion,
            'audience': self.get_audience_url(),
        }

        u = urllib2.urlopen(self.VERIFICATION_URL, urllib.urlencode(fields))
        rsp = u.read()

        return simplejson.loads(rsp)

persona_login_resource = PersonaLoginResource()
