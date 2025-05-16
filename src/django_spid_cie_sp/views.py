import base64
import datetime
import html
import json
import logging
import os
import re
import xml.etree.ElementTree as ET

from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from djangosaml2.views import LoginView, AssertionConsumerServiceView

from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.response import StatusError, StatusAuthnFailed, UnsolicitedResponse
from saml2.saml import AuthnContextClassRef, NAMEID_FORMAT_TRANSIENT
from saml2.samlp import NameIDPolicy, RequestedAuthnContext
from saml2.s_utils import deflate_and_base64_encode, UnsupportedBinding


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


access_logger = logging.getLogger('spid_cie.access')
error_logger = logging.getLogger('spid_cie.error')


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


class MultiSPLoginView(MultiSPMixin, LoginView):
    def get(self, request, *args, **kwargs):
        # Costruisci manualmente il client SAML
        try:
            saml_client = self.get_saml_client(request)
        except Exception as e:
            return TemplateResponse(
                request=request,
                template="spid_cie_error.html",
                context={"error_msg": e},
                status=400
            )

        # Recupera l'IdP selezionato
        idp_entity_id = request.GET.get('idp', None)
        if not idp_entity_id:
            error_logger.warning(
                f"LoginView chiamata senza parametro 'idp' | "
                f"path={request.path} | "
                f"ip={request.META.get('REMOTE_ADDR')}"
            )
            return self.handle_error(request, 'IdP mancante')

        name_id_policy = NameIDPolicy(
            format=NAMEID_FORMAT_TRANSIENT,
        )

        requested_authn_context = RequestedAuthnContext(
            authn_context_class_ref=[
                AuthnContextClassRef(
                    text="https://www.spid.gov.it/SpidL2"
                )
            ],
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

        # salva authn_request in sessione (per logging in ACS)
        if info.get("data", None):
            saml_request_match = re.search(
                r'name=["\']SAMLRequest["\']\s+value=["\'](.*?)["\']',
                info['data']
            )
            if saml_request_match:
                saml_request_encoded = saml_request_match.group(1)
                saml_request = html.unescape(saml_request_encoded)
            else:
                saml_request = ""
            request.session['SAMLRequest'] = saml_request
        else:
            request.session['SAMLRequest'] = ""

        request.session.modified = True
        return HttpResponse(
            info['data'],
            content_type='text/html'
        )


@method_decorator(csrf_exempt, name='dispatch')
class MultiSPACSView(MultiSPMixin, AssertionConsumerServiceView):

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if request.user.is_authenticated:
                user = request.user
                saml_client = self.get_saml_client(request)

                # recupero dati per il log da authn_response e authn_request in sessione
                authn_request = request.session.get("SAMLRequest", "")
                authn_request_xml = base64.b64decode(authn_request) if authn_request else None
                authn_request_root = ET.fromstring(authn_request_xml) if authn_request_xml else None

                authn_response = saml_client.parse_authn_request_response(
                    xmlstr=request.POST.get('SAMLResponse', ''),
                    binding=BINDING_HTTP_POST,
                )

                # log accesso
                log_record = {
                    "event": "spid_cie_login",
                    "user_id": getattr(user, settings.SAML_DJANGO_USER_MAIN_ATTRIBUTE, "N/A"),
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "AuthnReq_ID": authn_response.in_response_to,
                    "AuthnReq_IssueInstant": authn_request_root.attrib.get("IssueInstant") if authn_request_root else "N/A",
                    "Response_ID": authn_response.response.id,
                    "Response_IssueInstant": str(authn_response.response.issue_instant),
                    "Response_Issuer": authn_response.issuer(),
                    "Assertion_ID": authn_response.assertion.id,
                    "Assertion_Subject": getattr(authn_response.assertion.subject.name_id, 'text', 'N/A'),
                    "Assertion_NameQualifier": getattr(authn_response.assertion.subject.name_id, 'name_qualifier', 'N/A'),
                    "SP_EntityID": saml_client.config.entityid,
                    "IdP_EntityID": authn_response.issuer(),
                    "esito": "successo",
                    "livello_spid": authn_response.authn_info()[0][0] if authn_response.authn_info() else "N/A",
                    "ip": request.META.get("REMOTE_ADDR"),
                    "saml_response": request.POST.get('SAMLResponse'),
                    "authn_request": authn_request or "N/A",
                }
                access_logger.info(json.dumps(log_record))
            else:
                error_logger.warning(
                    f"ACS POST senza utente autenticato | "
                    f"path={request.path} | "
                    f"ip={request.META.get('REMOTE_ADDR')} | "
                    f"SAMLResponse={request.POST.get('SAMLResponse', '')[:100]}"
                )

            return response

        except (StatusError, StatusAuthnFailed, UnsolicitedResponse, UnsupportedBinding) as saml_error:
            # log errore SAML

            error_logger.error(
                f"Errore SAML durante ACS POST | "
                f"request_path={request.path} | "
                f"ip={request.META.get('REMOTE_ADDR')} | "
                f"messaggio={str(saml_error)} | "
                f"saml_response_trunc={request.POST.get('SAMLResponse', '')[:100]}",
                exc_info=True
            )
            return TemplateResponse(
                request=request,
                template="spid_cie_error.html",
                context={"error_msg": "Errore di autenticazione SAML."},
                status=400
            )

        except Exception as e:
            # log errore generico
            error_logger.error(
                f"Errore generico in ACS POST | "
                f"request_path={request.path} | "
                f"messaggio={str(e)}",
                exc_info=True
            )
            return TemplateResponse(
                request=request,
                template="spid_cie_error.html",
                context={"error_msg": "Errore interno del server."},
                status=500
            )


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def get(self, request):
        # Logout locale Django
        django_logout(request)

        # Pulisce eventuali riferimenti a SAML
        request.session.flush()

        # Reindirizza alla pagina iniziale
        return redirect(settings.LOGOUT_REDIRECT_URL)
