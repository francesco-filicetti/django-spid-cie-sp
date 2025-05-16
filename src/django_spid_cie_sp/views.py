import os

from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from djangosaml2.views import LoginView, AssertionConsumerServiceView

from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import AuthnContextClassRef
from saml2.samlp import NameIDPolicy
from saml2.samlp import RequestedAuthnContext

from .saml2.clients import *
from .saml2.configs import get_saml_config


def cie_metadata_view(request):
    if not CIE_SP_METADATA or not os.path.exists(settings.CIE_SP_METADATA):
        raise Http404("Il file dei metadati CIE non è stato trovato.")
    return FileResponse(open(settings.CIE_SP_METADATA, "rb"), content_type="application/samlmetadata+xml")


def spid_metadata_view(request):
    if not SPID_SP_METADATA or not os.path.exists(settings.SPID_SP_METADATA):
        raise Http404("Il file dei metadati CIE non è stato trovato.")
    return FileResponse(open(settings.SPID_SP_METADATA, "rb"), content_type="application/samlmetadata+xml")


def login_choice(request):
    if request.user.is_authenticated:
        return redirect(request.path)
    return render(request, "spid_cie_login.html")


class MultiSPMixin:
    def get_saml_client(self, request):
        if request.path.startswith('/spidSaml2/'):
            config = get_saml_config(request)
            return SPIDSaml2Client(config)
        elif request.path.startswith('/cieSaml2/'):
            config = get_saml_config(request)
            return CIESaml2Client(config)
        else:
            raise Exception("SP non riconosciuto")

@method_decorator(csrf_exempt, name='dispatch')
class MultiSPLoginView(MultiSPMixin, LoginView):
    def get(self, request, *args, **kwargs):
        # Costruisci manualmente il client SAML
        saml_client = self.get_saml_client(request)
        # Recupera l'IdP selezionato
        idp_entity_id = request.GET.get('idp', None)
        if not idp_entity_id:
            return self.handle_error(request, 'Missing idp parameter')

        name_id_policy = NameIDPolicy(
            format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
        )

        requested_authn_context = RequestedAuthnContext(
            authn_context_class_ref=[AuthnContextClassRef(text="https://www.spid.gov.it/SpidL2")],
            comparison="minimum"
        )

        # Genera la AuthnRequest con l’index
        session_id, info = saml_client.prepare_for_authenticate(
            entityid=idp_entity_id,
            relay_state=request.GET.get('next', '/'),
            binding=BINDING_HTTP_POST,
            attribute_consuming_service_index="0",
            force_authn=True,
            name_id_policy=name_id_policy,
            requested_authn_context=requested_authn_context,
        )

        # Salva sessione
        if 'SAMLRequestID' not in request.session:
            request.session['SAMLRequestID'] = {}

        request.session['SAMLRequestID'][session_id] = {
            'entity_id': idp_entity_id
        }

        return HttpResponse(info['data'], content_type='text/html')

@method_decorator(csrf_exempt, name='dispatch')
class MultiSPACSView(MultiSPMixin, AssertionConsumerServiceView):
    pass


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def get(self, request):
        # Logout locale Django
        django_logout(request)

        # Pulisce eventuali riferimenti a SAML
        request.session.flush()

        # Reindirizza alla pagina iniziale
        return redirect(settings.LOGOUT_REDIRECT_URL)
