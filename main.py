import re
from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.responses import RedirectResponse,HTMLResponse, Response
from pydantic import BaseModel

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

class SessionData(BaseModel):
    username: str

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
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

class temp():
    request1=""
value = ""
@app.get("/sso/redirect/")
async def read_root(request: Request, SAMLRequest: str):
    # print( await verifier.__call__(request))
    if cookie.__call__(request) == "No session cookie attached to request":
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})
    # return LoginProcessView().get()
    # print(request.url)
    print(SAMLRequest)
    print(request.cookies)
    print(vars(request))
    print( await verifier.__call__(request))
    # db = SAMLRequest
    # dbfile = open('examplePickle', 'ab')
      
    # # source, destination
    # pickle.dump(db, dbfile)                     
    # dbfile.close()
    # temp(request1=SAMLRequest)

    # check the session of the user
    # return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":SAMLRequest, "error": None})

@app.get("/acs")
async def acs(request: Request):
    print(vars(request))
    return templates.TemplateResponse("<html></html>",{"request": request})
    # response = RedirectResponse(url="http://localhost:3001/acs",)
    # return response

@app.post("/login/process/")
async def read_root(response: Response,request: Request,email: str = Form(...),password: str = Form(...),saml_request: str = Form(...),db: Session = Depends(get_db)):
    # print(vars(request.form))
    # print(request)

    # print(request['referer'])
    '''
    '''
    resp = LoginProcessView()
    user = resp.get_user(email,password,db)
    print(user)
    print(email,password)
    if user == None:
        return templates.TemplateResponse("loginform.html", {"request": request,"saml_request":saml_request, "error": "Invalid username or password"})
    print(vars(request))
    # print(request.headers['referer'])
    print(saml_request,"---saml_request")
    session = uuid4()
    cookie.attach_to_response(response, session)
    print(vars(response))
    print(session)
    return "seesion is attached"
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


    resp = resp.get(saml_request)
    # print(resp["data"]["data"])
    # return HTMLResponse(content=resp["data"]["data"]) #### thisone uncomment
    
    
    
    # return resp["data"]
    # return templates.TemplateResponse(resp["data"]["data"],{"request": request})
    # response = RedirectResponse(url="http://localhost:8088/acs")
    # return fastapi.responses.RedirectResponse(url="http://localhost:8088/acs",status_code=status.HTTP_302_FOUND)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)