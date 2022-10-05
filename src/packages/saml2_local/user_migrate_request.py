from saml2.entity import Entity
from saml2.saml import NameID
from saml2 import SAMLError
from saml2.samlp import AuthnRequest, SessionIndex, response_from_string, RequestAbstractType_
from saml2 import saml

NAMESPACE = 'urn:oasis:names:tc:SAML:2.0:protocol'

class UserMigrationRequestType_(RequestAbstractType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:LogoutRequestType element """

    c_tag = 'UserMigrationRequestType'
    c_namespace = NAMESPACE
    c_children = RequestAbstractType_.c_children.copy()
    c_attributes = RequestAbstractType_.c_attributes.copy()
    c_child_order = RequestAbstractType_.c_child_order[:]
    c_cardinality = RequestAbstractType_.c_cardinality.copy()
    c_children['{urn:oasis:names:tc:SAML:2.0:assertion}BaseID'] = (
        'base_id', saml.BaseID)
    c_cardinality['base_id'] = {"min": 0, "max": 1}
    c_children['{urn:oasis:names:tc:SAML:2.0:assertion}NameID'] = (
        'name_id', saml.NameID)
    c_cardinality['name_id'] = {"min": 0, "max": 1}
    c_children['{urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID'] = (
        'encrypted_id', saml.EncryptedID)
    c_cardinality['encrypted_id'] = {"min": 0, "max": 1}
    c_children['{urn:oasis:names:tc:SAML:2.0:protocol}SessionIndex'] = (
        'session_index', [SessionIndex])
    c_cardinality['session_index'] = {"min": 0}
    c_attributes['Reason'] = ('reason', 'string', False)
    c_attributes['NotOnOrAfter'] = ('not_on_or_after', 'dateTime', False)
    c_child_order.extend(
        ['base_id', 'name_id', 'encrypted_id', 'session_index'])

    def __init__(self,
                 base_id=None,
                 name_id=None,
                 encrypted_id=None,
                 session_index=None,
                 reason=None,
                 not_on_or_after=None,
                 issuer=None,
                 signature=None,
                 extensions=None,
                 id=None,
                 version=None,
                 issue_instant=None,
                 destination=None,
                 consent=None,
                 text=None,
                 extension_elements=None,
                 extension_attributes=None):
        RequestAbstractType_.__init__(self,
                                      issuer=issuer,
                                      signature=signature,
                                      extensions=extensions,
                                      id=id,
                                      version=version,
                                      issue_instant=issue_instant,
                                      destination=destination,
                                      consent=consent,
                                      text=text,
                                      extension_elements=extension_elements,
                                      extension_attributes=extension_attributes)
        self.base_id = base_id
        self.name_id = name_id
        self.encrypted_id = encrypted_id
        self.session_index = session_index or []
        self.reason = reason
        self.not_on_or_after = not_on_or_after

class UserMigrationRequest(UserMigrationRequestType_):
    """The urn:oasis:names:tc:SAML:2.0:protocol:LogoutRequest element """

    c_tag = 'UserMigrationRequest'
    c_namespace = NAMESPACE
    c_children = UserMigrationRequestType_.c_children.copy()
    c_attributes = UserMigrationRequestType_.c_attributes.copy()
    c_child_order = UserMigrationRequestType_.c_child_order[:]
    c_cardinality = UserMigrationRequestType_.c_cardinality.copy()

class Saml2LocalEntity(Entity):
    def __init__(self, entity_type, config=None, config_file="", virtual_organization="", msg_cb=None):
        super().__init__(entity_type, config, config_file, virtual_organization, msg_cb)

    def create_migrate_request(
        self,
        destination,
        issuer_entity_id,
        subject_id=None,
        name_id=None,
        reason=None,
        expire=None,
        message_id=0,
        consent=None,
        extensions=None,
        sign=None,
        session_indexes=None,
        sign_alg=None,
        digest_alg=None,
        ):
        if subject_id:
            if self.entity_type == "idp":
                name_id = NameID(
                    text=self.users.get_entityid(subject_id, issuer_entity_id, False)
                )
            else:
                name_id = NameID(text=subject_id)

        if not name_id:
            raise SAMLError("Missing subject identification")

        args = {}
        if session_indexes:
            sis = []
            for si in session_indexes:
                if isinstance(si, SessionIndex):
                    sis.append(si)
                else:
                    sis.append(SessionIndex(text=si))
            args["session_index"] = sis

        return self._message(
            UserMigrationRequest,
            destination,
            message_id,
            consent,
            extensions,
            sign,
            name_id=name_id,
            reason=reason,
            not_on_or_after=expire,
            issuer=self._issuer(),
            sign_alg=sign_alg,
            digest_alg=digest_alg,
            **args,
        )
