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

##### HOSTNAME
Imposta una variabile *HOSTNAME* con il dominio di produzione
```
HOSTNAME = example.host.it
```

##### INSTALLED APPS
Nelle *INSTALLED_APPS* aggiungi
```
"djangosaml2",
"django_spid_cie_sp",
```

##### LOGIN/LOGOUT ENDPOINT
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

##### LOG
Gestione dei log degli accessi con SPID/CIE da conservare per almeno 24 mesi (DPCM 24 ottobre 2014, articolo 13, comma 2),.  
Inserisci o integra nel file settings del progetto.
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s' # formattazione personalizzabile
        },
    },
    'handlers': {
        'spid_cie_access_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/spid_cie/access.log',  # path personalizzabile ma la cartella di destinazione deve essere presente
            'when': 'midnight',       # rotazione ogni giorno a mezzanotte
            'interval': 1,            # ogni 1 giorno
            'backupCount': 730,       # conserva 730 file, cioè 2 anni circa
            'formatter': 'verbose',
        },
        'spid_cie_error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/spid_cie/error.log',  # path personalizzabile ma la cartella di destinazione deve essere presente
            'when': 'midnight',
            'interval': 1,
            'backupCount': 730,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'spid_cie.access': {
            'handlers': ['spid_cie_access_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'spid_cie.error': {
            'handlers': ['spid_cie_error_file'],
            'level': 'ERROR',
            'propagate': True, # progaghiamo gli errori anche ai log superiori (es: uWSGI) per migliore gestione
        },
    }
}
```

##### CERTIFICATO E METADATA
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

* **CIE_PROD** = *False/True* (default *False*)  
se *True* permette di autenticarsi all'ambiente di produzione dell'IdP CIE, altrimenti a quello di test;
* **SPID_PROD** = *False/True* (default *False*)  
se *True* viene mostrato l'elenco dei providers SPID cliccando sullo spid-button, altrimenti viene presa in considerazione la variabile seguente;
* **SPID_VALIDATION** = *False/True* (default *False*)  
ha effetto solo se SPID_PROD è *False*.  
Se *True* mostra il collegamento al [validator ufficiale di SPID](https://validator.spid.gov.it/) per permettere ad AgID di effettuare il collaudo del SP ([regole tecniche](https://www.spid.gov.it/cos-e-spid/diventa-fornitore-di-servizi/procedura-tecnica/)), altrimenti permette di testare l'autenticazione con l'IdP di test [https://demo.spid.gov.it/samlsso](https://demo.spid.gov.it/samlsso).

---

### Note

* l'applicazione si basa sul progetto [djangosaml2](https://github.com/IdentityPython/djangosaml2);
* l'implementazione dell'autenticazione con SPID è stata effettuata seguendo le [regole tecniche SPID](https://docs.italia.it/italia/spid/spid-regole-tecniche/it/stabile/index.html);
* l'implementazione dell'autenticazione con CIE è stata effettuata seguendo le [regole tecniche CIE eID SAML](https://docs.italia.it/italia/cie/cie-eid-saml-docs/it/versione-corrente/index.html);
* il pulsante "Accedi con SPID" è stato implementato utilizzando la libreria [spid-sp-access-button](https://github.com/italia/spid-sp-access-button);
* per le Pubbliche Amministrazioni si consiglia la generazione in autonomia del certificato con la libreria [spid-compliant-certificates](https://github.com/italia/spid-compliant-certificates).