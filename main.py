from src.app import create_app
import populate
application = create_app()

if __name__ == "__main__":
    from src import settings_by_env
    import uvicorn
    uvicorn.run("main:application", host=settings_by_env.HOST_URL, port=settings_by_env.HOST_PORT, reload=True)
    
    