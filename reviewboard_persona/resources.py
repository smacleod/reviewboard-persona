from datetime import datetime
import urllib2
import urllib

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import simplejson

from djblets.siteconfig.models import SiteConfiguration
from djblets.util.dates import get_tz_aware_utcnow
from djblets.webapi.decorators import webapi_response_errors, \
                                      webapi_request_fields
from djblets.webapi.errors import INVALID_FORM_DATA, WebAPIError

from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import WebAPIResource


LOGIN_FAILED = WebAPIError(104, "Authenticating with Persona failed",
                           http_status=401)


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
        except Exception, e:
            return LOGIN_FAILED.with_message("Could not verify assertion: %s"
                                             % e)

        if 'status' not in response or response['status'] != "okay":
            # The assertion could not be verified
            return LOGIN_FAILED


        email = response['email']

        try:
            user = User.objects.get(email=email)
        except User.MultipleObjectsReturned:
            return LOGIN_FAILED.with_message("Multiple user accounts exist "
                                             "with the provided email")
        except User.DoesNotExist:
            return LOGIN_FAILED.with_message("A user does not exist with "
                                             "the provided email")


        auth.login(request, user)

        if settings.USE_TZ:
            user.last_login = get_tz_aware_utcnow()
        else:
            user.last_login = datetime.now()

        user.save()

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
