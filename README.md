# Django SPID/CIE SAML2 Service Provider


### Generazione del certificato

Genera chiave e certificato in formato *.pem*.

Puoi utilizzare il tool [spid-compliant-certificates](https://github.com/italia/spid-compliant-certificates) o acquistarne uno presso una CA riconosciuta.

----

### Firma dei metadata

Configura i tuoi metadata per SPID e CIE partendo dai template in */saml2/metadata/* e firmali con il comando
```
xmlsec1 --sign --output tuo_path/metadata/metadata_signed.xml --privkey-pem /tuo_path/certificates//key.pem,/tuo_path/certificates//crt.pem --id-attr:ID EntityDescriptor tuo_path/metadata/metadata.xml
```
utilizzando chiave e certificato creati in precedenza.

----

### Installazione

```
pip install git+https://github.com/francesco-filicetti/django-spid-cie-sp.git
```

----

### Configurazione del file settings del progetto

Imposta una variabile *HOSTNAME* con il dominio di produzione
```
HOSTNAME = example.host.it
```

Nelle *INSTALLED_APPS* aggiungi
```
"djangosaml2",
"django_spid_cie_sp",
```

Definisci la gestione degli URL di login/logout

```
if 'django_spid_cie_sp' in INSTALLED_APPS:
    from django_spid_cie_sp.settings import *
    MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')
else:
    LOCAL_URL_PREFIX = 'local' # or choose another prefix
    LOGIN_URL = your_local_login_url
    LOGOUT_URL = your_local_logout_url
LOGOUT_REDIRECT_URL='/'
```

Infine imposta i path assoluti di metadata e certificati
```
CIE_SP_METADATA = 'tuo_path/metadata/metadata_cie_signed.xml'
SPID_SP_METADATA = '/tuo_path/metadata/metadata_spid_signed.xml'
KEY_FILE = "/tuo_path/certificates/key.pem"
CERT_FILE = "/tuo_path/certificates/crt.pem"
```

---

### Configurazione degli URL

Nel file *urls.py* del progetto gestisci i path per l'autenticazione
```
if "django_spid_cie_sp" in settings.INSTALLED_APPS:
    import django_spid_cie_sp.urls
    urlpatterns += (path("", include(django_spid_cie_sp.urls, "django_spid_cie_sp")),)

else:
    # local_url_prefix = 'local'
    urlpatterns += (
        path(
            LOGIN_URL,
            auth_views.LoginView.as_view(template_name="login.html"),
            name="login",
        ),
    )
    urlpatterns += (
        path(
            LOGOUT_URL,
            auth_views.LogoutView.as_view(
                template_name="logout.html", next_page=settings.LOGOUT_REDIRECT_URL),
            name="logout",
        ),
    )
```

---

### Switch ambienti prod/preprod di SPID/CIE

Per interfacciarsi con gli ambienti di produzione o test (default) degli IdP basta effettuare nel file di settings l'override delle variabili
```
CIE_PROD = False/True
SPID_PROD = False/True
```