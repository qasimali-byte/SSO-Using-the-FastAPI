from fastapi import Depends, Form, Request, APIRouter, Response
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.responses import RedirectResponse,HTMLResponse, Response
import requests
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
from pydantic import BaseModel
from controller import SessionController

from loginprocessview import LoginProcessView
from fastapi.templating import Jinja2Templates
import uvicorn
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
router = APIRouter(tags=["Identity Provider"])
templates = Jinja2Templates(directory="templates/")

class SessionData(BaseModel):
    username: str

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie_idp",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
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

@router.get("/sso/redirect/",summary="Only Redirect Request from Service Provider")
async def sso_redirect(request: Request, SAMLRequest: str,db: Session = Depends(get_db)):
    # validate saml request parameter
    # if not validate_saml_request(SAMLRequest):
        # return Response(status_code=400, content="Invalid SAML Request")
    # get saml request data
    # give unique cookie to localhost + this cookie with the sp comes from with saml request should be stored in db
    # return to login page localhost:3000

    # print( await verifier.__call__(request))
    req = LoginProcessView()
    ## check the valid samrequest
    print(SAMLRequest,"----SAMLRequest")
    SamlRequestSerializer(SAMLRequest=SAMLRequest)
    # resp = req.get(SAMLRequest,email_)

    verify_cookie = cookie.__call__(request)
    if  verify_cookie == "No session cookie attached to request":
        print("No session cookie attached to request")
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})
    
    if verify_cookie == "Invalid session provided":
        print("Invalid session provided")
        # delete the cookie from browser and db
        # req.delete_cookie(verify_session[0],request)
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})
    ## session verification
    verify_session = await verifier.__call__(request)
    if verify_session[1] != True:
        print("Invalid session provided")
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})

    ## session verification in db
    if req.get_session(verify_session[0],db) == "session not found":
        print("session not found")
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})

    # return LoginProcessView().get()
    # print(request.url)
    print(SAMLRequest)
    print(request.cookies)
    print(vars(request))
    print( await verifier.__call__(request))
    email_ = req.get_userid(verify_session[0],db)
    resp = req.get(SAMLRequest,email_)
    # print(resp["data"]["data"])
    print("session found")

    return HTMLResponse(content=resp["data"]["data"]) #### thisone uncomment
    # return "session found"
    # db = SAMLRequest
    # dbfile = open('examplePickle', 'ab')
      
    # # source, destination
    # pickle.dump(db, dbfile)                     
    # dbfile.close()
    # temp(request1=SAMLRequest)

    # check the session of the user
    # return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})
    

@router.post("/sso/login", summary="Submit Login Page API submission")
async def sso_login(response: Response,request: Request,email: str = Form(...),password: str = Form(...),saml_request: str = Form(...),db: Session = Depends(get_db)):
    # print(vars(request.form))
    # print(request)

    # print(request['referer'])
    '''
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
    if resp.get_session(verify_session[0],db) == "session not found":
        valid_session = False


    if valid_session == True:
        return "session found"

    # resp = LoginProcessView()
    user = resp.get_user(email,password,db)
    if user == None:
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":saml_request, "error": "Invalid username or password"})
    print(vars(request))
    # print(request.headers['referer'])
    print(saml_request,"---saml_request")
    session = uuid4()
    print(session)
    ## store session in the database
    resp.store_session(session,email,db)
    
    print(vars(response))
    print(session)
    # return "seesion is attached"
    # print(username,password)
    # req = temp().request1
    # print(temp().request1)
    # dbfile = open('examplePickle', 'rb')     
    # db = pickle.load(dbfile)
    # dbfile.close()
    # print(db,"-------")
    # db = "http://localhost:8088/sso/redirect/?SAMLRequest="+db

    resp = resp.get(saml_request, email)
    print(resp["data"]["data"])
    response = HTMLResponse(content=resp["data"]["data"]) #### thisone uncomment
    cookie.attach_to_response(response, session)
    # return "session attached"
    return response
    
    
    
    # return resp["data"]
    # return templates.TemplateResponse(resp["data"]["data"],{"request": request})
    # response = RedirectResponse(url="http://localhost:8088/acs")
    # return fastapi.responses.RedirectResponse(url="http://localhost:8088/acs",status_code=status.HTTP_302_FOUND)

@router.get("/sso/logout",summary="Logout Request API From Service Provider")
async def sso_logout(request: Request,response : Response,SAMLRequest: str,db: Session = Depends(get_db)):
    pass