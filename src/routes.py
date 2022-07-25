from src.apis.v1.routes import forget_password_routes, sps_routes, idp_routes,auth_routes,user_routes,\
     frontend_routes,staticfiles_routes, roles_routes, practices_routes, users_routes
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from src.graphql.schemas.query_schema import Query

schema = strawberry.Schema(query=Query,config=StrawberryConfig(auto_camel_case=True))
graphql_app = GraphQLRouter(schema)
api_url : str = "/api/v1"

def registering_routes(app):
    app.include_router(staticfiles_routes.router, prefix=api_url)
    app.include_router(sps_routes.router, prefix=api_url)
    app.include_router(idp_routes.router)
    app.include_router(auth_routes.router, prefix=api_url)
    app.include_router(user_routes.router, prefix=api_url)
    app.include_router(frontend_routes.router)
    app.include_router(roles_routes.router, prefix=api_url)
    app.include_router(practices_routes.router, prefix=api_url)
    app.include_router(users_routes.router,prefix=api_url)
    app.include_router(forget_password_routes.router,prefix=api_url)    
    app.include_router(graphql_app, prefix="/graphql")