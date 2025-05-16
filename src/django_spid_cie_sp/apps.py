from django.apps import AppConfig


class DjangoSpidCieSpConfig(AppConfig):
    name = 'django_spid_cie_sp'
    label = 'django_spid_cie_sp'

    # ~ def ready(self):
        # ~ import djangosaml2.views
        # ~ from . client import get_saml_client as custom_get_saml_client

        # ~ djangosaml2.views.get_saml_client = custom_get_saml_client
