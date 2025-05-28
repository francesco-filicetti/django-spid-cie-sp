from django.conf import settings
from django.urls import path

from djangosaml2 import views

from . views import *


app_name = "django_spid_cie_sp"


urlpatterns = [
    path('spid-cie/login/', login_choice, name='login_choice'),

    # SPID endpoints
    path(f'{settings.SPID_SAML2_PREFIX}/metadata/', spid_metadata_view, name='spid_metadata_view'),
    path(f'{settings.SPID_SAML2_PREFIX}/login/', MultiSPLoginView.as_view(), name='spid_saml2_login'),
    path(f'{settings.SPID_SAML2_PREFIX}/acs/post/', MultiSPACSView.as_view(), name='spid_saml2_acs'),
    path(f'{settings.SPID_SAML2_PREFIX}/ls/post/', LogoutView.as_view(), name='spid_saml2_logout'),

    # CIE endpoints
    path(f'{settings.CIE_SAML2_PREFIX}/metadata/', cie_metadata_view, name='cie_metadata_view'),
    path(f'{settings.CIE_SAML2_PREFIX}/login/', MultiSPLoginView.as_view(), name='cie_saml2_login'),
    path(f'{settings.CIE_SAML2_PREFIX}/acs/post/', MultiSPACSView.as_view(), name='cie_saml2_acs'),
    path(f'{settings.CIE_SAML2_PREFIX}/ls/post/', LogoutView.as_view(), name='cie_saml2_logout'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
