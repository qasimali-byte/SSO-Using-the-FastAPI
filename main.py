import load_env
from src.app import create_app
application = create_app()

@application.on_event("startup")
async def startup_event():
    try:
        import populate
    except:
        pass
    
if __name__ == "__main__":
    from src import settings_by_env
    import uvicorn
    uvicorn.run("main:application", host=settings_by_env.HOST_URL, port=settings_by_env.HOST_PORT, reload=True)
    
    