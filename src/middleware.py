from src.apis.v1.middleware.middleware import AddActionMiddleWare
from src.apis.v1.constants.origins_enum import origins
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from Secweb.ExpectCt import ExpectCt
from Secweb.OriginAgentCluster import OriginAgentCluster
from Secweb.ReferrerPolicy import ReferrerPolicy
from Secweb.StrictTransportSecurity import HSTS
from Secweb.XContentTypeOptions import XContentTypeOptions
from Secweb.XDNSPrefetchControl import XDNSPrefetchControl
from Secweb.XDownloadOptions import XDownloadOptions
from Secweb.XFrameOptions import XFrame
from Secweb.XPermittedCrossDomainPolicies import XPermittedCrossDomainPolicies
from Secweb.xXSSProtection import xXSSProtection
from Secweb.CrossOriginEmbedderPolicy import CrossOriginEmbedderPolicy
from Secweb.CrossOriginOpenerPolicy import CrossOriginOpenerPolicy
from Secweb.CrossOriginResourcePolicy import CrossOriginResourcePolicy
from Secweb.ClearSiteData import ClearSiteData
from Secweb.CacheControl import CacheControl





def registering_middleware(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Access-Control-Allow-Headers","Set-Cookie", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    )
    
    application.add_middleware(ExpectCt, Option={'max-age': 128, 'enforce': True})
    application.add_middleware(OriginAgentCluster)
    application.add_middleware(ReferrerPolicy, Option={'Referrer-Policy': 'strict-origin-when-cross-origin'})
    application.add_middleware(HSTS, Option={'max-age': 4, 'preload': True})
    application.add_middleware(XContentTypeOptions)
    application.add_middleware(XDNSPrefetchControl, Option={'X-DNS-Prefetch-Control': 'on'})
    application.add_middleware(XDownloadOptions)
    application.add_middleware(XFrame, Option={'X-Frame-Options': 'DENY'})
    application.add_middleware(XPermittedCrossDomainPolicies, Option={'X-Permitted-Cross-Domain-Policies': 'none'})
    application.add_middleware(xXSSProtection, Option={'X-XSS-Protection': '0'})
    application.add_middleware(CrossOriginEmbedderPolicy, Option={'Cross-Origin-Embedder-Policy': 'unsafe-none'})
    application.add_middleware(CrossOriginOpenerPolicy, Option={'Cross-Origin-Opener-Policy': 'unsafe-none'})
    application.add_middleware(CrossOriginResourcePolicy, Option={'Cross-Origin-Resource-Policy': 'same-site'})
    # application.add_middleware(ClearSiteData, Option={'cookies': True}, Routes=['/login', '/logout/{id}'])
    application.add_middleware(ClearSiteData, Option={'cookies': True})
    application.add_middleware(CacheControl, Option={'s-maxage': 600, 'public': True})
    application.add_middleware(AddActionMiddleWare)
   
    