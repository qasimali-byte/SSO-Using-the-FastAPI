from src.packages.saml2_local.user_migrate_request import Saml2LocalEntity
from saml2.s_utils import rndstr
import saml2
import threading
from saml2.sdb import SessionStorage
from saml2.entity import Entity
from saml2.server import Server

class Saml2LocalServer(Saml2LocalEntity, Server):
    """ A class that does things that IdPs or AAs do """

    def __init__(
        self,
        config_file="",
        config=None,
        cache=None,
        stype="idp",
        symkey="",
        msg_cb=None,
    ):
        # pass
        # Saml2LocalEntity.__init__(self, stype, config, config_file, msg_cb=msg_cb)
        Server.__init__( self,
        config_file=config_file,
        config=config,
        cache=cache,
        stype=stype,
        symkey=symkey,
        msg_cb=msg_cb)
        # Saml2LocalEntity.__init__(self, stype, config, config_file, msg_cb=msg_cb)