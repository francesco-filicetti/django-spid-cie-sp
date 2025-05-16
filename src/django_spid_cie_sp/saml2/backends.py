from djangosaml2.backends import Saml2Backend

class CustomSaml2Backend(Saml2Backend):
    def authenticate(self, request, session_info=None, idp_entityid=None, **kwargs):
        if session_info and 'ava' in session_info:
            attributes = session_info['ava']
            if 'fiscalNumber' in attributes:
                attributes['fiscalNumber'] = [
                    v.replace('TINIT-', '') for v in attributes['fiscalNumber']
                ]
            # Aggiorna la session_info con gli attributi modificati
            session_info['ava'] = attributes

        return super().authenticate(
            request=request,
            session_info=session_info,
            idp_entityid=idp_entityid,
            **kwargs
        )
