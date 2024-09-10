import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from database.AppDatabase import AppDatabase
from routers import router as LoyaltyRouter
from config.config import get_settings


def get_openapi_schema():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers
        )

        for _, path in app.openapi_schema.get('paths').items():
            for _, param in path.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']

        del app.openapi_schema['components']['schemas']['HTTPValidationError']
        del app.openapi_schema['components']['schemas']['ValidationError']
    return app.openapi_schema


settings = get_settings()
app = FastAPI(title="OpenAPI definition",
              version="v1",
              servers=[
                  {"url": f"http://localhost:{settings['port']}"},
                  {"url": f"http://{settings['external_ip']}:{settings['port']}"}
              ]
              )
app.include_router(LoyaltyRouter, prefix='')
app.openapi = get_openapi_schema
app_db = AppDatabase.app_db


@app.exception_handler(HTTPException)
async def on_exception(request: Request, exception: HTTPException):
    return JSONResponse(status_code=exception.status_code, content={"Message": exception.detail})


if __name__ == "__main__":
    app_db.create_all()
    uvicorn.run('main:app',
                host=settings['host'],
                port=settings['port'],
                #ssl_keyfile="app/config/keys/private.key",
                #ssl_certfile="app/config/keys/identity_provider.ca.crt",
                log_level=settings['log_level'],
                reload=settings['reload'])
