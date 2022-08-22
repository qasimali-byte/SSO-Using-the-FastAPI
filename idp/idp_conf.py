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
    "key_file": "idp/pki/mykey.pem",
    "cert_file": "idp/pki/mycert.pem",
    "xmlsec_binary": "idp/xmlsec1.exe",
    "delete_tmpfiles": True,
    "metadata": {
            'local': ['idp/metadata/sp.xml','idp/metadata/sp1.xml','idp/metadata/ezsp.xml','idp/metadata/ezsplocal.xml',
            'idp/metadata/ezweb.xml']
        },
    
    # "attribute_map_dir": "attributemaps",
}