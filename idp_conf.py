CONFIG = {
    # "entityid": "http://saml.example.com:saml/idp.xml",
    "name": "Rolands IdP",
    # "service": {
    #     "idp": {
    #         "endpoints": {
    #             "single_sign_on_service": [
    #                 (
    #                     "http://localhost:8088/sso/redirect",
    #                     BINDING_HTTP_REDIRECT,
    #                 ),
    #             ],
    #             "single_logout_service": [
    #                 (
    #                     "http://saml.example.com:saml:8088/slo",
    #                     BINDING_HTTP_REDIRECT,
    #                 ),
    #             ],
    #         },
    #     }
    # },
    "key_file": "pki/mykey.pem",
    "cert_file": "pki/mycert.pem",
    "xmlsec_binary": "./xmlsec1.exe",
    "delete_tmpfiles": True,
    "metadata": {
            'local': ['metadata/sp.xml','metadata/sp1.xml','metadata/ezsp.xml']
        },
    
    # "attribute_map_dir": "attributemaps",
}