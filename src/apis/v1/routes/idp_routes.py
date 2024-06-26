from fastapi import Depends, Form, Request, APIRouter, Response
from fastapi_redis_session import SessionStorage, getSessionStorage

from src.apis.v1.core.project_settings import Settings
from src.apis.v1.controllers.idp_controller import IDPController
from fastapi_sessions.frontends.implementations.cookie import CookieParameters, CookieParameters2
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse, Response
import requests
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
from pydantic import BaseModel
from controller import SessionController

from loginprocessview import LoginProcessView
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
from uuid import UUID, uuid4
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
    BINDING_SOAP
)
from saml2.time_util import in_a_while

from serializers import SamlRequestSerializer
from src.apis.v1.models.idp_users_sp_apps_email_model import idp_users_sp_apps_email

router = APIRouter(tags=["Identity Provider"])
templates = Jinja2Templates(directory="templates/")


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()
cookie_params_2 = CookieParameters2()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie_idp",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

cookie_frontend = SessionCookie(
    cookie_name="cookie_frontend",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params_2,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: str,
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend="",
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


@router.post("/sso/", summary="Only Redirect Request from Service Provider")
async def sso_redirect(request: Request, SAMLRequest: str, db: Session = Depends(get_db)):
    verified_id = SessionController().verify_session(cookie_frontend, request)
    idp_controller = IDPController(db)
    verified_data = idp_controller.get_frontend_session_saml(verified_id[0])
    req = LoginProcessView()
    resp = req.get(verified_data[0].saml_req,"syed@gmail.com")
    resp = resp[0]
    return HTMLResponse(content=resp["data"]["data"])


@router.get("/sso/redirect/", summary="Only Redirect Request from Service Provider")
async def sso_redirect(request: Request, SAMLRequest: str,
                       sessionStorage: SessionStorage = Depends(getSessionStorage),
                       db: Session = Depends(get_db)
                       ):
    # this will be use for idp-initiated login
    # validate saml request parameter
    # if not validate_saml_request(SAMLRequest):
    # return Response(status_code=400, content="Invalid SAML Request")
    # get saml request data
    # give unique cookie to localhost + this cookie with the sp comes from with saml request should be stored in db
    # return to login page localhost:3000

    # print( await verifier.__call__(request))
    req = LoginProcessView()
    ## check the valid samrequest
    SamlRequestSerializer(SAMLRequest=SAMLRequest)

    verified_id = SessionController().verify_session(cookie, request)
    if verified_id[1] == 200:
        # verified_status = SessionController().check_session_redis(sessionStorage, verified_id[0])
        verified_status = SessionController().check_session_db(db, verified_id[0])
        if verified_status[1] == 200:

            email_ = req.get_userid(verified_id[0],db)
            resp=req.verify_app_allowed(SAMLRequest,db,email_)
            status_code = resp['status_code']
            if status_code == 307:
                return templates.TemplateResponse("notification.html",{"request": request})
            # here we will decide either users rediraction
            targeted_sp_app_id=resp['targeted_sp_app_id']
            result=req.get_sp_apps_email(db,targeted_sp_app_id,email_)
            if result is not None:
                sp_apps_email = result
                resp=req.get_multiple_account_access(SAMLRequest,sp_apps_email,email_,db)
            else:
                resp = req.get(SAMLRequest,email_,db)
            resp = resp[0]
            return HTMLResponse(content=resp["data"]["data"])

    session = uuid4()
    # store the cookie in db
    IDPController(db).store_frontend_saml(session,SAMLRequest)
    # response = templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})
    host = Settings().SSO_FRONTEND_URL
    # logout the user from frontend as well
    
    # response = RedirectResponse(url="http://{}/sign-in".format("localhost:8088"))

    response = RedirectResponse(url="{}sign-in".format(host)) 
    cookie_frontend.attach_to_response(response, session)
    return response


@router.post("/sso/login", summary="Submit Login Page API submission")
async def sso_login(response: Response, request: Request, email: str = Form(...), password: str = Form(...),
                    saml_request: str = Form(...), db: Session = Depends(get_db)):
    '''
    this will also is using in idp initiated login flow
    '''
    valid_session = True

    ### verify session if exsists
    if cookie.__call__(request) == "No session cookie attached to request":
        valid_session = False

    ## session verification
    verify_session = await verifier.__call__(request)
    if verify_session[1] != True:
        # delete the cookie from browser and db
        valid_session = False

    ## session verification in db
    resp = LoginProcessView()
    if resp.get_session(verify_session[0], db) == "session not found":
        valid_session = False

    if valid_session == True:
        return "session found"

    # resp = LoginProcessView()
    user = resp.get_user(email, password, db)
    if user == None:
        return templates.TemplateResponse("loginform.html", {"request": request, "saml_request": saml_request,
                                                             "error": "Invalid username or password"})
    response=resp.verify_app_allowed(saml_request,db,email)
    status_code = response['status_code']
    if status_code == 307:
        return templates.TemplateResponse("notification.html",{"request": request,})
    targeted_sp_app_id=response['targeted_sp_app_id']
    result=resp.get_sp_apps_email(db,targeted_sp_app_id,email)
    session = uuid4()
    if result is not None:
        sp_apps_email = result
        resp.store_session(session,email,db)
        resp=resp.get_multiple_account_access(saml_request,sp_apps_email,email,db)
    else:
        resp.store_session(session,email,db)
        resp = resp.get(saml_request,email,db)
    ## store session in the database
    application_entity_id = resp[1]['sp_entity_id']
    resp = resp[0]
    response = HTMLResponse(content=resp["data"]["data"]) #### thisone uncomment
    cookie.attach_to_response(response, session)
    return response


def test_logout_request_from_idp(remove_sp, name_id):
        
    
    from saml2.samlp import SessionIndex
    from saml2 import server
    idp_server = server.Server(config_file="idp/idp_conf.py")
    nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
                 text=name_id)
    t_l = [
        "loadbalancer-91.siroe.com",
        "loadbalancer-9.siroe.com"
    ]
    t_l_2 = {
        "loadbalancer-9.siroe.com": "http://localhost:8000/slo/request",
        "loadbalancer-91.siroe.com": "http://localhost:8010/slo/request"
    }
    t_l.remove(remove_sp)

    req_id, req = idp_server.create_logout_request(
        issuer_entity_id=t_l[0],
        destination=t_l_2[t_l[0]],
        name_id=nid, reason="Tired", expire=in_a_while(minutes=15),
        session_indexes=["_foo"])

    info = idp_server.apply_binding(
        BINDING_SOAP, req, t_l_2[t_l[0]],
        relay_state="relay2")
    redirect_url = None
    try:
        response = requests.post(info['url'], data=info['data'], headers={'Content-Type': 'application/xml'})
    except Exception as e:
        print(e, "----e")


# SAMLRequest: str
@router.get("/sso/logout", summary=["Logout Request API From Service Provider"])
async def logout(request: Request, response: Response, SAMLRequest: str, db: Session = Depends(get_db), ):
    from base64 import decodebytes as b64decode
    from saml2 import server
    idp_server = server.Server(config_file="idp/idp_conf.py")

    samlreq = SAMLRequest

    req_info = idp_server.parse_logout_request(samlreq, BINDING_HTTP_REDIRECT)
    # response = RedirectResponse(url=redirect_url,status_code=status.HTTP_302_FOUND)

    # verify_request_signature(req_info)

    # resphttp = idp_server.handle_logout_request(samlreq, nid,
    #         BINDING_HTTP_REDIRECT)

    # find the users logged in database in which sp
    resp = idp_server.create_logout_response(req_info.message, [entity.BINDING_HTTP_REDIRECT])
    hinfo = idp_server.apply_binding(entity.BINDING_HTTP_REDIRECT, resp.__str__(), resp.destination, "/", response=True)
    # create logout request for sp2
    # test_logout_request_from_idp("loadbalancer-91.siroe.com")
    # html_response = {
    #     "data": hinfo,
    #     "type": "REDIRECT",
    # }
    redirect_url = None
    for key, value in hinfo['headers']:
        if key == 'Location':
            redirect_url = value
            break
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    verified_id = SessionController().verify_session(cookie, request)
    if verified_id[1] == 200:
        verified_status = SessionController().check_session_db(db, verified_id[0])
        if verified_status[1] == 200:
            SessionController().delete_session(db, verified_id[0])
            cookie.delete_from_response(response)
        else:
            SessionController().delete_userid(db, req_info.message.name_id.text)

    # test_logout_request_from_idp(req_info.message.issuer.text,req_info.message.name_id.text)
    return response
