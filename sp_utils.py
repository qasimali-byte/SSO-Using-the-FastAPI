from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
import saml2

BASE_URL = 'http://localhost:8088'

SAML_LOGIN_SETTINGS = {
                        # 'METADATA_AUTO_CONF_URL': 'https://idp.testshib.org/idp/shibboleth',
                       'METADATA_LOCAL_FILE_PATH': 'idp/metadata/ez_login_sp.xml',
                    #    'ENTITY_ID': 'https://idp.testshib.org/idp/shibboleth',
                       'DEFAULT_NEXT_URL': '/',
                    #    'NAME_ID_FORMAT': 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',

                       }

def _get_metadata():
    if 'METADATA_LOCAL_FILE_PATH' in SAML_LOGIN_SETTINGS:
        return {
            'local': [SAML_LOGIN_SETTINGS['METADATA_LOCAL_FILE_PATH']]
        }
    else:
        return {
            'remote': [
                {
                    "url": SAML_LOGIN_SETTINGS['METADATA_AUTO_CONF_URL'],
                },
            ]
        }

def _get_saml_client():
    acs_url = ''.rstrip('/') + '/saml/acs/'
    metadata = _get_metadata()
    saml_settings = {
        'metadata': metadata,
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST)
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': False,
                'want_response_signed': False,
            },
        },
    }

    spConfig = Saml2Config()
    spConfig.load({
    'entityid': 'ezlogin/saml',
    "name": "faisa2l",
    # "name_id":"faisal@gamil.com",
    "service": {
        "sp": {
                "name": "Automation Hub SP",
                "name_id_format": saml2.saml.NAMEID_FORMAT_PERSISTENT,
                "allow_unsolicited": True,
                "endpoints": {
                    # "assertion_consumer_service": [
                    #     ("http://localhost:8010" + "/sso/acs/", saml2.BINDING_HTTP_POST),
                    # ],
                    # "single_logout_service": [
                    #     (BASE_URL + "/saml2/ls/", saml2.BINDING_HTTP_REDIRECT),
                    #     (BASE_URL + "/saml2/ls/post/", saml2.BINDING_HTTP_POST),
                    # ],
                },
                "force_authn": False,
                "name_id_format_allow_create": True,
                "required_attributes": ["emailAddress"],
                "authn_requests_signed": False,
                "logout_requests_signed": True,
                "want_assertions_signed": True,
                "want_response_signed": False,
            },
        "idp": {
            'name': 'testing IdP',
            'endpoints': {
                'single_sign_on_service': [
                    ('%s/sso/post' % BASE_URL, saml2.BINDING_HTTP_POST),
                    ('%s/sso/redirect' % BASE_URL, saml2.BINDING_HTTP_REDIRECT),
                ],
            },
            'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
        }
    },
    "key_file": "pki/mykey.pem",
    "cert_file": "pki/mycert.pem",
    "xmlsec_binary": "./xmlsec1.exe",
    "delete_tmpfiles": True,
    "metadata": metadata,
    
})

    spConfig.allow_unknown_attributes = True
    saml_client = Saml2Client(config=spConfig)
    return saml_client