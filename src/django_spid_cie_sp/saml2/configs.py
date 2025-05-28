import os
import saml2

from django.apps import apps
from django.conf import settings

from saml2.config import SPConfig


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COMMON_CONFIG = {
    "attribute_map_dir": f"{BASE_DIR}/attribute-maps",
    "authn_requests_signed": True,
    "signing_algorithm":  saml2.xmldsig.SIG_RSA_SHA256,
    "digest_algorithm":  saml2.xmldsig.DIGEST_SHA256,
    "xmlsec_binary": "/usr/bin/xmlsec1",
    "key_file": settings.KEY_FILE,
    "cert_file": settings.CERT_FILE,
    "encryption_keypairs": [{
        "key_file": settings.KEY_FILE,
        "cert_file": settings.CERT_FILE,
    }]
}
SP_COMMON_CONFIG = {
    "authn_requests_signed": True,
    "allow_unsolicited": True,
    "want_assertions_signed": True,
    "want_response_signed": True,
    "name_id_format": "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
    "signing_algorithm":  saml2.xmldsig.SIG_RSA_SHA256,
    "digest_algorithm":  saml2.xmldsig.DIGEST_SHA256,
}

def get_saml_config(request=None):
    # Analizza l"URL per capire se SPID o CIE
    path = request.path if request else ""
    config = {}
    if path.startswith(f"/{settings.SPID_SAML2_PREFIX}/"):
        config = {
            "entityid": getattr(settings, "SPID_SP_ENTITY_ID", f"https://{settings.HOSTNAME}/{settings.SPID_SAML2_PREFIX}/metadata/"),
            "service": {
                "sp": {
                    "endpoints": {
                        "assertion_consumer_service": [
                            (f"https://{settings.HOSTNAME}/{settings.SPID_SAML2_PREFIX}/acs/post/", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"),
                        ],
                        "single_logout_service": [
                            (f"https://{settings.HOSTNAME}/{settings.SPID_SAML2_PREFIX}/ls/post/", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"),
                        ],
                    },
                    "attribute_consumer_service_index": settings.SPID_SP_ATTRIBUTE_CONSUMER_SERVICE_INDEX,
                },
            },
            "metadata":  {
                "remote": [
                    {
                        "url": settings.SPID_ENTITIES_METADATA_URL if settings.SPID_PROD else settings.SPID_METADATA_URL_PREPROD
                    }
                ]
            },

        }
    elif path.startswith(f"/{settings.CIE_SAML2_PREFIX}/"):
        config = {
            "entityid": getattr(settings, "CIE_SP_ENTITY_ID", f"https://{settings.HOSTNAME}/{settings.CIE_SAML2_PREFIX}/metadata/"),
            "service": {
                "sp": {
                    "endpoints": {
                        "assertion_consumer_service": [
                            (f"https://{settings.HOSTNAME}/{settings.CIE_SAML2_PREFIX}/acs/post/", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"),
                        ],
                        "single_logout_service": [
                            (f"https://{settings.HOSTNAME}/{settings.CIE_SAML2_PREFIX}/ls/post/", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"),
                        ],
                    },
                    "attribute_consumer_service_index": settings.CIE_SP_ATTRIBUTE_CONSUMER_SERVICE_INDEX,
                },
            },
            "metadata": {
                "remote": [
                    {"url": settings.CIE_METADATA_URL_PROD if settings.CIE_PROD else settings.CIE_METADATA_URL_PREPROD},
                ],
            },
        }
    if config:
        config.update(COMMON_CONFIG)
        config["service"]["sp"].update(SP_COMMON_CONFIG)
        sp_config = SPConfig()
        sp_config.load(config)
        return sp_config
