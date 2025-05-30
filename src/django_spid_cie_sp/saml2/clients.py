# custom_saml_client.py
from django.conf import settings

from saml2.client import Saml2Client
from saml2.saml import Issuer


class CIESaml2Client(Saml2Client):
    def create_authn_request(self, *args, **kwargs):
        issuer = Issuer(
            name_qualifier=getattr(settings, "CIE_SP_ENTITY_ID", f"https://{settings.HOSTNAME}/{settings.CIE_SAML2_PREFIX}/metadata/"),
            format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity",
            text=getattr(settings, "CIE_SP_ENTITY_ID", f"https://{settings.HOSTNAME}/{settings.CIE_SAML2_PREFIX}/metadata/")
        )
        req_id, req = super().create_authn_request(issuer=issuer, *args, **kwargs)
        return req_id, req


class SPIDSaml2Client(Saml2Client):
    def create_authn_request(self, *args, **kwargs):
        issuer = Issuer(
            name_qualifier=getattr(settings, "SPID_SP_ENTITY_ID", f"https://{settings.HOSTNAME}/{settings.SPID_SAML2_PREFIX}/metadata/"),
            format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity",
            text=getattr(settings, "SPID_SP_ENTITY_ID", f"https://{settings.HOSTNAME}/{settings.SPID_SAML2_PREFIX}/metadata/")
        )
        req_id, req = super().create_authn_request(issuer=issuer, *args, **kwargs)
        return req_id, req
