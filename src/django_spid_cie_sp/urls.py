from django.urls import path

from djangosaml2 import views

from . views import *


app_name = "django_spid_cie_sp"


urlpatterns = [
    path('spid-cie/login/', login_choice, name='login_choice'),

    # SPID endpoints
    path('spidSaml2/metadata/', spid_metadata_view, name='spid_metadata_view'),
    path('spidSaml2/login/', MultiSPLoginView.as_view(), name='spid_saml2_login'),
    path('spidSaml2/acs/post/', MultiSPACSView.as_view(), name='spid_saml2_acs'),
    path('spidSaml2/ls/post/', LogoutView.as_view(), name='spid_saml2_logout'),

    # CIE endpoints
    path('cieSaml2/metadata/', cie_metadata_view, name='cie_metadata_view'),
    path('cieSaml2/login/', MultiSPLoginView.as_view(), name='cie_saml2_login'),
    path('cieSaml2/acs/post/', MultiSPACSView.as_view(), name='cie_saml2_acs'),
    path('cieSaml2/ls/post/', LogoutView.as_view(), name='cie_saml2_logout'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
