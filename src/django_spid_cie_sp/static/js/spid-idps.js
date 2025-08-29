// * spid-idps.js *
// This script populate the SPID button with a remote json or the `idps` var content
//var queryURL = "js/JSON_IDP_list_EXAMPLE.json";
var queryURL = "https://registry.spid.gov.it/entities-idp?&output=json&custom=info_display_base";
var idps = [{"entity_id":"https://spid.teamsystem.com/idp","organization_name":"TeamSystem s.p.a.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-teamsystemid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fspid.teamsystem.com%2Fidp?output=json"},{"entity_id":"https://loginspid.aruba.it","organization_name":"ArubaPEC S.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-arubaid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Floginspid.aruba.it?output=json"},{"entity_id":"https://identity.infocert.it","organization_name":"InfoCert S.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-infocertid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fidentity.infocert.it?output=json"},{"entity_id":"https://posteid.poste.it","organization_name":"Poste Italiane SpA","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-posteid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fposteid.poste.it?output=json"},{"entity_id":"https://idp.intesigroup.com","organization_name":"Intesi Group S.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-intesigroupspid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fidp.intesigroup.com?output=json"},{"entity_id":"https://id.eht.eu","organization_name":"EtnaHitech S.C.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-etnaid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fid.eht.eu?output=json"},{"entity_id":"https://loginspid.infocamere.it","organization_name":"InfoCamere S.C.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-infocamereid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Floginspid.infocamere.it?output=json"},{"entity_id":"https://idp.namirialtsp.com/idp","organization_name":"Namirial","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-namirialid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fidp.namirialtsp.com%2Fidp?output=json"},{"entity_id":"https://id.lepida.it/idp/shibboleth","organization_name":"Lepida S.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-lepidaid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fid.lepida.it%2Fidp%2Fshibboleth?output=json"},{"entity_id":"https://spid.register.it","organization_name":"Register.it S.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-spiditalia.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fspid.register.it?output=json"},{"entity_id":"https://identity.sieltecloud.it","organization_name":"Sielte S.p.A.","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-sielteid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Fidentity.sieltecloud.it?output=json"},{"entity_id":"https://login.id.tim.it/affwebservices/public/saml2sso","organization_name":"TI Trust Technologies srl","logo_uri":"https://cdn.jsdelivr.net/gh/italia/spid-sp-access-button/src/production/img/spid-idp-timid.svg","registry_link":"https://registry.spid.gov.it/entities-idp/https%3A%2F%2Flogin.id.tim.it%2Faffwebservices%2Fpublic%2Fsaml2sso?output=json"}]
// spid_populate function, if '.spid-button[data-spid-remote] ul' exist, try to get the remote json file and pupulate all spid buttons
function spid_populate() {
    let spid_elements = document.querySelectorAll('ul[data-spid-remote]')
    if (spid_elements.length > 0 ) {
        if (spid_prod) {
            fetch(queryURL)
                .then(function (response) {
                    return response.json();
                })
                .then(function (idps) {
                    idps = idps.sort(() => Math.random() - 0.5)
                    for (var u = 0; u < spid_elements.length; u++) {
                        for (var i = 0; i < idps.length; i++) { spid_addIdpEntry(idps[i], spid_elements[u]); }
                    }
                })
                .catch(function (error) {
                    console.log('Error during fetch: ' + error.message);
                    idps.sort(() => Math.random() - 0.5)
                    for (var u = 0; u < spid_elements.length; u++) {
                        for (var i = 0; i < idps.length; i++) { spid_addIdpEntry(idps[i], spid_elements[u]); }
                    }
                });
        }
        else if (spid_validation) {
            let li = document.createElement('li');
            li.className = 'spid-idp-button-link';
            li.innerHTML = `<a href="` + spid_url_validation + `" target="_blank" style="text-align: center; padding: 15px 0; font-size: 1.2rem;">
                                <span>SPID Validator</span>
                            </a>`
            spid_elements[0].prepend(li)
        }
        else { // not prod & not validation
            const att = document.createAttribute("data-idp");
            att.value = spid_entity_id_preprod;
            let li = document.createElement('li');
            li.className = 'spid-idp-button-link';
            li.setAttributeNode(att);
            li.innerHTML = `<form method="get" action="` + spid_login_url + `">
                                <input type="hidden" name="idp" value="` + spid_entity_id_preprod + `">
                                <button type="submit" class="idp-button-idp-logo" name="Demo SPID Validator" type="submit" style="background: #333; text-align: center;">
                                    <span class="spid-sr-only">Demo SPID Validator</span>
                                    <img class="spid-idp-button-logo" src="https://demo.spid.gov.it/img/idp-logo.png" alt="Demo SPID Validator" />
                                </button>
                            </form>`
            spid_elements[0].prepend(li)
        }
    }
}

// function spid_addIdpEntry make a "li" element with the ipd link and prepend this in a element
//
// options:
// - data - is an object with "organization_name", "entity_id" and "logo_uri" values
// - element - is the element where is added the new "li" element
function spid_addIdpEntry(data, element) {
    const att = document.createAttribute("data-idp");
    att.value = data['entity_id'];
    let li = document.createElement('li');
    li.className = 'spid-idp-button-link';
    li.setAttributeNode(att);
    li.innerHTML = `<form method="get" action="` + spid_login_url + `">
                        <input type="hidden" name="idp" value="${data['entity_id']}">
                        <button type="submit" class="idp-button-idp-logo" name="${data['organization_name']}" type="submit">
                            <span class="spid-sr-only">${data['organization_name']}</span>
                            <img class="spid-idp-button-logo" src="${data['logo_uri']}" alt="${data['organization_name']}" />
                        </button>
                      </form>`
    element.prepend(li)
}

// when page is ready populate all spid buttons
document.onreadystatechange = function () {
    if (document.readyState == "interactive") {
        spid_populate()
    }
}

