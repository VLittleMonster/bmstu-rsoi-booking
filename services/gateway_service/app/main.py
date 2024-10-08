import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from routers import router as GatewayRouter
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
                  {"url": f"http://{settings['external_ip']}:{settings['port']}"},
                  {"url": f"http://localhost:{settings['port']}"}
              ]
              )
app.include_router(GatewayRouter, prefix='')
app.openapi = get_openapi_schema
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run('main:app',
                host=settings['host'],
                port=settings['port'],
                log_level=settings['log_level'],
                reload=settings['reload'])
