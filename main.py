import re
from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.responses import RedirectResponse,HTMLResponse, Response
import requests
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
from pydantic import BaseModel
from constants import Constants
from controller import SessionController

from loginprocessview import LoginProcessView
from fastapi.templating import Jinja2Templates
import uvicorn
import fastapi
from models import Base
from db.session import engine, get_db
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
from core.development_config import settings
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

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
create_tables()


@app.get("/sso/redirect/", tags=["Redirect Request Generated From Service Provider"])
async def read_root(request: Request, SAMLRequest: str,db: Session = Depends(get_db)):
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

@app.post("/login/process/", tags=["Submit Login Page API submission"])
async def read_root(response: Response,request: Request,email: str = Form(...),password: str = Form(...),saml_request: str = Form(...),db: Session = Depends(get_db)):
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


    '''
    '''


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

def test_logout_request_from_idp(remove_sp,name_id):
    from saml2.samlp import SessionIndex
    from saml2 import server
    idp_server = server.Server(config_file="./idp_conf.py")
    nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
             text=name_id)
    t_l = [
        "loadbalancer-91.siroe.com",
        "loadbalancer-9.siroe.com"
    ]
    t_l_2 = {
        "loadbalancer-9.siroe.com":"http://localhost:8000/slo/request",
        "loadbalancer-91.siroe.com":"http://localhost:8010/slo/request"
    }
    t_l.remove(remove_sp)

    req_id, req = idp_server.create_logout_request(
        issuer_entity_id=t_l[0],
        destination=t_l_2[t_l[0]],
        name_id=nid, reason="Tired", expire=in_a_while(minutes=15),
        session_indexes=["_foo"])

    # assert req.destination == "http://localhost:8088/logout/process"
    # assert req.reason == "Tired"
    # assert req.version == "2.0"
    # assert req.name_id == nid
    # assert req.issuer.text == "loadbalancer-9.siroe.com"
    # assert req.session_index == [SessionIndex("_foo")]
    print(req,"----req")
    info = idp_server.apply_binding(
    BINDING_SOAP, req, t_l_2[t_l[0]],
    relay_state="relay2")
    redirect_url = None
    print(info,"----info")
    response = requests.post(info['url'], data=info['data'], headers={'Content-Type': 'application/xml'})
    # test_logout_response_from_sp(info['data'])


# SAMLRequest: str
@app.get("/logout/process",tags=["Logout Request API From Service Provider"])
async def logout(request: Request,response : Response,SAMLRequest: str,db: Session = Depends(get_db),):
    print(SAMLRequest)
    from base64 import decodebytes as b64decode
    from saml2 import server
    idp_server = server.Server(config_file="./idp_conf.py")
    # print(req,"-----req-----")
    # info = saml_client.apply_binding(
    #     BINDING_HTTP_REDIRECT, req, destination="",
    #     relay_state="relay2")
    # print(data,"---reached here---")
    # loc = data['body']
    # qs = parse.parse_qs(loc[:])
    # print(qs)
    samlreq = SAMLRequest
    # resphttp = idp_server.handle_logout_request(samlreq, nid,
    #         BINDING_HTTP_REDIRECT)
    # _dic = unpack_form(resphttp['data'], "SAMLResponse")
    # xml = b64decode(_dic['SAMLResponse'].encode('UTF-8'))
    # print(xml,"---xml--")
    req_info = idp_server.parse_logout_request(samlreq, BINDING_HTTP_REDIRECT)
    print(vars(req_info),"---req_info---",req_info.message.name_id.text,vars(req_info.message),req_info.message.issuer.text)
    # response = RedirectResponse(url=redirect_url,status_code=status.HTTP_302_FOUND)

    # verify_request_signature(req_info)

    # resphttp = idp_server.handle_logout_request(samlreq, nid,
    #         BINDING_HTTP_REDIRECT)

    # find the users logged in database in which sp
    resp = idp_server.create_logout_response(req_info.message, [entity.BINDING_HTTP_REDIRECT])
    print(vars(resp.issuer),"--req_info--")
    hinfo = idp_server.apply_binding(entity.BINDING_HTTP_REDIRECT, resp.__str__(), resp.destination, "/", response=True)
    print(hinfo,"---hinfo---")
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
    print(redirect_url,"----redirect_url")
    response = RedirectResponse(url=redirect_url,status_code=status.HTTP_302_FOUND)
    verified_id = SessionController().verify_session(cookie,request)
    print(verified_id)
    if verified_id[1] == 200:
        verified_status = SessionController().check_session_db(db,verified_id[0])
        if verified_status[1] == 200:
            SessionController().delete_session(db,verified_id[0])
            cookie.delete_from_response(response)
        else:
            SessionController().delete_userid(db,req_info.message.name_id.text)
    
    # test_logout_request_from_idp(req_info.message.issuer.text,req_info.message.name_id.text)
    return response
    # response = HTMLResponse(content=resp["data"]["data"])
    # print(html_response)
    # return html_response
    # return ""
#   response = RedirectResponse('*your login page*', status_code= 302)
#   response.delete_cookie(key ='*your access token name*')
#   return response

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST_URL, port=settings.HOST_PORT, reload=True)