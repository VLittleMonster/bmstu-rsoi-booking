from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import status
import schemas.dto as schemas


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    for err in exc.errors():
        if err['loc'][0] == 'header' and err['loc'][1] == 'Authorization':
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
