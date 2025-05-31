# CIE
# ~ CIE_SP_ENTITY_ID = "" override in django.conf.settings
CIE_SAML2_PREFIX = "cieSaml2"
CIE_SP_ATTRIBUTE_CONSUMER_SERVICE_INDEX = 0
CIE_SP_METADATA = ""
CIE_PROD = False
CIE_ENTITY_ID_PROD = "https://idserver.servizicie.interno.gov.it/idp/profile/SAML2/POST/SSO"
CIE_ENTITY_ID_PREPROD = "https://preproduzione.idserver.servizicie.interno.gov.it/idp/profile/SAML2/POST/SSO"
CIE_METADATA_URL_PROD = "https://idserver.servizicie.interno.gov.it/idp/shibboleth?Metadata"
CIE_METADATA_URL_PREPROD = "https://preproduzione.idserver.servizicie.interno.gov.it/idp/shibboleth?Metadata"

# SPID
# ~ SPID_SP_ENTITY_ID = "" override in django.conf.settings
SPID_SAML2_PREFIX = "spidSaml2"
SPID_SP_ATTRIBUTE_CONSUMER_SERVICE_INDEX = 0
SPID_SP_METADATA = ""
SPID_PROD = False
SPID_VALIDATION = False
SPID_ENTITIES_METADATA_URL = "https://registry.spid.gov.it/entities-idp"
SPID_ENTITY_ID_PREPROD = "https://demo.spid.gov.it"
SPID_METADATA_URL_PREPROD = "https://demo.spid.gov.it/metadata.xml"
SPID_URL_VALIDATION = "https://validator.spid.gov.it/"

# COMMON
KEY_FILE = ""
CERT_FILE = ""

# Django
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_URL = "/spid-cie/login/"
LOGOUT_URL = "/logout/"
SAML_CONFIG_LOADER = "django_spid_cie_sp.saml2.configs.get_saml_config"
SAML_USE_NAME_ID_AS_USERNAME = False
SAML_DJANGO_USER_MAIN_ATTRIBUTE = "taxpayer_id"
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = "__iexact"
SAML_CREATE_UNKNOWN_USER = True

SAML_ATTRIBUTE_MAPPING = {
    "name": ("first_name", ),
    "familyName": ("last_name", ),
    "fiscalNumber": ("taxpayer_id", "username"),
}

SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

AUTHENTICATION_BACKENDS = (
    # ~ "djangosaml2.backends.Saml2Backend",
    "django_spid_cie_sp.saml2.backends.CustomSaml2Backend",
    "django.contrib.auth.backends.ModelBackend",
)
