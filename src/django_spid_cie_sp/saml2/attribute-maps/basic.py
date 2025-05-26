_MAP = {
    "spidCode": "spidCode",
    "name": "name",
    "familyName": "familyName",
    "placeOfBirth": "placeOfBirth",
    "countyOfBirth": "countyOfBirth",
    "dateOfBirth": "dateOfBirth",
    "gender": "gender",
    "companyName": "companyName",
    "registeredOffice": "registeredOffice",
    "fiscalNumber": "fiscalNumber",
    "ivaCode": "ivaCode",
    "idCard": "idCard",
    "mobilePhone": "mobilePhone",
    "email": "email",
    "address": "address",
    "expirationDate": "expirationDate",
    "digitalAddress": "digitalAddress",
}

MAP = {
    "identifier": "urn:oasis:names:tc:SAML:2.0:attrname-format:basic",
    "fro": _MAP,
    "to": {v:k for k,v in _MAP.items()}
}
